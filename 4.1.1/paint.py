from __future__ import annotations  
from typing import TYPE_CHECKING
from network import NetworkHander
from dataclasses import asdict
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

    def rect(self, start: Point, stop: Point, color = None, fill = False, temp = False):
        if not color:
            color = self.currentColor

        if temp:
            self.clearTempBuffer()
            actions.rect(self.tempBuffer, start, stop, color, self.tempMask)

        else:
            actions.rect(self.buffer, start, stop, color)

            self.networkHandler.sendAction({
                "rect": {
                    "start": asdict(start),
                    "stop": asdict(stop),
                    "color": color,
                    "fill": fill
                }
            })


    def line(self, start: Point, stop: Point, color, temp = False):
        if temp:
            self.clearTempBuffer()
            actions.line(self.tempBuffer, start, stop, color, self.tempBuffer)        

        else:
            actions.line(self.buffer, start, stop, color)        

            self.networkHandler.sendAction({
                "line": {
                    "start": asdict(start),
                    "stop": asdict(stop),
                    "color": color
                }
            })

    def ellipse(self, start: Point, stop: Point, color, fill = False, temp = False):
        if temp:
            self.clearTempBuffer()
            actions.ellipse(self.tempBuffer, start, stop, color, fill, self.tempMask)

        else:
            actions.ellipse(self.buffer, start, stop, color, fill)

            self.networkHandler.sendAction({
                "ellipse": {
                    "start": asdict(start),
                    "stop": asdict(stop),
                    "color": color,
                    "fill": fill
                }
            })

    def fill(self, point: Point, color):
        actions.floodFill(self.buffer, point, color)

        self.networkHandler.sendAction({
            "fill": {
                "point": point,
                "color": color
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
        if "rect" in data:
            rect = data["rect"]
            actions.rect(self.buffer, Point(**rect["start"]), Point(**rect["stop"]), rect["color"], rect["fill"]) 
        
        elif "line" in data:
            line = data["line"]
            actions.line(self.buffer, Point(**line["start"]), Point(**line["stop"]), line["color"])

        elif "ellipse" in data:
            ellipse = data["ellipse"]
            actions.ellipse(self.buffer, Point(**ellipse["start"]), Point(**ellipse["stop"]), ellipse["color"], ellipse["fill"])

        elif "fill" in data:
            fill = data["fill"]
            actions.floodFill(self.buffer, Point(**fill["point"]), fill["color"])
