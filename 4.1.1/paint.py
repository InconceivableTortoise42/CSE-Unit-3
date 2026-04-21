from __future__ import annotations  
from typing import TYPE_CHECKING
from PIL import Image, ImageTk
from colorbar import ColorBar
from toolbar import ToolBar
import tkinter as tk
import numpy as np

if TYPE_CHECKING:
    from tools import Tool

class Paint(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(background = "gray")

        self.width = 600
        self.height = 600

        self.pixel_size = 4

        self.undoStack = []
        self.redoStack = []

        self.lastPos = (0, 0)
        self.currentStroke = []

        # Toolbar + Colorbar

        self.colorBar = ColorBar(self, self.setColor)
        self.colorBar.pack(side = "bottom", fill = "x")

        self.toolBar = ToolBar(self, self.setTool)
        self.toolBar.pack(side = "left", fill = "y")

        self.currentTool = self.toolBar.getTool()
        self.currentColor = self.colorBar.getColor()

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
        # self.canvas.bind("<Button-3>", lambda _: self.strokeCancel())


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
        self.lastPos = (event.x, event.y)
        self.render()        

    def mouseMove(self, event):
        event.x = int(event.x / self.pixel_size)
        event.y = int(event.y / self.pixel_size)
        self.currentTool.on_mouse_move(self, event)

    def keyEnter(self):
        self.currentTool.on_enter(self)

    def rect(self, start, stop, fill = False, temp = False):
        if temp:
            buffer = self.tempBuffer
        else:
            buffer = self.buffer

        x1, x2 = sorted([start[0], stop[0]])
        y1, y2 = sorted([start[1], stop[1]])

        buffer[y1 : y2 + 1, x1 : x2 + 1] = self.currentColor

        if temp:
            self.tempMask[y1 : y2 + 1, x1 : x2 + 1] = True

    def line(self, start, stop, temp = False):
        if temp:
            buffer = self.tempBuffer
        else:
            buffer = self.buffer

        steps = max(np.abs(np.array(start) - stop)) + 1
        points = np.round(np.linspace(start, stop, steps)).astype(int)

        buffer[points[:, 1], points[:, 0]] = self.currentColor

        if temp:
            self.tempMask[points[:, 1], points[:, 0]] = True

    def ellipse(self, start, stop, fill = False, temp = False):
        if temp:
            buffer = self.tempBuffer
        else:
            buffer = self.buffer

        x1, x2 = sorted([start[0], stop[0]])
        y1, y2 = sorted([start[1], stop[1]])

        width = (x2 - x1) + 2
        height = (y2 - y1) + 2

        for x in range(width):
            for y in range(height):
                normalized = ((2.0 * x / width) - 1.0, 1.0 - (2.0 * y / height))
                if (0.95 < normalized[0] ** 2 + normalized[1] ** 2 < 1.05):
                    buffer[y1 + y, x1 + x] = self.currentColor 

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

        self.after(1, lambda: self.tempBuffer.fill(0))
        self.after(1, lambda: self.tempMask.fill(False))

    def onCanvas(self, x, y) -> bool:
        if 0 <= x * self.pixel_size < self.width and 0 <= y * self.pixel_size < self.height:
            return True
        else:
            return False
    
    # def strokeCancel(self):
    #     # Canceling stroke
    #     if self.currentStroke:
    #         for point in self.currentStroke:
    #             self.brush3x3(point[0], point[1], (255, 255, 255))

    #     self.currentStroke = []
    #     self.render()
