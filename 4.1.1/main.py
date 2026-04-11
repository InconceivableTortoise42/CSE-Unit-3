from tkinter import colorchooser
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paint - Multiplayer") 
        self.icon = tk.PhotoImage(file ='icon.png')
        self.iconphoto(False, self.icon)

        self.resizable = True
        self.geometry("800x600")

        self.configure(menu = MenuBar())

        self.paintScreen = Paint(self)

        self.paintScreen.pack(expand = True, fill = "both")

        self.bind("x", lambda _: self.paintScreen.colorBar.swapPrimarySecondary())

        self.mainloop()

class MenuBar(tk.Menu):
    def __init__(self, *args, **kwargs):
        super().__init__()

        # Sub Menus
        self.fileMenu = tk.Menu(self, tearoff = False)
        self.fileMenu.add_command(label = "New")
        self.fileMenu.add_command(label = "Open")
        self.fileMenu.add_command(label = "Save")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "Exit", command = self.master.quit)

        # Adding Submenus to Menubar
        self.add_cascade(label = "File", menu = self.fileMenu)

class MainMenu(tk.Frame):
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
        self.canvas.pack(expand = True, anchor = "nw")



class ColorBar(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
            width = 15,
            height = 15,
            background = self.primaryColor,
            relief = "sunken",
            border = 1
        )
        
        self.secondaryColorFrame= tk.Frame(
            master = self.wrapper,
            width = 15,
            height = 15,
            background = self.secondaryColor,
            relief = "sunken",
            border = 1
        )
        
        self.secondaryColorFrame.place(x = 12, y = 12)
        self.primaryColorFrame.place(x = 5, y = 5)
        self.primaryColorFrame.lift()

        self.wrapper.pack(side = "left", padx = 10)

        # Bind to wrapper and children for proper hover and click event
        for widget in self.wrapper.winfo_children() + [self.wrapper]:
            widget.bind("<Enter>", lambda _: self.wrapper.configure(background = "lightgray"))
            widget.bind("<Leave>", lambda _: self.wrapper.configure(background = "#DFDFDF"))
            widget.bind("<Button-1>", lambda _: self.swapPrimarySecondary())

        # Custom color gradient buttom
        from PIL import Image, ImageTk

        self.customColor = tk.Canvas(
            self,
            width = 36,
            height = 36,
            border = 2,
            relief = "sunken"
        )

        # Resize with PIL
        self.gradientButtonImage = Image.open("gradient.png")
        self.gradientButtonImage = self.gradientButtonImage.resize((36, 36)) 
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
                ["darkred", "darkorange", "gold", "darkgreen", "darkblue", "purple2", "deeppink2"]
            ]
        }

        for row in self.presets["colors"]:
            while len(row) < self.presets["columns"]:
                row.append("")

        self.presetFrame = tk.Frame(
            master = self,
            width = self.presets["columns"] * (self.presets["size"] + self.presets["gap"]),
            height = self.presets["rows"] * (self.presets["size"] + self.presets["gap"]),
            relief = "sunken"
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


class ToolBar(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(
            background = "lightgray",
            width = 64,
            relief = "raised",
            border = 2
        )

        self.toolIcons = tk.PhotoImage("tools.png")

        self.toolsNames = [
            "Freeform Selection",
            "Rectangular Selection",
            "Eraser",
            "Paint Bucket",
            "Eye Dropper",
            "Zoom",
            "Pencil",
            "Brush",
            "Spray Can",
            "Type",
            "Line",
            "Curve",
            "Rectangle Shape",
            "Custom Shape",
            "Circle Shape",
            "Beveled Rectangle Shape"
        ]

        # TODO Use photoimage subsection for individual icons
        


if __name__ == "__main__":
    App()