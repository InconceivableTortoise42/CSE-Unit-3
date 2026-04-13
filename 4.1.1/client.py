from PIL import Image, ImageTk
from ColorBar import ColorBar
from ToolBar import ToolBar
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paint - Multiplayer") 
        self.icon = tk.PhotoImage(file ='assets/icon.png')
        self.iconphoto(False, self.icon)

        self.resizable = True
        self.geometry("800x600")

        self.mainMenu= MainMenu(self)

        self.mainMenu.pack(expand = True, fill = "both")

        # self.configure(menu = MenuBar())

        # self.paintScreen = Paint(self)

        # self.paintScreen.pack(expand = True, fill = "both")

        # self.bind("x", lambda _: self.paintScreen.colorBar.swapPrimarySecondary())

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

        self.configure(background = "#FEFEFE")

        self.logoSize = (430, 255)
        self.logoImage = ImageTk.PhotoImage(Image.open("assets/logo.png").resize((self.logoSize[0], self.logoSize[1])))

        self.logo = tk.Label(
            self,
            image = self.logoImage,
            width = self.logoSize[0],
            height = self.logoSize[1]
        )
        
        self.logo.pack(expand = True)

        self.buttonWrapper = tk.Frame(self, background = "#FEFEFE")

        self.singlePlayer = tk.Button(
            self.buttonWrapper,
            text = "Single Player",
            command = lambda: print("Simgle Player")
        )

        self.singlePlayer.pack(expand = True, pady = 5)

        self.multiPlayer= tk.Button(
            self.buttonWrapper,
            text = "Multi Player",
            command = lambda: print("Multi Player")
        )

        self.multiPlayer.pack(expand = True, pady = 5)

        self.quitButton = tk.Button(
            self.buttonWrapper,
            text = "Quit",
            command = self.master.quit 
        )

        self.quitButton.pack(expand = True, pady = 5)

        self.buttonWrapper.pack(expand = True)


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