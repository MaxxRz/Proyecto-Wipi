import tkinter as tk
from tkinter import messagebox

from utils.config_ui import FONTS, MEDIDAS, COLORS

from utils.funciones import actualizarCanva, destruirListadoCanva, contenedorCanva



## Frame para pestaña donde se agregaran las nuevas campañas
class FrameCampanas(tk.Frame):
    def __init__(self, root = None, tablaDB = None):
        super().__init__(root)
        self.root = root
        self.config(
            width=self.root.winfo_width(),
            height=self.root.winfo_height()
            )
        self.grid(row=0, column=0, sticky="nsew")
        
        #variable de lista de campanas checkbox
        self.chkListadoData = []
        self.checkboxes = []
        self.chkListData = {
            "box": [],
            "data": [],
        }
        
        
        # tabla de BD campañas 
        self.tablaCampanas = tablaDB
        
                
        
        # frames
        self.listCampanas()
        self.nuevaCampana()
        
        
    
    #container donde mostrara la lista de campañas y se trabajaran
    def listCampanas(self):
        # Label Contenedor
        lblFrameCampanas = tk.LabelFrame(self, text="Campañas")
        lblFrameCampanas.config(
            font=(FONTS["lblFrame"]),
            height=250,
        )
        lblFrameCampanas.pack_propagate(False)
        lblFrameCampanas.pack(padx=MEDIDAS["pad_GlobalX"],
                               pady=(MEDIDAS["pad_FrameTop"], 0),
                               fill=tk.X,)

        
        #funcion para crear un contenedor canva.
        #le pasamos el contenedor padre y regresara el canva padre e hijo
        canvaCampana = contenedorCanva(lblFrameCampanas)
        
        #modificamos la altura del contenedor
        canvaCampana[1].pack(pady=MEDIDAS["pad_GlobalY"]/ 2,)
        
        #Btn Eliminar Campaña
        btnEliminarCam = tk.Button(lblFrameCampanas, text="Eliminar", command=self.borrarCampana)
        btnEliminarCam.config(
            cursor="hand2"
        )
        btnEliminarCam.pack(
            side="right",
            padx=MEDIDAS["pad_GlobalY"] / 2,
            pady=(0, MEDIDAS["pad_GlobalY"] / 2), )
        
        
        #Guardar btn en una variable para usarla despues
        self.btnEliminarCam = btnEliminarCam

      
        
        #### Creacion de variables
        #canvaContenido guarda el canva para volver a cargar en un futuro
        self.canvaPadre = canvaCampana[0]
        #guardamos el canvas en una variable self para usarla mas adelante
        self.canvaHijo = canvaCampana[1]
        
        
        
        # obtenemos el listado a traves de peticion a la BD
        #for campana in  self.tablaCampanas.obtenerTodo():
        # funcion para mostrar las campañas
        self.mostrarCampanaLista(self.canvaPadre,  self.tablaCampanas.obtenerTodo())
    

            
        # Actualizar la región del Canvas para el scroll
        actualizarCanva(self.canvaPadre, self.canvaHijo)


            
    def nuevaCampana(self):
        # Label Contenedor
        lblFrameNuevaCam = tk.LabelFrame(self, text="Agregar")
        lblFrameNuevaCam.config(
            font=(FONTS["lblFrame"]),
            height=200,
        )
        lblFrameNuevaCam.pack(padx=MEDIDAS["pad_GlobalX"],
                               pady=MEDIDAS["pad_GlobalY"],
                               fill=tk.X)
        
        
        lblEtryNuevaCam = tk.Label(lblFrameNuevaCam, text="Ingrese el nombre de la campaña que desea agregar:")
        lblEtryNuevaCam.config(
            font=FONTS["text"],
            fg=COLORS["text"],
            anchor="w"
            )
        lblEtryNuevaCam.pack(padx=MEDIDAS["pad_GlobalX"] / 2,
                             pady=(MEDIDAS["pad_GlobalY"] / 2, 0 ),
                             fill=tk.X)
        
        etryNuevaCam = tk.Entry(lblFrameNuevaCam)
        etryNuevaCam.config(
                    font=FONTS["text"])
        etryNuevaCam.pack(fill="x", 
                    expand=True,
                    ipady=2,
                    padx=MEDIDAS["pad_GlobalX"] / 2,
                    pady=(0, MEDIDAS["pad_GlobalY"] / 2))
        
        btnAgregarCam = tk.Button(lblFrameNuevaCam, 
                                  text="Agregar", 
                                  cursor="hand2",
                                  command=self.guardarNuevaCampana)
        btnAgregarCam.pack(
            side="right",
            padx=MEDIDAS["pad_GlobalX"] / 2,
            pady=(0, MEDIDAS["pad_GlobalY"] / 2))

        # creacion de variable entry para obtener su data
        self.etryNuevaCam = etryNuevaCam
    

    # Funcion para el validado y guardado de un elemento
    def guardarNuevaCampana(self):
        noExist = True
        
        if not self.etryNuevaCam.get():
            messagebox.showerror(message="Favor de agregar un dato valido")
            return
        
        #recorre el listado de campañas y validamos si existe uno igual 
        for campana in self.tablaCampanas.obtenerColumna('campana'):
            if campana.lower() == self.etryNuevaCam.get().lower():
                noExist = False
                break
        
        #si no existe realiza el procedimiento de guardado
        if noExist:
            # valida si el guardado en la BD falla
            if self.tablaCampanas.insertar(campana = self.etryNuevaCam.get()):
                
                #guarda la campana en el SQL
                messagebox.showinfo(message="Nueva Campaña Guardada")
                
                #agrega el nuevo elemento a la lista para mostrar lo guardado
                self.mostrarCampanaLista(self.canvaPadre,  self.tablaCampanas.obtenerTodo())
                
                #actualizamos los escrolls del canva
                actualizarCanva(self.canvaPadre, self.canvaHijo)
                
                #reiniciamos el entry
                self.etryNuevaCam.delete(0, 'end')
            else:
               messagebox.showerror(message="Error de conexion a la BD")
                
        else:
            messagebox.showwarning(message="La campaña que desea agregar ya existe")


    ##### Funcion para borrar campanas
    def borrarCampana(self):
        if messagebox.askyesno(title="",message="Seguro que deseas eliminar las campañas seleccionadas"):
            campanasList = []

            #recorremos el listado de campanas de reversa
            #obtenemos su valor boolean si es true lo almacenamos en una variable para pasar a sql y eliminar
            #eliminamos la campaña del listado
            for i in reversed(range(len(self.chkListData['data']))):
                if(self.chkListData['data'][i][1].get()):
                    campanasList.append(self.chkListData['data'][i][0])
                                            
            #realizamos la eliminacion de las campañas en la bd y guardamos su retorno                 
            resultado = self.tablaCampanas.eliminar(campanasList)
            
            if resultado:
                messagebox.showinfo(title="",message="Campañas Eliminadas Correctamente")
                
                #modificar guardarlo en una funcion para actualizar la altura del contenido del list
                #modificar guardarlo en una funcion para actualizar la altura del contenido del list
                self.mostrarCampanaLista(self.canvaPadre,  self.tablaCampanas.obtenerTodo())
                
                #actualizamos los escrolls del canva
                actualizarCanva(self.canvaPadre, self.canvaHijo)
            else:
                messagebox.showerror(title="",message="Ah ocurrido un error intente nuevamente")
                    
           
    ##### funcion para mostrar la lista
    def mostrarCampanaLista(self, framePadre, listCampanas):    
            
        destruirListadoCanva(
            self.chkListData['box'], 
            self.chkListData['data'],)

        
            #deshabilita el btn si no hay contenido
        if not listCampanas:
            self.btnEliminarCam['state'] = tk.DISABLED
        else:
            self.btnEliminarCam['state'] = tk.NORMAL
        
        listCampanas = [lista[1] for lista in listCampanas]
        
        for campana in listCampanas:
            
            var = tk.BooleanVar()  # Variable para cada Checkbutton
            # Guarda la campaña y su checkbox
            checkBtn = tk.Checkbutton(framePadre, text=campana, variable=var)
            checkBtn.config(bg="white")
            checkBtn.pack(anchor="w")
            
            self.chkListData['box'].append(checkBtn)
            self.chkListData['data'].append((campana, var))
        
            






