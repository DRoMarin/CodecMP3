from re import L
from tkinter import N
import numpy as np
import matplotlib.pyplot as plt
import time
from cmath import exp, pi, cos, sin
from math import log2
import scipy.io.wavfile as waves
from typing import List
import csv


# INGRESO
archivo = 'test_audio.wav'
faudio, audio = waves.read(archivo)

import json
import pickle




def IFFT_64(x):
    fft_size=len(x)//2 
    ifft_out=[0]*64

    for bloque_index in range(0,fft_size,int(64/2)):
        bloque_temp=x[bloque_index:bloque_index+int(64/2)]
        output_temp=np.fft.irfft(bloque_temp)
        if bloque_index==0:
            ifft_out=output_temp
        else: 
            ifft_out=np.concatenate((ifft_out,output_temp))  
    return ifft_out*320

#man=IFFT_64(x)



#plt.subplot(2,1,1)
#plt.title("Time signal")
#plt.plot(audio)

#plt.subplot(2,1,2)
#plt.title("IFFT")
#plt.plot(man)

#plt.show()

#textfile = open("decoder.txt", "w")
#for element in man:
#    textfile.write(str(element) + "\n")
#textfile.close()

