from PIL import Image, ImageTk 
from colorbar import ColorBar
from toolbar import ToolBar
from tools import Tool
import tkinter as tk
import numpy as np

class Paint(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(background = "gray")

        self.width = 600
        self.height = 600

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

        self.canvas = tk.Canvas(self, width = self.width, height = self.height)
        self.canvas.pack(expand = True, anchor = "nw")

        self.buffer = np.full((self.height, self.width, 3), 255, dtype = np.uint8)

        self.image = self.canvas.create_image(0, 0, anchor = "nw")
        self.render()

        # Canvas Events

        self.canvas.bind("<B1-Motion>", self.mouseDrag)
        self.canvas.bind("<ButtonRelease-1>", self.mouseUp)
        self.canvas.bind("<ButtonPress-1>", self.mouseDown)
        self.canvas.bind("<Button-3>", lambda _: self.strokeCancel())


    def setTool(self, tool: Tool):
        self.currentTool = tool

    def setColor(self, color):
        self.currentColor = color

    def mouseDrag(self, event):
        num_steps = max(np.abs(np.array(self.lastPos) - (event.x, event.y))) + 1
        points = np.round(np.linspace(self.lastPos, (event.x, event.y), num_steps)).astype(int)

        self.lastPos = np.array([event.x, event.y])

        for point in points:
            self.brush3x3(point[0], point[1])
            self.currentStroke.append((int(point[0]), int(point[1])))

        self.render()        

    def mouseUp(self, event):
        self.currentStroke.append((event.x, event.y))
        self.currentStroke = []

    def mouseDown(self, event):
        self.lastPos = (event.x, event.y)

    def strokeCancel(self):
        # Canceling stroke
        if self.currentStroke:
            for point in self.currentStroke:
                self.brush3x3(point[0], point[1], (255, 255, 255))

        self.currentStroke = []
        self.render()

    def brush3x3(self, x, y, color = None):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y - 1 : y + 2, x - 1 : x + 2] = color if color else self.currentColor

    def render(self):
        # NumPy -> PIL -> PhotoImage

        pilImage = Image.fromarray(self.buffer)

        self.imageTK = ImageTk.PhotoImage(pilImage)

        self.canvas.itemconfig(self.image, image = self.imageTK)

