# -*- coding: utf-8 -*-

import numpy
import pathlib
import pandas as pd
from graficar import * 
from audio import * 
from fingerprint import * 
from hashing import * 
FileName='grabacion'

print("¿Que desea hacer?")
modo = input()

def grabacion(filename, seconds):

    print("Presione 'r' para empezar la grabación...")
    record(seconds,filename)

def play(filename):

    print("Presione 'p' para reproducir el audio...")

def crear_fingerprint(filename, filename_fp, name, test=False):
    print("Haciendo maravillas...")

def Busqueda_matching(dfC, min_match = 5):
    print("Haciendo maravillas...")

def db():
    f=open('data/patrones/fingerprints/BASE_DATOS.txt',"w")
    dir = 'data/patrones/files'
    directorio = pathlib.Path(dir)
    for fichero in directorio.iterdir():
        f.write(fichero.name+'\n')
    f.close()

def read_db():
    f = "data/patrones/fingerprints/BASE_DATOS.txt"
    return f   

def resultados(mode, display = True, direct = "output"):


    if mode == 'grabar':

        print("******************************************************")
        print("****************** Grabar música *********************")
        print("******************************************************")

        record(FileName+'.wav',20)
        canal(FileName+'.wav')
        FsHz, x1 = wav.read(FileName+'.wav')
        sub(FileName,FsHz,x1)

    elif mode == 'actualizar':

        print("******************************************************")
        print("************ Base de datos txt ***********************")
        print("******************************************************")
        db()

    elif mode == 'fingerprint':

        print("******************************************************")
        print("****************** FINGERPRINT ***********************")
        print("******************************************************")

        with open(read_db(), 'r') as d:
            for linea in d:
                 
                 abc='data/patrones/files/'+linea[0:len(linea)-5]
                 FsHz, x1 = wav.read(abc+'.wav')
                 sub('data/patrones/fingerprints/'+linea[0:len(linea)-5],FsHz,x1)
                  
        

    elif mode == 'evaluar':
        print("******************************************************")
        print("**************** Opinión de Marvel *******************")
        print("******************************************************")

        with open(read_db(), 'r') as d:
            for linea in d:
                 abc='data/patrones/fingerprints/'+linea[0:len(linea)-5]
                 Record = pd.read_csv(abc+'.csv', names=['Hash'], sep=";")
                 pf = pd.read_csv('grabacion'+'.csv', names=['Hash'], sep=";")
                 print(len(Record))
                 print(matching(Record,Record))

resultados(modo)