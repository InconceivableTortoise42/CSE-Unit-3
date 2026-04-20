from __future__ import annotations  
from typing import TYPE_CHECKING
from collections import deque
from threading import Thread
import numpy as np

if TYPE_CHECKING:
    from paint import Paint

class Tool:
    def on_mouse_move(self, app: Paint, event):
        pass

    def on_mouse_down(self, app: Paint, event):
        pass

    def on_mouse_drag(self, app: Paint, event):
        pass

    def on_mouse_up(self, app: Paint, event):
        pass

    def on_enter(self, app: Paint):
        pass

class Pencil(Tool):
    def on_mouse_down(self, app: Paint, event):
        self.draw(app, event.x, event.y, app.currentColor)

    def on_mouse_drag(self, app: Paint, event):
        app.line(app.lastPos, (event.x, event.y))
        app.lastPos = (event.x, event.y)


    def on_mouse_up(self, app: Paint, event):
        app.currentStroke.append((event.x, event.y))
        app.currentStroke = []
        
    def draw(self, app: Paint, x, y, color):
        if app.onCanvas(x, y):
            app.buffer[y, x] = color 

class Bucket(Tool):
    def on_mouse_down(self, app: Paint, event):
        targetColor = tuple(app.buffer[event.y, event.x])
        newColor = app.currentColor

        if targetColor == newColor:
            return

        queue = deque() 
        queue.append((event.x, event.y))

        while queue:
            x, y = queue.popleft()
             
            if not app.onCanvas(x, y):
                continue
            
            if not tuple(app.buffer[y, x]) == targetColor:
                continue

            app.buffer[y, x] = newColor

            queue.append((x - 1, y))
            queue.append((x + 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))

class Eraser(Tool):
    def on_mouse_down(self, app: Paint, event):
        self.erace(app, event.x, event.y)

    def on_mouse_drag(self, app: Paint, event):
        num_steps = max(np.abs(np.array(app.lastPos) - (event.x, event.y))) + 1
        points = np.round(np.linspace(app.lastPos, (event.x, event.y), num_steps)).astype(int)

        app.lastPos = (event.x, event.y)

        for point in points:
            self.erace(app, point[0], point[1])
            app.currentStroke.append((int(point[0]), int(point[1])))

    def on_mouse_up(self, app: Paint, event):
        app.currentStroke.append((event.x, event.y))
        app.currentStroke = []
        
    def erace(self, app: Paint, x, y):
        if app.onCanvas(x, y):
            app.buffer[y, x] = (255, 255, 255)


class Eyedropper(Tool):
    def on_mouse_down(self, app: Paint, event):
        app.colorBar.setPrimaryColor(
            '#{:02x}{:02x}{:02x}'.format(*
            tuple(app.buffer[event.y, event.x]
        )))

class Rectangle(Tool):
    def __init__(self):
        self.visual = 0

    def on_mouse_down(self, app: Paint, event):
        self.start = (event.x, event.y)

    def on_mouse_drag(self, app: Paint, event):
        self.stop = (event.x, event.y)
        self.create_visual(app)

    def on_mouse_up(self, app: Paint, event):
        self.stop = (event.x, event.y)
        app.rect(self.start, self.stop)

        if self.visual:
            app.canvas.delete(self.visual)

    def create_visual(self, app: Paint):
        if self.visual:
            app.canvas.delete(self.visual)

        x1, x2 = sorted([self.start[0], self.stop[0]])
        y1, y2 = sorted([self.start[1], self.stop[1]])

        self.visual = app.canvas.create_rectangle(
            x1 * app.pixel_size,
            y1 * app.pixel_size,
            (x2 + 1) * app.pixel_size,
            (y2 + 1) * app.pixel_size,
            fill = '#{:02x}{:02x}{:02x}'.format(*app.currentColor), # RGB 2 HEX
            outline = ""
        )   

class Line(Tool):
    def __init__(self) -> None:
        self.visual = 0

    def on_mouse_down(self, app: Paint, event):
        self.last = (event.x, event.y)

    def on_mouse_up(self, app: Paint, event):
        app.line(self.last, (event.x, event.y))
        app.canvas.delete(self.visual)

    def on_mouse_drag(self, app: Paint, event):
        if self.visual:
            app.canvas.delete(self.visual)

        self.visual = app.canvas.create_line(
            self.last[0] * app.pixel_size,
            self.last[1] * app.pixel_size,
            event.x * app.pixel_size,
            event.y * app.pixel_size,
            fill = '#{:02x}{:02x}{:02x}'.format(*app.currentColor) # RGB 2 HEX
        )

class CustomShape(Tool):
    def __init__(self):
        self.points = []
        self.visual = 0

    def on_mouse_up(self, app: Paint, event):
        if self.points:
            app.line(self.points[-1], (event.x, event.y))
        self.points.append((event.x, event.y))
        app.render()
    
    def on_mouse_move(self, app: Paint, event):
        if self.points:
            self.create_visual(app, (event.x, event.y))

    def on_enter(self, app: Paint):
        app.line(self.points[-1], self.points[0])
        self.points = []
        app.canvas.delete(self.visual)
        app.render()
    
    def create_visual(self, app: Paint, mousePos):
        if self.visual:
            app.canvas.delete(self.visual)

        self.visual = app.canvas.create_line(
            self.points[-1][0] * app.pixel_size,
            self.points[-1][1] * app.pixel_size,
            mousePos[0] * app.pixel_size,
            mousePos[1] * app.pixel_size,
            fill = '#{:02x}{:02x}{:02x}'.format(*app.currentColor) # RGB 2 HEX
        )