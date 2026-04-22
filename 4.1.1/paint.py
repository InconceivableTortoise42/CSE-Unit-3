from __future__ import annotations  
from typing import TYPE_CHECKING
from network import NetworkHander
from PIL import Image, ImageTk
from colorbar import ColorBar
from toolbar import ToolBar
from point import Point
import tkinter as tk
import numpy as np
import actions

if TYPE_CHECKING:
    from tools import Tool

class Paint(tk.Frame):
    def __init__(self, network = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(background = "gray")

        self.width = 600
        self.height = 600

        self.pixel_size = 4

        self.undoStack = []
        self.redoStack = []

        self.lastPos: Point = Point(0, 0)
        self.currentStroke = []

        # Toolbar + Colorbar

        self.colorBar = ColorBar(self, self.setColor)
        self.colorBar.pack(side = "bottom", fill = "x")

        self.toolBar = ToolBar(self, self.setTool)
        self.toolBar.pack(side = "left", fill = "y")

        self.currentTool = self.toolBar.getTool()
        self.currentColor: tuple[int, int, int] = self.colorBar.getColor()

        # Canvas Buffer and Image

        self.canvas = tk.Canvas(self,
             width = self.width,
             height = self.height,
             borderwidth = 0,
             highlightthickness = 0
        )

        self.canvas.pack(expand = True, anchor = "nw")

        self.buffer = np.full((int(self.height / self.pixel_size), int(self.width / self.pixel_size), 3), 255, dtype = np.uint8)
        self.tempBuffer = np.zeros((int(self.height / self.pixel_size), int(self.width / self.pixel_size), 3), dtype = np.uint8)
        self.tempMask = np.zeros((int(self.height / self.pixel_size), int(self.width / self.pixel_size)), dtype = bool)

        self.image = self.canvas.create_image(0, 0, anchor = "nw")

        self.render()

        # Canvas Events

        self.canvas.bind("<B1-Motion>", self.mouseDrag)
        self.canvas.bind("<ButtonRelease-1>", self.mouseUp)
        self.canvas.bind("<ButtonPress-1>", self.mouseDown)
        self.canvas.bind("<Motion>", self.mouseMove)
        self.master.bind("<Return>", lambda _: self.keyEnter())

        # Network
        if network:
            self.networkHandler = NetworkHander("", self)


    def setTool(self, tool: Tool):
        self.currentTool = tool

    def setColor(self, color):
        self.currentColor = color

    def mouseDrag(self, event):
        event.x = int(event.x / self.pixel_size)
        event.y = int(event.y / self.pixel_size)
        self.currentTool.on_mouse_drag(self, event)
        self.render()        

    def mouseUp(self, event):
        event.x = int(event.x / self.pixel_size)
        event.y = int(event.y / self.pixel_size)
        self.currentTool.on_mouse_up(self, event)
        self.render()        

    def mouseDown(self, event):
        event.x = int(event.x / self.pixel_size)
        event.y = int(event.y / self.pixel_size)
        self.currentTool.on_mouse_down(self, event)
        self.lastPos = Point(event.x, event.y)
        self.render()        

    def mouseMove(self, event):
        event.x = int(event.x / self.pixel_size)
        event.y = int(event.y / self.pixel_size)
        self.currentTool.on_mouse_move(self, event)

    def keyEnter(self):
        self.currentTool.on_enter(self)

    def clearTempBuffer(self):
        self.tempBuffer.fill(0)
        self.tempMask.fill(False)

    def onCanvas(self, x, y) -> bool:
        if 0 <= x * self.pixel_size < self.width and 0 <= y * self.pixel_size < self.height:
            return True
        else:
            return False

    def rect(self, start: Point, stop: Point, color = None, fill = False, temp = False):
        if not color:
            color = self.currentColor

        if temp:
            self.clearTempBuffer()
            buffer = self.tempBuffer
        else:
            buffer = self.buffer

            self.networkHandler.sendAction({
                "rect": {
                    "start": start,
                    "stop": stop,
                    "fill": fill,
                    "color": color
                }
            })

        actions.rect(buffer, start, stop, color, )

    def line(self, start: Point, stop: Point, temp = False):
        if temp:
            self.clearTempBuffer()
            buffer = self.tempBuffer
        else:
            buffer = self.buffer

            self.networkHandler.sendAction({
                "line": {
                    "start": start,
                    "stop": stop
                }
            })

    def ellipse(self, start: Point, stop: Point, fill = False, temp = False):
        if temp:
            self.clearTempBuffer()
            buffer = self.tempBuffer
        else:
            buffer = self.buffer
            self.networkHandler.sendAction({
                "ellipse": {
                    "start": start,
                    "stop": stop,
                    "fill": fill
                }
            })

    def fill(self, point: Point):

        self.networkHandler.sendAction({
            "fill": {
                "point": point,
                "color": self.currentColor
            }
        })

    def render(self):
        # NumPy -> PIL -> PhotoImage

        # Expand mask into third dimension to make np.where work [x, y, None] = True | False
        mask = self.tempMask[..., None]

        pilImage = Image.fromarray(
            np.where(mask, self.tempBuffer, self.buffer)
        ).resize(
            (self.width, self.height),
              Image.NEAREST # type: ignore
        ) 

        self.imageTK = ImageTk.PhotoImage(pilImage)

        self.canvas.itemconfig(self.image, image = self.imageTK)

    def runAction(self, data):
        pass
