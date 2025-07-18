import tkinter as tk

from utils.config_ui import MEDIDAS


class FrameInfo(tk.Frame):
    def __init__(self, root = None):
        super().__init__(root)
        self.root = root
        self.config()
        self.grid(row=0, column=0, sticky="nsew")
        
        # ----- LABELS 
        frameContainer = tk.Frame(self)
        frameContainer.pack(
            fill=tk.Y,
            expand=tk.TRUE,
            side=tk.BOTTOM)
        
        
        frameConteinerText = tk.Frame(frameContainer)
        frameConteinerText.pack(
            side=tk.BOTTOM,
            pady=MEDIDAS["pad_GlobalY"])
        
        
        
        lblNameApp = tk.Label(frameConteinerText, text="WIPI")
        lblNameApp.config(font=("Arial",14, "bold"))
        lblNameApp.pack()

        lblVersion = tk.Label(frameConteinerText, text="Version v2.0b")
        lblVersion.config()
        lblVersion.pack()
        
        lblDesarollador = tk.Label(frameConteinerText, text="Max Salas \ Teleperformance")
        lblDesarollador.config()
        lblDesarollador.pack()
        
        lblDescription = tk.Label(frameConteinerText, text="App enfocada en la visualizacion de presentaciones \nen pantallas remotas a traves de wifi")
        lblDescription.config(fg="#4a4a4a")
        lblDescription.pack()

