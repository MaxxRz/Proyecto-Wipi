import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from utils.config_ui import FONTS, MEDIDAS, COLORS
from utils.funciones import obtenerConfig

import os
import json

class LoadingWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Cargando...")
        self.window.geometry("300x200")
        self.window.iconbitmap(r"interfaz\assets\TPico.ico")
        self.window.resizable(False, False)
        
        # Imagen de carga
        runtaImg = os.path.join(os.getcwd(), r"interfaz\assets\tplogo.png")
        image = Image.open(runtaImg)  # Asegúrate de tener una imagen en el mismo directorio
        image = image.resize((64, 64))
        self.photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(self.window, image=self.photo)
        image_label.pack(pady=10)

        # Mensaje de estado
        self.status_label = tk.Label(self.window, text="Preparando...", font=("Arial", 12))
        self.status_label.pack(pady=5)

        # Barra de progreso opcional
        self.progress = ttk.Progressbar(self.window, mode='indeterminate')
        self.progress.pack(pady=10, fill='x', padx=20)
        self.progress.start(10)

        # Cuando se cierra la ventana, se notifica al MainWindow
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
        

    def update_status(self, message):
        self.status_label.config(text=message)
        self.window.update_idletasks()

    def finish(self):
        self.status_label.config(text="Proceso Terminado")
        self.progress.destroy()
        
        self.btnFinish = tk.Button(self.window, text="cerrar", command=lambda: self.close())
        self.btnFinish.pack(pady=10, fill='x', padx=20)
        
    def close(self):
        self.window.destroy()
    

class changeDataConfig():
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Configuración")
        self.window.iconbitmap(r"interfaz\assets\TPico.ico")
        self.window.resizable(0,0)
        
        ancho = 250
        self.dataConfig = obtenerConfig()
        fpsValues = ["3 fps",
                    "15 fps",
                    "24 fps",
                    "30 fps",
                    ]
        
        
        lblFrameConfig = tk.LabelFrame(self.window)
        lblFrameConfig.config(
            font=(FONTS["lblFrame"]),
        )
        
        lblFrameConfig.pack(padx=MEDIDAS["pad_GlobalX"] / 2,
                            pady=MEDIDAS["pad_GlobalY"] / 2,
                            fill="x"
                            )
        

        lblFps = tk.Label(lblFrameConfig, text="Fps:")
        lblFps.pack(anchor="w",
                    padx=MEDIDAS["pad_GlobalX"] / 2,
                    pady=(MEDIDAS["pad_GlobalY"] / 2,0))
        
        
        self.cbBoxSelectFps = ttk.Combobox(lblFrameConfig, state="readonly",
                values = fpsValues)   
        
        for i, value in enumerate(fpsValues):
            if int(value[:-4]) == int(self.dataConfig["fps"]):
                self.cbBoxSelectFps.current(i)
                break        
        
        self.cbBoxSelectFps.config(font=("",10))
        self.cbBoxSelectFps.pack(fill="x", expand=True,
                            padx=MEDIDAS["pad_GlobalX"] / 2,)
        
        
        
        lblDuracion = tk.Label(lblFrameConfig, text="Duración por imagen (seg):")
        lblDuracion.pack(anchor="w",
                         padx=MEDIDAS["pad_GlobalX"] / 2,
                         pady=(MEDIDAS["pad_GlobalY"] / 2,0))

        # combobox para la seleccion de la campaña
        self.entryDuracion = tk.Entry(lblFrameConfig)
        self.entryDuracion.pack(fill="x", expand=True,
                            padx=MEDIDAS["pad_GlobalX"] / 2,)
        self.entryDuracion.insert(0,self.dataConfig["duracion_por_imagen"])
        
        btnGuardar = tk.Button(lblFrameConfig, text="Guardar", command=self.guardarConfiguracion)
        btnGuardar.config(cursor="hand2")
        btnGuardar.pack(side="right",
                        pady=MEDIDAS["pad_GlobalY"] / 2,
                        padx=(0,MEDIDAS["pad_GlobalX"] / 2))


        self.window.update_idletasks()
        
        # Cuando se cierra la ventana, se notifica al MainWindow
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)

    
    def guardarConfiguracion(self):
        num = 0
        
        # obtenemos el primer dato y validamos si hay modificacion
        if not int(self.cbBoxSelectFps.get()[:-4]) == self.dataConfig['fps']:
            self.dataConfig['fps'] = int(self.cbBoxSelectFps.get()[:-4])
        else:
            num = 1
        # obtenemos el segundo dato y validamos si hay modificacion
        if not int(self.entryDuracion.get()) == self.dataConfig['duracion_por_imagen']:
             self.dataConfig['duracion_por_imagen'] = int(self.entryDuracion.get())
        else:
            num += 1 
        
        # si no hay modificacion no guarda nada
        if num == 2:
            return  
            
        rutaArchivo = os.path.join(os.getcwd(), f"utils\config.json")
        
        # guarda lo modificado
        with open(rutaArchivo, "w") as file:
            json.dump([self.dataConfig], file, indent=4)
                
        
        
        
        









        