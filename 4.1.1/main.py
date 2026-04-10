import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paint - Multiplayer") 
        self.icon = tk.PhotoImage(file='icon.png')
        self.iconphoto(False, self.icon)

        self.resizable = True
        self.geometry("800x600")

        self.paintScreen = Paint(self)

        self.paintScreen.pack(expand = True, fill = "both")

        self.bind("x", lambda _: self.paintScreen.colorBar.swapPrimarySecondary())

        self.mainloop()


class Menu(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__()


class Paint(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(background = "gray")

        self.colorBar = ColorBar(self)
        self.colorBar.pack(side = "bottom", fill = "x")

        self.toolBar = ToolBar(self)
        self.toolBar.pack(side = "left", fill = "y")

        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand = True)



class ColorBar(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(
            background = "lightgray",
            height = 50,
            relief = "raised",
            border = 2,
        )

        self.pack_propagate(False)

        # Primary + Secondary Colors

        self.wrapper = tk.Frame(master = self)

        self.primaryColor = "black"
        self.secondaryColor = "white"

        self.primaryColorFrame = tk.Frame(
            master = self.wrapper,
            width = 30,
            height = 30,
            background = self.primaryColor,
            relief = "sunken",
            border = 2
        )
        
        self.primaryColorFrame.pack(anchor = "w", side = "left")
        
        self.secondaryColorFrame= tk.Frame(
            master = self.wrapper,
            width = 30,
            height = 30,
            background = self.secondaryColor,
            relief = "sunken",
            border = 2
        )
        
        self.secondaryColorFrame.pack(anchor = "w", side = "right")

        self.wrapper.pack(side = "left", padx = 10)

        # Presets

        self.presets = {
            "columns": 7,
            "rows": 2,
            "size": 15,
            "gap": 5,
            "colors": [
                ["red", "orange", "yellow", "green", "blue", "purple", "pink"],
                ["brown", "black", "white", "gray", "", "", ""]
            ]
        }

        self.presetFrame = tk.Frame(
            master = self,
            width = self.presets["columns"] * (self.presets["size"] + self.presets["gap"]),
            height = self.presets["rows"] * (self.presets["size"] + self.presets["gap"]),
            relief = "sunken"
        )

        self.presetFrame.pack(anchor = "w", expand = True, side = "right")

        for x in range(self.presets["columns"]):
            for y in range(self.presets["rows"]):
                frame = tk.Frame(
                    master = self.presetFrame,
                    width = self.presets["size"],
                    height = self.presets["size"],
                    relief = "sunken",
                    border = 2,
                    background = self.presets["colors"][y][x] or "black",
                )

                frame.grid(
                    column = x,
                    row = y,
                    padx = self.presets["gap"] // 2,
                    pady = self.presets["gap"] // 2
                )

                # Color var frozen for correct binding
                frame.bind("<Button-1>", lambda _, color = frame["background"]: self.setPrimaryColor(color))

    def setPrimaryColor(self, color):
        self.primaryColor = color
        self.primaryColorFrame.configure(bg = color)

    def setSecondaryColor(self, color):
        self.secondaryColor = color
        self.secondaryColorFrame.configure(bg = color)

    def swapPrimarySecondary(self):
        primary = self.primaryColor
        secondary = self.secondaryColor

        self.setPrimaryColor(secondary)
        self.setSecondaryColor(primary)


class ToolBar(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(
            background = "lightgray",
            width = 50,
            relief = "raised",
            border = 2
        )


if __name__ == "__main__":
    App()