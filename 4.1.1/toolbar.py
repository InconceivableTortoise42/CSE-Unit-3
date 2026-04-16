from collections.abc import Callable
from PIL import Image, ImageTk
import tkinter as tk
from tools import *

class ToolBar(tk.Frame):
    def __init__(self, master, on_tool_change: Callable[[Tool], None],*args, **kwargs):
        super().__init__(master = master, *args, **kwargs)

        self.configure(
            background = "lightgray",
            width = 80,
            relief = "raised",
            border = 2
        )

        self.pack_propagate(False)

        self.callback = on_tool_change

        self.currentTool = "pencil"

        # 16 x 16 icons in a row scales to self.toolIconSize
        self.toolIconSize = 24
        self.toolCount = 16
        self.toolIconSheet = Image.open("assets/tools.png").resize((
                                        self.toolIconSize * self.toolCount,
                                        self.toolIconSize
                                        ))

        self.toolIcons = [] # Made so that images aren't garbage collected

        # Names in order of image
        self.tools = {
            "freeform-selection": Tool(),
            "rectangular-selection": Tool(),
            "eraser": Tool(),
            "paint-bucket": Bucket(),
            "eye-dropper": Tool(),
            "zoom": Tool(),
            "pencil": Pencil(),
            "brush": Tool(),
            "spray-can": Tool(),
            "type": Tool(),
            "line": Tool(),
            "curve": Tool(),
            "rectangle-shape": Tool(),
            "custom-shape": Tool(),
            "circle-shape": Tool(),
            "beveled-rectangle-shape": Tool()
        }

        self.wrapper = tk.Frame(self)

        i = 0 # Icon itterator
        
        for x in range(2):
            for y in range(8):
                frame = tk.Frame(
                    master = self.wrapper,
                    relief = "raised",
                    border = 2,
                    name = list(self.tools)[i]
                )

                self.toolIcons.append(
                    ImageTk.PhotoImage(
                        self.toolIconSheet.crop((
                            i * self.toolIconSize,
                            0,
                            i * self.toolIconSize + self.toolIconSize,
                            self.toolIconSize
                        ))
                    )
                )

                # Label for image
                tk.Label(
                    frame,
                    image = self.toolIcons[-1]).pack()

                frame.grid(
                    column = x,
                    row = y
                )

                # Bind click to label and not frame
                for widget in frame.winfo_children():
                    widget.bind("<Button-1>", lambda _, name = list(self.tools)[i]: self.setTool(name))

                i -=- 1 # Lol
            

        self.wrapper.pack(anchor = "n", expand = True, pady = 5)

        # Set relief of current tool initially
        self.setTool("pencil")

    def setTool(self, toolName: str):

        # Reset style of current
        self.wrapper.nametowidget(
            self.currentTool
        ).configure(
            relief = "raised"
        )

        # Set new tool and style 
        self.currentTool = toolName

        self.wrapper.nametowidget(
            toolName
        ).configure(
            relief = "sunken"
        )

        # Paint callback
        self.callback(self.tools[self.currentTool])

    def getTool(self) -> Tool:
        return self.tools[self.currentTool]
