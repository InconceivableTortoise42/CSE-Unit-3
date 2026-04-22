from __future__ import annotations  
from typing import TYPE_CHECKING
from point import Point
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
        app.line(app.lastPos, Point(event.x, event.y))
        app.lastPos = Point(event.x, event.y)

    def on_mouse_up(self, app: Paint, event):
        app.currentStroke.append((event.x, event.y))
        app.currentStroke = []
        
    def draw(self, app: Paint, x, y, color):
        if app.onCanvas(x, y):
            app.buffer[y, x] = color 

class Bucket(Tool):
    def on_mouse_down(self, app: Paint, event):
        app.fill(Point(event.x, event.y))

class Eraser(Tool):
    def on_mouse_down(self, app: Paint, event):
        self.erace(app, event.x, event.y)

    def on_mouse_drag(self, app: Paint, event):
        num_steps = max(np.abs(np.array((app.lastPos.x - event.x, app.lastPos.y - event.y)))) + 1
        points = np.round(np.linspace((app.lastPos.x, app.lastPos.y), (event.x, event.y), num_steps, retstep = False)).astype(int)

        app.lastPos = Point(event.x, event.y)

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
        self.start = Point(event.x, event.y)

    def on_mouse_drag(self, app: Paint, event):
        self.stop = Point(event.x, event.y)
        self.create_visual(app)

    def on_mouse_up(self, app: Paint, event):
        self.stop = Point(event.x, event.y)
        app.rect(self.start, self.stop)
        app.render()

    def create_visual(self, app: Paint):
        x1, x2 = sorted([self.start.x, self.stop.x])
        y1, y2 = sorted([self.start.y, self.stop.y])

        app.rect(Point(x1, y1), Point(x2, y2), temp = True)
        app.render()

class Line(Tool):
    def on_mouse_down(self, app: Paint, event):
        self.last = Point(event.x, event.y)

    def on_mouse_up(self, app: Paint, event):
        app.line(self.last, Point(event.x, event.y))
        app.render()

    def on_mouse_drag(self, app: Paint, event):
        app.line(self.last, Point(event.x, event.y), temp = True)
        app.render()

class CustomShape(Tool):
    def __init__(self):
        self.points: list[Point] = []

    def on_mouse_up(self, app: Paint, event):
        if self.points:
            app.line(self.points[-1], Point(event.x, event.y))
        self.points.append(Point(event.x, event.y))
        app.render()
    
    def on_mouse_move(self, app: Paint, event):
        if self.points:
            self.create_visual(app, Point(event.x, event.y))

    def on_enter(self, app: Paint):
        app.line(self.points[-1], self.points[0])
        self.points = []
        app.clearTempBuffer()
        app.render()
    
    def create_visual(self, app: Paint, mousePos: Point):
        app.line(self.points[-1], mousePos, temp = True)
        app.render()

class Ellipse(Tool):
    def __init__(self):
        self.visual = 0

    def on_mouse_down(self, app: Paint, event):
        self.start = Point(event.x, event.y)

    def on_mouse_drag(self, app: Paint, event):
        self.stop = Point(event.x, event.y)
        self.create_visual(app)

    def on_mouse_up(self, app: Paint, event):
        self.stop = Point(event.x, event.y)
        app.ellipse(self.start, self.stop)

    def create_visual(self, app: Paint):
        app.ellipse(self.start, self.stop, temp = True)