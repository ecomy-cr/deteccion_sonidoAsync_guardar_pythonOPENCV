from datetime import datetime
from tkinter import W, Button, Label
from playsound import playsound

hora = datetime.now()

import threading
import cv2
import tkinter as tk

def alarma():
    cap = cv2.VideoCapture("Video.mp4")

    #his   tamaño del historico
    # muestra de pixeles para capturar 
    # detectShadows detecta sombras o no 
    
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc  = cv2.VideoWriter_fourcc(*'mp4v')

    grabador = cv2.VideoWriter("nuevo.mp4", fourcc, 30, (w,h) )

    mov = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=False)

    #opencCL desactivar
    cv2.ocl.setUseOpenCL(False)

    while(1):
        ret, frame = cap.read()

        #si no hay video cerramosS
        if not ret:
            break

        #aplicamos deteccion
        mascara = mov.apply(frame)

        #creamos copia para los contornos
        contornos = mascara.copy()

        #buscamos los contornos
        con, jerarquia = cv2.findContours(contornos, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#pasamos por los contornos 
        for i in con:
            #contornos pequeños ruido en el video 
            if cv2.contourArea(i) < 8918:
                continue
            if cv2.contourArea(i) >= 8918:
                #obtenemos los limites de los contornos 
                (x,y,w,h) = cv2.boundingRect(i)

                #dibujamos rectangulo en la imagen o video
                cv2.rectangle(frame, (x,y) , (x+w, y+h), (0,0,255),2)
                cv2.putText(frame, '{}'.format('alarma') , (x,y-5), 1,1.3, (0,0,255) , 1, cv2.LINE_AA)
                grabador.write(frame)
            
#async
            threading.Thread(target=playsound, args=('bu.wav',), daemon=True).start()

        #mostramos la camara, mascara y contornos
        cv2.imshow('Alarma activa' , frame)
        #cv2.imshow('Umbral' , mascara)
        #cv2.imshow('Contornos', contornos)

        k = cv2.waitKey(5)
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


def normal():
    
    cap = cv2.VideoCapture("Video.mp4")

    #his   tamaño del historico
    # muestra de pixeles para capturar 
    # detectShadows detecta sombras o no 


    mov = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=False)

    #opencCL desactivar
    cv2.ocl.setUseOpenCL(False)
    while(1):
        ret, frame = cap.read()
        if not ret:
            break
    
        #aplicamos deteccion
        mascara = mov.apply(frame)

        #creamos copia para los contornos
        contornos = mascara.copy()

        #buscamos los contornos
        con, jerarquia = cv2.findContours(contornos, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#pasamos por los contornos 
        for i in con:
            #contornos pequeños ruido en el video 
            if cv2.contourArea(i) < 11918:
                continue
            if cv2.contourArea(i) >= 11918:
                #obtenemos los limites de los contornos 
                (x,y,w,h) = cv2.boundingRect(i)

                #dibujamos rectangulo en la imagen o video
                cv2.rectangle(frame, (x,y) , (x+w, y+h), (0,0,255),2)
                cv2.putText(frame, '{}'.format('movimiento') , (x,y-5), 1,1.3, (0,0,255) , 1, cv2.LINE_AA)
    
        #mostramos la camara, mascara y contornos
        cv2.imshow('Alarma activa' , frame)
        cv2.imshow('Umbral' , mascara)
        cv2.imshow('Contornos', contornos)

        k = cv2.waitKey(5)
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()



def tk_pantalla_app():
    #hacer global una variable para usarla en todo el codigo
    global miPantalla
    miPantalla = tk.Tk()

    #tamaño
    
    miPantalla.geometry("500x250")
    fecha = datetime.now()

    miPantalla.title("Camara de seguridad YeAraya")
    Label(text ="Hola Yeisson, {}".format(fecha), bg ="gray", width="300", height= "2", font= ("Verdana", 13)).pack()
#espacio
    Label( miPantalla, text="").pack()


    Button(text="Iniciar con Alarma", height="2", width="30", command= alarma).pack()


    #creamos espacio
    
    Label( miPantalla, text="").pack()



    Button(text="Iniciar sin Alarma", height="2", width="30", command= normal).pack()

    miPantalla.mainloop()

tk_pantalla_app()
