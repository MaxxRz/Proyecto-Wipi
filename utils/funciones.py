import tkinter as tk
from tkinter import filedialog
from utils.config_ui import FONTS, MEDIDAS, COLORS

import win32com.client
import os
import shutil
import cv2 as cv
import json



## FUNCIONES GENERICAS DE USO
def actualizarCanva(padre, canva):
    # Actualizar la región del Canvas para el scroll
    padre.update_idletasks()
    canva.config(scrollregion=canva.bbox("all"))
    

def contenedorCanva(FramePadre):
    # canvas contenedor para hacer scroll de campañas
    # Canvas para scroll
    # Configuracion del contenedor canva 
    canvas = tk.Canvas(FramePadre)
    canvas.config(
        bg="white")
    canvas.pack(fill="both", 
                expand=True, 
                padx=MEDIDAS["pad_GlobalX"] / 2,
                pady=(0, MEDIDAS["pad_GlobalY"]/ 2),)
    
    # Crear un Scrollbar para el Canvas
    scrollbar = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    
    # Configurar el Canvas para que use el Scrollbar 
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Crear un Frame dentro del Canvas que contendrá los Checkbuttons
    frameContenido = tk.Frame(canvas)
    frameContenido.config(bg="white")
    canvas.create_window((0, 0), window=frameContenido, anchor="nw")
    
    #retorna el contenedor y el canva para actualizar su contenido en el futuro
    return [frameContenido, canvas]


def destruirListadoCanva(chkBoxes, chkData):    
    for chk in chkBoxes:
        chk.destroy()

    chkBoxes.clear()
    chkData.clear()


def obtenerArchivo():
    filePaths = filedialog.askopenfilenames(
        filetypes=(
            ("Todos los archivos compatibles", "*.mp4 *.avi *.pptx"),
            ("Archivos MP4", "*.mp4"),
            ("Archivos AVI", "*.avi"),
            ("Presentaciones PowerPoint", "*.pptx")
        )
    )

    return filePaths


def obtenerConfig():
    configPath = os.path.join(os.path.dirname(__file__), 'config.json')
    
    
    #obtenemos la configuracion
    with open(configPath, 'r') as f:
        config = json.load(f)
    
    return config[0]
    


## FUNCIONES COPILACION DE VIDEOS

def powerPointToVideo(urlPresentacion):
    root = os.getcwd()
    
    ppt_path = urlPresentacion
    output_folder = os.path.join(root, f"files\presentacion")
    
    # Crear la carpeta si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    #creamos una carpeta e introducimos cada diapositiva como imagen
    ppt_app = win32com.client.Dispatch("PowerPoint.Application")

    presentation = ppt_app.Presentations.Open(ppt_path, WithWindow=False)
    presentation.Export(output_folder, "JPG")
    presentation.Close()
    ppt_app.Quit()
    

    #----------------------------------------------------------
    
    listaImagenes = []
    listaImagenes2 = []
    imagenesComprimidas = []
    
    dataConfig = obtenerConfig()

    #recorremos el listado de imagenes y las organizamos numericamente
    for img in os.listdir(output_folder):
        if len(img) < 17:
            listaImagenes.append(img)
        else:
            listaImagenes2.append(img)
    
    #array con la lista de imagenes organizada
    listaImagenes.extend(listaImagenes2)

    #leemos las imagenes por bit y las guardamos
    for img in listaImagenes:
        imagenesComprimidas.append(cv.imread(os.path.join(output_folder, img)))
    


    listadoArchivos = os.listdir(os.path.join(root, f"files"))
    
    nameVideo = os.path.join(root, f"files/video{len(listadoArchivos)}.avi")
    

    #obtenemos las medidas
    fps = dataConfig['fps']
    width = dataConfig['width']
    height = dataConfig['height']
    duracion = dataConfig['duracion_por_imagen']
    framesXImagen = int(duracion * fps)
    
    
    # creacion del video 
    out = cv.VideoWriter(nameVideo, cv.VideoWriter_fourcc(*'XVID'), fps, (width, height))
    
    for img in imagenesComprimidas:
        for _ in range(framesXImagen):
            frame = cv.resize(img, (width, height))
            out.write(frame)
            
    out.release()
    
    
    try:
        #eliminarmos la carpeta de imagenes
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
    except OSError as e:
        print(f"Error al eliminar la carpeta '{output_folder}': {e}")


def videoToVideo(urlVideo):
    root = os.getcwd()
    dataConfig = obtenerConfig()
    
    listadoArchivos = os.listdir(os.path.join(root, f"files"))
    
    noArchivos = (len(listadoArchivos) + 1)
    
    output_folder = os.path.join(root, fr"files\video{noArchivos}.avi")
    
    #si el video es "Avi" solo copiamos y terminamos
    if urlVideo[-3:] == "avi":
        try:
            shutil.copy(urlVideo, output_folder)
        except:
            pass
        
        return
    
    # Abrir el video MP4
    cap = cv.VideoCapture(urlVideo)
    
    fps = dataConfig['fps']
    width = dataConfig['width']
    height = dataConfig['height']
    

    # Crear escritor para AVI
    out = cv.VideoWriter(output_folder, cv.VideoWriter_fourcc(*'XVID'), fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_resized = cv.resize(frame, (width, height))
        out.write(frame_resized)

    cap.release()
    out.release()
    
    
    
def copilarArchivos(archivos, loading):
    
    root = os.path.join(os.getcwd(), f"files")
    listadoVideos = os.listdir(root) 
    
    #Borramos todos los archivos si hay
    for ruta in listadoVideos:
        ruta = os.path.join(root, ruta)
        print("video:")
        print(ruta)
        if os.path.exists(ruta):
            os.remove(ruta)
    
    
    #recorremos el listado de archivos
    for archivo in archivos:
        directArchivo = archivo[0]
        
        #si es una presentacion creamos video
        if directArchivo[-4:] == "pptx":
            loading.update_status("Convirtiendo presentacion a video...")
            powerPointToVideo(directArchivo)
        
        #si es video pasamos directo
        if directArchivo[-3:] == "mp4" or directArchivo[-3:] == "avi":
            loading.update_status("Modificando Video...")
            videoToVideo(directArchivo)
            
    loading.update_status("Copilando Videos...")

    #despues de copilar todos los videos en una carpeta 
    
    dataConfig = obtenerConfig()
    videoFinal = os.path.join(root, 'videoFinal.avi')
    
    listadoCap = []
    
    #si solo hay un video, cambiamos el nombre y finalizamos
    if len(listadoVideos) == 1:
        archivo = os.path.join(root, listadoVideos[0])
        archivo2 = os.path.join(root, 'videoFinal.avi')
        os.rename(archivo, archivo2)
        return
    
    #si hay mas de un video, enlistamos las rutas
    for video in listadoVideos:
        listadoCap.append(cv.VideoCapture(os.path.join(root, video)))
    
    
    fps = dataConfig['fps']
    width = dataConfig['width']
    height = dataConfig['height']
        
    # Crear el video final
    out = cv.VideoWriter(videoFinal, cv.VideoWriter_fourcc(*'XVID'), fps, (width, height))

    for cap in listadoCap:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_resized = cv.resize(frame, (width, height))
            out.write(frame_resized)
        cap.release()
    
    out.release()
    
    #Al finalizar eliminaremos todos los videos y dejaremos solo el ultimo
    for ruta in listadoVideos:
        ruta = os.path.join(root, ruta)

        if os.path.exists(ruta):
            os.remove(ruta)