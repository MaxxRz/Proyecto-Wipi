import tkinter as tk
import threading
from tkinter import messagebox, ttk

from utils.config_ui import FONTS, MEDIDAS, COLORS

from utils.funciones import *
from interfaz.others_windows import LoadingWindow, changeDataConfig



class FrameIndex(tk.Frame):
    def __init__(self, root = None, tablasDB = None):
        super().__init__(root)
        self.root = root
        self.config(
            width=self.root.winfo_width(),
            height=self.root.winfo_height()
            )
        self.grid(row=0, column=0, sticky="nsew")
        
        #Variables
        self.windowConfig = None
        self.windowLoading = None
        #variable de lista de campanas checkbox
        self.chkListData = {
            "box": [],
            "data": [],
        }
        
        self.chkListArchivos = {
            "box": [],
            "data": [],
        }
                
    
        # tabla de BD campañas 
        self.tablaCampanas = tablasDB[0]
        self.tablaPantallas = tablasDB[1]
        
        
        # frames
        self.FrameChoicePantallas()
        self.FrameArchivos()
        self.FrameBtnEjecutar()
    

    #container donde mostrara la lista de campañas y se trabajaran
    def FrameChoicePantallas(self):
        
        # Label Contenedor
        lblFramePantallas = tk.LabelFrame(self, text="Selección de pantallas")
        lblFramePantallas.config(
            font=(FONTS["lblFrame"]),
            height=210,
        )
        lblFramePantallas.pack_propagate(False)
        lblFramePantallas.pack(padx=MEDIDAS["pad_GlobalX"],
                               pady=(MEDIDAS["pad_FrameTop"], 0),
                               fill=tk.X,)
        
        
        #Seccion top
        frameTop = tk.Frame(lblFramePantallas)
        frameTop.config(
            pady=MEDIDAS["pad_GlobalY"] / 2,
            padx=MEDIDAS["pad_GlobalX"] / 2,
        )
        frameTop.pack(fill=tk.X) 
        
        lblSelectCampana = tk.Label(frameTop, text="Elige la Campaña: ")
        lblSelectCampana.config(
            font=(FONTS["text"]),
            fg=COLORS["text"],
        )
        lblSelectCampana.pack(side=tk.LEFT)
        
        
        # combobox para la seleccion de la campaña
        cbBoxSelectCampana = ttk.Combobox(frameTop, state="readonly",
                values = self.tablaCampanas.obtenerColumna('campana'))
        cbBoxSelectCampana.config(
                    font=("",10))
        cbBoxSelectCampana.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        #un evento para saber que campaña seleccionan
        cbBoxSelectCampana.bind("<<ComboboxSelected>>", self.onSelectCampana)
        
        
        
        #Llamamos a la funcion contenedor Canva  donde le pasaremos el frame padre
        #la cual contiene el contenedor donde se mostrara el listado deseado
        #guardamos su retorno en una variable el cual nos dara un array con el frame contenedor de todo
        #y el canvas dodne se agregaran la lista
        canvaIndex = contenedorCanva(lblFramePantallas)
        
        
        lblInstrucciones = tk.Label(lblFramePantallas, text="* Seleccione las las opciones donde se transmitira.")
        lblInstrucciones.config(
            font=(FONTS["subText"]),
            fg=COLORS["subText"],
        )
        lblInstrucciones.pack(
            side=tk.LEFT,
            pady=(0, MEDIDAS["pad_GlobalY"] / 2),
            padx=MEDIDAS["pad_GlobalX"] / 2,
            )
        
        
        
        #### Creacion de variables
        #canvaContenido guarda el contedor para volver a cargar en un futuro
        self.canvaPadreIndex = canvaIndex[0]
        #guardamos el canvas en una variable self para usarla mas adelante
        self.canvaHijoIndex = canvaIndex[1]
        # guardamos el combobox en una variable para en un futuro actualizar
        self.cbBoxSelectCampana = cbBoxSelectCampana
       
            
    def FrameArchivos(self):
        # Label Contenedor
        lblFrameArchivos = tk.LabelFrame(self, text="Archivos a transmitir")
        lblFrameArchivos.config(
            font=(FONTS["lblFrame"]),
            height=250,
        )
        lblFrameArchivos.pack_propagate(False)

        lblFrameArchivos.pack(padx=MEDIDAS["pad_GlobalX"],
                               pady=MEDIDAS["pad_GlobalY"],
                               fill=tk.BOTH)

        #Seccion top
        frameTop = tk.Frame(lblFrameArchivos)
        frameTop.config(
            pady=MEDIDAS["pad_GlobalY"] / 2,
            padx=MEDIDAS["pad_GlobalX"] / 2,
            height=30,
        )
        frameTop.pack(fill=tk.BOTH) 
        
        lblArchivosText = tk.Label(frameTop, text="Botón para seleccionar los archivos.")
        lblArchivosText.config(
            font=(FONTS["text"]),
            fg=COLORS["text"],
        )
        lblArchivosText.pack(side=tk.LEFT)
        

        # combobox para la seleccion de la campaña
        btnSearchArchivo = tk.Button(frameTop, text="Buscar...", cursor="hand2", command=self.mostrarArchivos)
        btnSearchArchivo.config(
            width=10,
            height=1,
            pady=0,
        )
        btnSearchArchivo.pack(side=tk.RIGHT)

        canvaArchivos = contenedorCanva(lblFrameArchivos)
        
        
        btnConfigurar = tk.Button(lblFrameArchivos, text="Configuracion", command=lambda: self.windowsDataConfig(self.root))
        btnConfigurar.config(
            cursor="hand2",
        )
        btnConfigurar.pack(
            side="left",
            padx=MEDIDAS["pad_GlobalY"] / 2,
            pady=(0, MEDIDAS["pad_GlobalY"] / 2), )

        
        
        btnEliminar = tk.Button(lblFrameArchivos, text="Eliminar", command=self.borrarArchivos)
        btnEliminar.config(
            cursor="hand2",
            state=tk.DISABLED,
        )
        btnEliminar.pack(
            side="right",
            padx=MEDIDAS["pad_GlobalY"] / 2,
            pady=(0, MEDIDAS["pad_GlobalY"] / 2), )

        
        
        #### Creacion de variables
        #canvaContenido guarda el contedor para volver a cargar en un futuro
        self.canvaPadreArchivos = canvaArchivos[0]
        #guardamos el canvas en una variable self para usarla mas adelante
        self.canvaHijoArchivos = canvaArchivos[1]
        self.btnEliminar = btnEliminar
        

    def FrameBtnEjecutar(self):
        FrameBtnEjecutar = tk.Frame(self)
        FrameBtnEjecutar.config()
        FrameBtnEjecutar.pack(padx=MEDIDAS["pad_GlobalX"],
                              ipady=0,
                              ipadx=0,
                              fill=tk.BOTH)


        btnEjecutar = tk.Button(FrameBtnEjecutar, text="Aceptar", 
                                command=lambda:threading.Thread(target=self.ejecutarProceso).start())
        btnEjecutar.config(
            font=FONTS['lblFrame'],
            cursor="hand2",
        )
        btnEjecutar.pack(
            side="right",)


    #funcion la cual muestra el avance
    def ejecutarProceso(self):
        if self.chkListArchivos['data'] == None:
            print("no hay archivos")
            return        
        
        
        if self.windowLoading is None or not self.windowLoading.window.winfo_exists():
            self.windowLoading =  LoadingWindow(self.root)
            copilarArchivos(self.chkListArchivos['data'], self.windowLoading)
            self.windowLoading.update_status("¡Proceso completado!")
            self.windowLoading.finish()
        else:
            return


    def mostrarArchivos(self):
        archivos = obtenerArchivo();
        
        self.actualizarArchivos(archivos)
        
        #deshabilita el btn si no hay contenido
        if not archivos:
            self.btnEliminar['state'] = tk.DISABLED
        else:
            self.btnEliminar['state'] = tk.NORMAL
            

    ##### Funcion para borrar Archivos seleccionados
    def borrarArchivos(self): 
        if messagebox.askyesno(title="",message="Seguro que deseas eliminar las pantallas seleccionadas"):
        
            listaModificada = []
            
            #recorremos el listado de archivos de reversa
            #validamos si no es true y guardamos en un nuevo listado
            for i in reversed(range(len(self.chkListArchivos['data']))):
                if not(self.chkListArchivos['data'][i][1].get()):
                    listaModificada.append(self.chkListArchivos['data'][i][0])
            
            
            
            #destruimos los arrays para crearlos nuevamente modificados
            destruirListadoCanva(
                self.chkListArchivos['box'], 
                self.chkListArchivos['data'],) 
            
            self.actualizarArchivos(listaModificada[::-1])
                       
           
    def actualizarArchivos(self, archivos):
        # se pasa array con la ruta de los archivos
        for archivo in archivos:
            letra = archivo.rfind("/") + 1
            
            var = tk.BooleanVar()  # Variable para cada Checkbutton
        
            checkBtn = tk.Checkbutton(self.canvaPadreArchivos, text=archivo[letra:], variable=var)
            checkBtn.config(bg="white")
            checkBtn.pack(anchor="w")
            
            #guardamos el chkbox para mostrarlo
            self.chkListArchivos['box'].append(checkBtn)
            #guardamos y asociamos el chebox a la ruta completa
            self.chkListArchivos['data'].append((archivo, var))
        
        actualizarCanva(self.canvaPadreArchivos, self.canvaHijoArchivos)
        
        
    # funcion al seleccionar la campaña
    def onSelectCampana(self, event):
        self.campanaElegida = self.cbBoxSelectCampana.get()
        
        # obtenemos el listado a traves de peticion a la BD
        #for campana in  self.tablaCampanas.obtenerTodo():
        # funcion para mostrar las campañas
        self.mostrarPantallasLista(self.canvaPadreIndex,  self.tablaPantallas.obtenerColumnaRestriccion(self.campanaElegida))
    

    ##### funcion para mostrar la lista de pantallas segun la campaña seleccionada
    def mostrarPantallasLista(self, framePadre, listPantallas):    
            
        destruirListadoCanva(
            self.chkListData['box'], 
            self.chkListData['data'],)

        # modifica la lista de pantallas que aparecen
        for campana in listPantallas:

            var = tk.BooleanVar()  # Variable para cada Checkbutton
            # Guarda la campaña y su checkbox
            checkBtn = tk.Checkbutton(framePadre, text=campana, variable=var)
            checkBtn.config(bg="white")
            checkBtn.pack(anchor="w")
            
            self.chkListData['box'].append(checkBtn)
            self.chkListData['data'].append((campana, var))
        
        #modificar guardarlo en una funcion para actualizar la altura del contenido del list
        actualizarCanva(self.canvaPadreIndex,  self.canvaHijoIndex)
        
        
    ##### funcion para acutalizar la pestaña
    def actualziarIndex(self):
        self.cbBoxSelectCampana.config(values = self.tablaCampanas.obtenerColumna('campana') )
        self.cbBoxSelectCampana.set('')   
        
        destruirListadoCanva(
            self.chkListData['box'], 
            self.chkListData['data'],)  
        
        destruirListadoCanva(
            self.chkListArchivos['box'], 
            self.chkListArchivos['data'],)              


    ## funcion para validar si esta abierta la ventana config, si es asi no la abre 
    def windowsDataConfig(self,root):
        if self.windowConfig is None or not self.windowConfig.window.winfo_exists():
            self.windowConfig = changeDataConfig(root)
        else:
            return