import tkinter as tk
from tkinter import ttk

from interfaz.gui_info import FrameInfo
from interfaz.gui_campanas import FrameCampanas
from interfaz.gui_pantallas import FramePantallas
from interfaz.gui_index import FrameIndex

import tkinter.font as tkFont
from model.campanasDao import TablaDB




class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Pantallas")
        self.root.geometry('380x600')
        self.root.iconbitmap(r"interfaz\assets\TPico.ico")
        self.root.resizable(0,0)
        
        listaTablas = {
            "Campanas": TablaDB("campanas", ["campana"]),
            "Pantallas": TablaDB("pantallas", ["pantalla", "fk_campana"])
        }
        listaTablas["Campanas"].isExist()
        listaTablas["Pantallas"].isExist()
        
        # validacion de la existencia de las tablas y su guardado par su uso
        self.tablaCampanas = TablaDB("campanas", ["campana"])


        self.tablaPantallas = TablaDB("pantallas", ["pantalla", "fk_campana"])



        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        
        # Crear los frames
        self.pageInfo = FrameInfo(self.notebook)
        self.pageCampanas = FrameCampanas(self.notebook, listaTablas["Campanas"])
        self.pagePantallas = FramePantallas(self.notebook, listaTablas)
        self.pageIndex = FrameIndex(self.notebook, [self.tablaCampanas, self.tablaPantallas])
        
        
        self.notebook.add(self.pageIndex, text="Inicio")
        self.notebook.add(self.pageCampanas, text="Campañas")
        self.notebook.add(self.pagePantallas, text="Pantallas")
        self.notebook.add(self.pageInfo, text="Informacion")
        
        
        # Vincular el evento de cambio de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
        
    def on_tab_change(self, event):
        selected = self.notebook.index(self.notebook.select())
        if selected == 0: 
            self.pageIndex.actualziarIndex()
            
        if selected == 2:
            self.pagePantallas.actualziarCamapanas()
            


        
if __name__ == "__main__":
    root = tk.Tk()
    # Cambiar la fuente por defecto
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=10) 
    
    app = App(root)
    root.mainloop()

