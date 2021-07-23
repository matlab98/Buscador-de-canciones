#import the pyplot and wavfile modules 

import matplotlib.pyplot as plot

import scipy.io.wavfile as waves
import numpy as np 
 

# Read the wav file (mono)



def canal(FileName): 
    muestreo, sonido = waves.read(FileName)
    # canales: monofónico o estéreo
    tamano = np.shape(sonido)
    muestras = tamano[0]
    m = len(tamano)
    canales = 1  # monofónico
    if (m>1):  # estéreo
        canales = tamano[1]
    # experimento con un canal
    if (canales>1):
       canal = 0
       uncanal = sonido[:,canal] 
    else:
       uncanal = sonido
    graficar(uncanal,muestreo)
    

def graficar(uncanal,muestreo): 

    # rango de observación en segundos
    inicia = 0.000
    termina = 2.000*10

    # observación en número de muestra
    a = int(inicia*muestreo)
    b = int(termina*muestreo)
    parte = uncanal[a:b]

    # tiempos en eje x
    dt = 1/muestreo
    ta = a*dt
    tb = (b-1)*dt
    tab = np.arange(ta,tb,dt)

    plot.plot(tab,parte[0:len(tab)])
    plot.xlabel('tiempo (s)')
    plot.ylabel('Amplitud')
    plot.show(block=False)





