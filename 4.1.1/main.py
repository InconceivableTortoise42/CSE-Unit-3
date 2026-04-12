from PIL import Image, ImageTk
from ColorBar import ColorBar
from ToolBar import ToolBar
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

        self.configure(
            background = "lightgray",
            relief = "raised",
            border = 2
        )

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


if __name__ == "__main__":
    App()