from collections.abc import Callable
from tkinter import colorchooser
from PIL import Image, ImageTk
import tkinter as tk

class ColorBar(tk.Frame):
    def __init__(self, master, on_color_change: Callable[[tuple], None], *args, **kwargs):
        super().__init__(master = master, *args, **kwargs)

        self.callback = on_color_change

        self.configure(
            background = "lightgray",
            height = 64,
            relief = "raised",
            border = 2,
        )

        self.pack_propagate(False)

        # Primary + Secondary Colors

        self.wrapper = tk.Frame(
            master = self, 
            width = 36,
            height = 36,
            background = "#DFDFDF",
            relief = "sunken",
            border = 2
        )

        self.primaryColor = "black"
        self.secondaryColor = "white"

        self.primaryColorFrame = tk.Frame(
            master = self.wrapper,
            width = 12,
            height = 12,
            background = self.primaryColor,
            relief = "sunken",
            border = 1
        )
        
        self.secondaryColorFrame= tk.Frame(
            master = self.wrapper,
            width = 12,
            height = 12,
            background = self.secondaryColor,
            relief = "sunken",
            border = 1
        )
        
        self.secondaryColorFrame.place(relx = 0.6, rely = 0.6, anchor = "center")
        self.primaryColorFrame.place(relx = 0.4, rely = 0.4, anchor = "center")
        self.primaryColorFrame.lift()

        self.wrapper.pack(side = "left", padx = 10)

        # Bind to wrapper and children for proper hover and click event
        for widget in self.wrapper.winfo_children() + [self.wrapper]:
            widget.bind("<Enter>", lambda _: self.wrapper.configure(background = "lightgray"))
            widget.bind("<Leave>", lambda _: self.wrapper.configure(background = "#DFDFDF"))
            widget.bind("<Button-1>", lambda _: self.swapPrimarySecondary())

        # Custom color gradient buttom
        self.customColor = tk.Canvas(
            self,
            width = 32,
            height = 32,
            border = 2,
            relief = "sunken",
        )

        # Resize with PIL
        self.gradientButtonImage = Image.open("assets/gradient.png")
        self.gradientButtonImage = self.gradientButtonImage.resize((48, 48)) 
        self.gradientButtonImage = ImageTk.PhotoImage(self.gradientButtonImage)

        self.customColor.create_image(0, 0, anchor = "nw", image = self.gradientButtonImage)

        self.customColor.pack(
            anchor = "w",
            padx = 10,
            expand = True,
            side = "right",
        )

        self.customColor.bind(
            "<Button-1>",
            lambda _: self.setPrimaryColor(colorchooser.askcolor()[1])
        )

        # Presets

        self.presets = {
            "columns": 10 ,
            "rows": 2,
            "size": 16,
            "gap": 4,
            "colors": [
                ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "black", "gray"],
                ["darkred", "darkorange", "gold", "darkgreen", "darkblue", "purple2", "deeppink2", "white", "white", "white"]
            ]
        }

        for row in self.presets["colors"]:
            while len(row) < self.presets["columns"]:
                row.append("")

        self.presetFrame = tk.Frame(
            master = self,
            width = self.presets["columns"] * (self.presets["size"] + self.presets["gap"]),
            height = self.presets["rows"] * (self.presets["size"] + self.presets["gap"]),
            relief = "sunken",
            background = "lightgray"
        )

        self.presetFrame.pack(anchor = "w", side = "right")

        for x in range(self.presets["columns"]):
            for y in range(self.presets["rows"]):
                frame = tk.Frame(
                    master = self.presetFrame,
                    width = self.presets["size"],
                    height = self.presets["size"],
                    relief = "sunken",
                    border = 2,
                    background = self.presets["colors"][y][x] or "white",
                )

                frame.grid(
                    column = x,
                    row = y,
                    padx = self.presets["gap"] // 2,
                    pady = self.presets["gap"] // 2
                )

                # Note: lambda far freezing
                frame.bind(
                    "<Button-1>",
                    lambda _, x = x, y = y:
                    self.setPrimaryColor(self.presets["colors"][y][x])
                )

                frame.bind(
                    "<Shift-Button-1>",
                    lambda _, frame = frame, x = x, y = y:
                    (
                        frame.configure(background = self.primaryColor), # Buttom bg
                        self.setPresetColor((x, y))
                    )
                )

    def setPrimaryColor(self, color):
        self.primaryColor = color
        self.primaryColorFrame.configure(bg = color)
        self.callback(self.getColor())

    def setSecondaryColor(self, color):
        self.secondaryColor = color
        self.secondaryColorFrame.configure(bg = color)
    
    def setPresetColor(self, location: tuple[int, int]):
        self.presets["colors"][location[1]][location[0]] = self.primaryColor

    def swapPrimarySecondary(self):
        primary = self.primaryColor
        secondary = self.secondaryColor

        self.setPrimaryColor(secondary)
        self.setSecondaryColor(primary)

    def getColor(self):
        # Raw RGB 0..65535 to 0..255
        return tuple((color // 256 for color in self.master.winfo_rgb(self.primaryColor)))
