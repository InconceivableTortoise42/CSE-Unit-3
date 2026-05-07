from PIL import Image, ImageTk 
from tkinter import messagebox
from typing import Callable
from paint import Paint
from tkinter import ttk
import tkinter as tk
from main import app
import subprocess
import threading
import uvicorn
import sys
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
    
    def save(self):
        if self.paintScreen:
            self.paintScreen.save()

    def launchPaint(self, network: bool, wsUrl: str = "ws://localhost:8000"):
        self.mainMenu.destroy()

        self.paintScreen = Paint(master = self, network = network, wsUrl = wsUrl)

        self.paintScreen.pack(expand = True, fill = "both")

        self.bind("x", lambda _: self.paintScreen.colorBar.swapPrimarySecondary())

        self.configure(menu = MenuBar(self, network))
    
    def copyTunnelUrl(self):
        if self.tunnelUrl:
            self.clipboard_clear()
            self.clipboard_append(self.tunnelUrl)
            self.update()

    def runUvicorn(self):
        self.serverProcess = subprocess.Popen([
            sys.executable,
            "-m", "uvicorn",
            "main:app",
            "--host", "127.0.0.1",
            "--port", "8000"
        ])

    def launchServer(self, on_tunnel_ready: Callable[[str], None]) -> None:

        # Server
        self.runUvicorn()

        # Tunnel

        self.tunnelProcess = subprocess.Popen(
            ["./cloudflared.exe", "tunnel", "--url", "http://localhost:8000", "--protocol", "http2"],
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            text = True
        )

        self.tunnelUrl = None

        # Stdout Thread
        def readOutput():
            for line in self.tunnelProcess.stdout: # type: ignore
                match = re.search(r"https://.*\.trycloudflare\.com", line)
                if match:
                    self.tunnelUrl = match.group(0).replace("https://", "wss://")
                    break

        threading.Thread(target = readOutput, daemon = True).start() 

        # Loader
        self.loadingWindow = tk.Toplevel(self)
        self.loadingWindow.title("Starting server...")
        
        self.loader = ttk.Progressbar(self.loadingWindow, mode = "indeterminate", length = 300)
        self.loader.pack(padx = 20, pady = 20)
        self.loader.start()

        # Polling

        def poll():
            if self.tunnelUrl:
                self.loader.stop()
                self.loadingWindow.destroy()
                on_tunnel_ready(self.tunnelUrl)
            else:
                self.after(100, poll)

        poll()


class MenuBar(tk.Menu):
    def __init__(self, master: App, network: bool, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(
            background = "darkgray",
            relief = "raised",
            border = 2
        )

        # Sub Menus
        self.fileMenu = tk.Menu(self, tearoff = False)
        self.fileMenu.add_command(label = "New")
        self.fileMenu.add_command(label = "Save", command = master.save)
        if network:
            self.fileMenu.add_command(label = "Copy join link.", command = master.copyTunnelUrl)
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
        self.app.launchServer(self.tunnelReady)

    def tunnelReady(self, tunnelUrl: str):
        self.showUrl = messagebox.showinfo("Websocket URL", f"Your Url: {tunnelUrl}")
        print(tunnelUrl)
        self.app.launchPaint(network = True, wsUrl = tunnelUrl)
        self.destroy()

if __name__ == "__main__":
    App()