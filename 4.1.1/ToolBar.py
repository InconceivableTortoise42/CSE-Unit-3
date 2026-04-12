from PIL import Image, ImageTk
import tkinter as tk

class ToolBar(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(
            background = "lightgray",
            width = 80,
            relief = "raised",
            border = 2
        )

        self.pack_propagate(False)

        self.currentTool = "pencil"

        # 16 x 16 icons in a row scales to self.toolIconSize
        self.toolIconSize = 24
        self.toolCount = 16
        self.toolIconSheet = Image.open("tools.png").resize((
                                        self.toolIconSize * self.toolCount,
                                        self.toolIconSize
                                        ))

        self.toolIcons = [] # Made so that images aren't garbage collected

        # Names in order of image
        self.toolNames = [
            "freeform-selection",
            "rectangular-selection",
            "eraser",
            "paint-bucket",
            "eye-dropper",
            "zoom",
            "pencil",
            "brush",
            "spray-can",
            "type",
            "line",
            "curve",
            "rectangle-shape",
            "custom-shape",
            "circle-shape",
            "beveled-rectangle-shape"
        ]

        self.wrapper = tk.Frame(self)

        i = 0 # Icon itterator
        
        for x in range(2):
            for y in range(8):
                frame = tk.Frame(
                    master = self.wrapper,
                    relief = "raised",
                    border = 2,
                    name = self.toolNames[i]
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

                i -=- 1 # Lol
            

        self.wrapper.pack(anchor = "n", expand = True, pady = 5)

        # Set relief of current tool initially
        self.wrapper.nametowidget(
            self.currentTool
        ).configure(
            relief = "sunken"
        )

