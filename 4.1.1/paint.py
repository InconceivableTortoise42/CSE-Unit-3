from __future__ import annotations  
from typing import TYPE_CHECKING
from PIL import Image, ImageTk
from collections import deque
from colorbar import ColorBar
from toolbar import ToolBar
import tkinter as tk
import numpy as np
import websockets
import threading
import asyncio
import queue
import json

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

        # Start Network Handler

        self.wsURL = "ws://localhost"
        self.websocketQueue = queue.Queue()

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
            self.clearTempBuffer()
            buffer = self.tempBuffer
        else:
            buffer = self.buffer
            self.broadcast({
                "rect": {
                    "start": start,
                    "stop": stop,
                    "fill": fill
                }
            })

        x1, x2 = sorted([start[0], stop[0]])
        y1, y2 = sorted([start[1], stop[1]])

        buffer[y1 : y2 + 1, x1 : x2 + 1] = self.currentColor

        if temp:
            self.tempMask[y1 : y2 + 1, x1 : x2 + 1] = True

    def line(self, start, stop, temp = False):
        if temp:
            self.clearTempBuffer()
            buffer = self.tempBuffer
        else:
            buffer = self.buffer
            self.broadcast({
                "line": {
                    "start": start,
                    "stop": stop
                }
            })

        steps = max(np.abs(np.array(start) - stop)) + 1
        points = np.round(np.linspace(start, stop, steps)).astype(int)

        buffer[points[:, 1], points[:, 0]] = self.currentColor

        if temp:
            self.tempMask[points[:, 1], points[:, 0]] = True

    def ellipse(self, start, stop, fill = False, temp = False):
        if temp:
            self.clearTempBuffer()
            buffer = self.tempBuffer
        else:
            buffer = self.buffer
            self.broadcast({
                "ellipse": {
                    "start": start,
                    "stop": stop,
                    "fill": fill
                }
            })

        x1, x2 = sorted([start[0], stop[0]])
        y1, y2 = sorted([start[1], stop[1]])

        rx = (x2 - x1) // 2
        ry = (y2 - y1) // 2
        cx = x1 + rx
        cy = y1 + ry

        rx2 = rx * rx
        ry2 = ry * ry

        x = 0
        y = ry

        dx = 2 * ry2 * x
        dy = 2 * rx2 * y

        def plot(px, py):
            if fill:
                # draw horizontal spans
                for fx in range(cx - px, cx + px + 1):
                    buffer[cy + py, fx] = self.currentColor
                    buffer[cy - py, fx] = self.currentColor
                    if temp:
                        self.tempMask[cy + py, fx] = True
                        self.tempMask[cy - py, fx] = True
            else:
                points = [
                    (cx + px, cy + py),
                    (cx - px, cy + py),
                    (cx + px, cy - py),
                    (cx - px, cy - py),
                ]
                for px_, py_ in points:
                    buffer[py_, px_] = self.currentColor
                    if temp:
                        self.tempMask[py_, px_] = True

        # --- Region 1 ---
        p1 = ry2 - rx2 * ry + 0.25 * rx2

        while dx < dy:
            plot(x, y)

            if p1 < 0:
                x += 1
                dx += 2 * ry2
                p1 += dx + ry2
            else:
                x += 1
                y -= 1
                dx += 2 * ry2
                dy -= 2 * rx2
                p1 += dx - dy + ry2

        # --- Region 2 ---
        p2 = (ry2 * (x + 0.5)**2 +
            rx2 * (y - 1)**2 -
            rx2 * ry2)

        while y >= 0:
            plot(x, y)

            if p2 > 0:
                y -= 1
                dy -= 2 * rx2
                p2 += rx2 - dy
            else:
                y -= 1
                x += 1
                dx += 2 * ry2
                dy -= 2 * rx2
                p2 += dx - dy + rx2

    def floodFill(self, point: tuple[int, int], color = None):
        targetColor = tuple(self.buffer[point])

        # Either current color, or if over network: provided color
        newColor = self.currentColor if not color else color

        self.broadcast({
            "fill": {
                "point": point,
                "color": self.currentColor
            }
        })

        if targetColor == newColor:
            return

        queue = deque() 
        queue.append(point)

        while queue:
            x, y = queue.popleft()
             
            if not self.onCanvas(x, y):
                continue
            
            if not tuple(self.buffer[y, x]) == targetColor:
                continue

            self.buffer[y, x] = newColor

            queue.append((x - 1, y))
            queue.append((x + 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))



    # def ellipse(self, start, stop, fill = False, temp = False):
    #     if temp:
    #         self.clearTempBuffer()
    #         buffer = self.tempBuffer
    #     else:
    #         buffer = self.buffer

    #     x1, x2 = sorted([start[0], stop[0]])
    #     y1, y2 = sorted([start[1], stop[1]])

    #     width = (x2 - x1) + 2
    #     height = (y2 - y1) + 2

    #     for x in range(width):
    #         for y in range(height):

    #             normalized = (
    #                 (2.0 * x / width) - 1.0,
    #                 1.0 - (2.0 * y / height)
    #             )

    #             value = normalized[0]**2 + normalized[1]**2

    #             if abs(value - 1.0) < 0.1:
    #                 buffer[y1 + y, x1 + x] = self.currentColor 
    #                 if temp:
    #                     self.tempMask[y1 + y, x1 + x] = True


    def clearTempBuffer(self):
        self.tempBuffer.fill(0)
        self.tempMask.fill(False)


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


    def onCanvas(self, x, y) -> bool:
        if 0 <= x * self.pixel_size < self.width and 0 <= y * self.pixel_size < self.height:
            return True
        else:
            return False

    def broadcast(self, action: dict):
        print(json.dumps(action))

    def wsListener(self):
        pass