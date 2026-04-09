import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.iconbitmap("icon.ico")
        self.title("Paint - Multiplayer") 
        self.resizable = True
        self.geometry("800x600")

        self.paintScreen = Paint()

        self.paintScreen.pack(expand = True, fill = "both")

        self.mainloop()


class Menu(tk.Frame):
    def __init__(self):
        super().__init__()


class Paint(tk.Frame):
    def __init__(self):
        super().__init__()

        self.configure(background = "gray")

        self.colorBar = ColorBar()
        self.colorBar.pack(side = "bottom", fill = "x")

        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand = True)


class ColorBar(tk.Frame):
    def __init__(self):
        super().__init__()

        self.configure(
            background = "lightgray",
            height = 40,
            relief = "raised",
            border = 2
        )

class ToolBar(tk.Frame):
    def __init__(self):
        super().__init__()

        self.configure(
            background = "lightgray",
            height = 40,
            relief = "raised",
            border = 2
        )


class ColorPicker(tk.Toplevel):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    App()