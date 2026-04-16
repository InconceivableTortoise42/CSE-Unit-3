from __future__ import annotations  
from typing import TYPE_CHECKING
from collections import deque
from threading import Thread
import numpy as np

if TYPE_CHECKING:
    from paint import Paint

class Tool:
    def on_mouse_down(self, app: Paint, event):
        pass

    def on_mouse_drag(self, app: Paint, event):
        pass

    def on_mouse_up(self, app: Paint, event):
        pass

class Pencil(Tool):
    def __init__(self) -> None:
        pass

    def on_mouse_down(self, app: Paint, event):
        pass

    def on_mouse_drag(self, app: Paint, event):
        num_steps = max(np.abs(np.array(app.lastPos) - (event.x, event.y))) + 1
        points = np.round(np.linspace(app.lastPos, (event.x, event.y), num_steps)).astype(int)

        app.lastPos = (event.x, event.y)

        for point in points:
            self.draw(app, point[0], point[1], app.currentColor)
            app.currentStroke.append((int(point[0]), int(point[1])))

    def on_mouse_up(self, app: Paint, event):
        app.currentStroke.append((event.x, event.y))
        app.currentStroke = []

    def draw(self, app: Paint, x, y, color):
        if app.onCanvas(x, y):
            app.buffer[y - 1 : y + 2, x - 1 : x + 2] = color 

class Bucket(Tool):
    def __init__(self) -> None:
        pass

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


    def on_mouse_drag(self, app, event):
        pass

    def on_mouse_up(self, app, event):
        pass
