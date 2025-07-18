import tkinter as tk
import ipaddress
from tkinter import messagebox, ttk

from utils.config_ui import FONTS, MEDIDAS, COLORS
from utils.funciones import actualizarCanva, destruirListadoCanva, contenedorCanva


class FramePantallas(tk.Frame):
    def __init__(self, root = None, tablasDB = None):
        super().__init__(root)
        self.root = root
        self.config(
            width=self.root.winfo_width(),
            height=self.root.winfo_height(),
            )
        self.grid(row=0, column=0, sticky="nsew")
        
        #Variables
        #variable de lista de campanas checkbox
        self.chkListData = {
            "box": [],
            "data": [],
        }
               
    
        # tabla de BD campañas 
        self.tablaCampanas = tablasDB["Campanas"]
        self.tablaPantallas = tablasDB["Pantallas"]
        
        
        # frames
        self.listaPantallas()
        self.nuevaPantalla()
    

    ## Container donde mostrara la lista de campañas y se trabajaran
    def listaPantallas(self):
        
        # Label Contenedor
        lblFramePantallas = tk.LabelFrame(self, text="Pantallas")
        lblFramePantallas.config(
            font=(FONTS["lblFrame"]),
            height=250,
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
        
               
        #funcion para crear canva. Nos regresa el padre y el hijo del canva para actualizar su uso
        canvaPantallas = contenedorCanva(lblFramePantallas)
        
               
        #Btn Eliminar Campaña
        btnEliminarCam = tk.Button(lblFramePantallas, text="Eliminar", 
            command= self.borrarPantalla)
        btnEliminarCam.config(
            cursor="hand2",
            state=tk.DISABLED,
        )
        btnEliminarCam.pack(
            side="right",
            padx=MEDIDAS["pad_GlobalY"] / 2,
            pady=(0, MEDIDAS["pad_GlobalY"] / 2), )




        #### Creacion de variables
        #canvaContenido guarda el contedor para volver a cargar en un futuro
        self.canvaPadrePantallas = canvaPantallas[0]
        #guardamos el canvas en una variable self para usarla mas adelante
        self.canvaHijoPantallas = canvaPantallas[1]
        # guardamos el combobox en una variable para en un futuro actualizar
        self.cbBoxSelectCampana = cbBoxSelectCampana
        #Guardar btn en una variable para usarla despues
        self.btnEliminarCam = btnEliminarCam        
        
                               

    ## Frame donde se agregaran nuevas pantallas
    def nuevaPantalla(self):
        # Label Contenedor
        lblFrameNuevaPan = tk.LabelFrame(self, text="Agregar")
        lblFrameNuevaPan.config(
            font=(FONTS["lblFrame"]),
            height=200,
        )
        lblFrameNuevaPan.pack(padx=MEDIDAS["pad_GlobalX"],
                               pady=MEDIDAS["pad_GlobalY"],
                               fill=tk.X)
        
        lblEtryNuevaPan = tk.Label(lblFrameNuevaPan, text="Ingresa la dirección IP que desea agregar:")
        lblEtryNuevaPan.config(
            font=FONTS["text"],
            fg=COLORS["text"],
            anchor="w"
            )
        lblEtryNuevaPan.pack(padx=MEDIDAS["pad_GlobalX"] / 2,
                             pady=(MEDIDAS["pad_GlobalY"] / 2, 0 ),
                             fill=tk.X)
        
        etryNuevaPan = tk.Entry(lblFrameNuevaPan)
        etryNuevaPan.config(
                    font=FONTS["text"])
        etryNuevaPan.pack(fill="x", 
                    expand=True,
                    ipady=2,
                    padx=MEDIDAS["pad_GlobalX"] / 2,
                    pady=(0, MEDIDAS["pad_GlobalY"] / 2))
        
        
        
        btnAgregarCam = tk.Button(lblFrameNuevaPan, 
                                  text="Agregar", 
                                  cursor="hand2",
                                  command=self.guardarNuevaPantalla,
                                  )
        btnAgregarCam.pack(
            side="right",
            padx=MEDIDAS["pad_GlobalX"] / 2,
            pady=(0, MEDIDAS["pad_GlobalY"] / 2))


        # creacion de variable entry para obtener su data
        self.etryNuevaPan = etryNuevaPan
        
    


    def validateIP(self, ip):
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ipaddress.AddressValueError:
            return False
        

    # Al seleccionar una campaña, solicita la actualizacion del contenido
    def onSelectCampana(self, event):        
        # obtenemos el listado a traves de peticion a la BD
        # funcion para mostrar las campañas
        self.mostrarPantallasLista(
            self.canvaPadrePantallas, 
            self.tablaPantallas.obtenerColumnaRestriccion(self.cbBoxSelectCampana.get())
            )
        
    

    def guardarNuevaPantalla(self):
        noExist = True
        #revision campo tenga un contenido valido
        if not self.etryNuevaPan.get() or not self.validateIP(self.etryNuevaPan.get()):
            messagebox.showerror(message="Favor de agregar un dato valido")
            self.etryNuevaPan.delete(0, tk.END)
            return
        
        
        #Validacion campaña seleccionada
        if not self.cbBoxSelectCampana.get():
            messagebox.showerror(message="Para guardar selecciona una campaña en el recuadro de arriba")
            return
          
        
        #recorre el listado de campañas y validamos si existe uno igual 
        #llamamos a la funcion de la bd "otenerColumnaRestriccion" y le pasamos la campaña elegida para realizar la validacion
        
        for pantalla in self.tablaPantallas.obtenerColumnaRestriccion(self.cbBoxSelectCampana.get()):
            if pantalla.lower() == self.etryNuevaPan.get().lower():
                noExist = False
                break
        
        
        #si no existe realiza el procedimiento de guardado
        if noExist:
            # realizamos el guardado del contenido y dependiendo el resultado la guardaremos en una varialble BOOLEANA
            notError = self.tablaPantallas.insertar(
                        pantalla = self.etryNuevaPan.get(), 
                        fk_campana = self.cbBoxSelectCampana.get() )
            
            #si no hay error continuamos
            if notError:
                
                messagebox.showinfo(message="Nueva Pantalla Guardada")
                
                #reiniciamos el canva para mostrar la lista actualizada
                self.mostrarPantallasLista(
                    self.canvaPadrePantallas,  
                    self.tablaPantallas.obtenerColumnaRestriccion(self.cbBoxSelectCampana.get()))
                
                #actualizamos los escrolls del canva
                actualizarCanva(self.canvaPadrePantallas, self.canvaHijoPantallas)
                
                self.etryNuevaPan.delete(0, 'end')
                
            else:
               messagebox.showerror(message="Error de conexion a la BD")
        else:
            messagebox.showwarning(message="La campaña que desea agregar ya existe")


    ##### funcion para mostrar la lista
    def mostrarPantallasLista(self, canvaPadre, listPantallas):    
        
        destruirListadoCanva(
            self.chkListData['box'], 
            self.chkListData['data'],)


        # modifica la lista de pantallas que aparecen
        for campana in listPantallas:

            var = tk.BooleanVar()  # Variable para cada Checkbutton
            # Guarda la campaña y su checkbox
            checkBtn = tk.Checkbutton(canvaPadre, text=campana, variable=var)
            checkBtn.config(bg="white")
            checkBtn.pack(anchor="w")
            
            self.chkListData['box'].append(checkBtn)
            self.chkListData['data'].append((campana, var))
        
        #modificar guardarlo en una funcion para actualizar la altura del contenido del list
        actualizarCanva(self.canvaPadrePantallas, self.canvaHijoPantallas)
        
        #deshabilita el btn si no hay contenido
        if not listPantallas:
            self.btnEliminarCam['state'] = tk.DISABLED
        else:
            self.btnEliminarCam['state'] = tk.NORMAL
                
        
    ##### Funcion para borrar pantallas
    def borrarPantalla(self): 
        if messagebox.askyesno(title="",message="Seguro que deseas eliminar las pantallas seleccionadas"):
        
            pantallaList = []
            
            #recorremos el listado de campanas de reversa
            #obtenemos su valor boolean si es true lo almacenamos en una variable para pasar a sql y eliminar
            #eliminamos la campaña del listado
            for i in reversed(range(len(self.chkListData['data']))):
                if(self.chkListData['data'][i][1].get()):
                    pantallaList.append(self.chkListData['data'][i][0])
                
            
            resultado = self.tablaPantallas.eliminar(pantallaList, self.cbBoxSelectCampana.get())

            
            if resultado:
                messagebox.showinfo(title="",message="Pantallas Eliminadas Correctamente")
                
                #reiniciamos el canva para mostrar la lista actualizada
                self.mostrarPantallasLista(
                    self.canvaPadrePantallas,  
                    self.tablaPantallas.obtenerColumnaRestriccion(self.cbBoxSelectCampana.get()))
                
                #actualizamos los escrolls del canva
                actualizarCanva(self.canvaPadrePantallas, self.canvaHijoPantallas)
            else:
                messagebox.showerror(title="",message="Ah ocurrido un error intente nuevamente")
                                                         

    ##### funcion para acutalizar la pestaña
    def actualziarCamapanas(self):
        self.cbBoxSelectCampana.config(values=self.tablaCampanas.obtenerColumna('campana'))
        self.cbBoxSelectCampana.set('')   

        # borra los checkbox que se quedaron en la pestaña
        destruirListadoCanva(
            self.chkListData['box'],
            self.chkListData['data']
        )     
        
        self.btnEliminarCam['state'] = tk.DISABLED
        

