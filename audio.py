
import pyaudio
import wave
import sys
import sounddevice as sd
from scipy.io.wavfile import write
from playsound import playsound

def play_audio(filename):
    print('Escuchando ...... ')
    playsound(filename)

def record(filename,seconds):
    
    fs = 2100  

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    print('Recording: ', seconds, "seconds *********")
    sd.wait()  # Wait until recording is finished
    print('**** Finished recording')
    write(filename, fs, myrecording)  # Save as WAV file 
    print('**** Save audio: ', filename)

