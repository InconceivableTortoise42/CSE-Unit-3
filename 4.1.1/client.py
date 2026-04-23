from PIL import Image, ImageTk 
from paint import Paint
import tkinter as tk
import subprocess
from tkinter import messagebox
import re

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paint - Multiplayer") 
        self.icon = tk.PhotoImage(file ='assets/icon.png')
        self.iconphoto(False, self.icon)

        self.resizable = True
        self.geometry("800x600")

        self.mainMenu = MainMenu(self)

        self.mainMenu.pack(expand = True, fill = "both")


        self.mainloop()

    def launchPaint(self, network: bool, wsUrl:str = "ws://localhost:8000"):
        self.mainMenu.destroy()

        self.paintScreen = Paint(master = self, network = network, wsUrl = wsUrl)

        self.paintScreen.pack(expand = True, fill = "both")

        self.bind("x", lambda _: self.paintScreen.colorBar.swapPrimarySecondary())

        self.configure(menu = MenuBar())

    def launchServer(self) -> str:
        command = 'start cmd /k "uvicorn main:app"'

        subprocess.Popen(command, shell=True)

        command = 'start cmd /k "./cloudflared.exe tunnel --url http://localhost:8000'
        
        process = subprocess.Popen(
            command,
            stdout = subprocess.PIPE,
            shell = True
        )
        
        print("Waiting for tunnel to create...")
        
        while True:
            if process.stdout:
                line = process.stdout.readline()

                if not line:
                    break
                    
                match = re.search(r"https://.*\.trycloudflare\.com", str(line))
                print(line)

                if match:
                    print("Found Match!")
                    return match.group(0)

            self.update()

        return "ws://localhost:8000"

class MenuBar(tk.Menu):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.configure(
            background = "darkgray",
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
    def __init__(self, master: App, *args, **kwargs):
        super().__init__(master = master)

        self.app: App = master

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
            command = lambda: self.app.launchPaint(False)
        )

        self.singlePlayer.pack(expand = True, pady = 5)

        self.multiPlayer= tk.Button(
            self.buttonWrapper,
            text = "Multi Player",
            command = self.networkScreen
        )

        self.multiPlayer.pack(expand = True, pady = 5)

        self.quitButton = tk.Button(
            self.buttonWrapper,
            text = "Quit",
            command = self.master.quit 
        )

        self.quitButton.pack(expand = True, pady = 5)

        self.buttonWrapper.pack(expand = True)

    def networkScreen(self):
        for child in self.winfo_children():
            child.destroy()

        self.hostRoomButton = tk.Button(self, text = "New Room", command = self.hostRoom)
        self.hostRoomButton.pack(expand = True, anchor = "s")

        self.orLabel = tk.Label(self, text = "OR", font = ("TKDefaultFont", 30))
        self.orLabel.pack(pady = 20)

        self.entryLabel = tk.Label(self, text = "Existing room websocket url:")
        self.entryLabel.pack()
        self.urlEntry = tk.Entry(self, width = 60)
        self.urlEntry.pack() 
        self.connectButton = tk.Button(self, text = "Connect", command = self.connect)
        self.connectButton.pack(expand = True, anchor = "n")

    def connect(self):
        self.app.launchPaint(wsUrl = self.urlEntry.get(), network = True)
        self.destroy()

    def hostRoom(self):
        self.tunnel = self.app.launchServer()
        self.showUrl = messagebox.showinfo("Websocket URL", f"Your Url: {self.tunnel}")
        self.app.launchPaint(network = True, wsUrl = self.tunnel)
        self.destroy()


if __name__ == "__main__":
    App()