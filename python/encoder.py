from decimal import ROUND_UP
from tkinter import N
import numpy as np
import matplotlib.pyplot as plt
import time
from cmath import exp, log, pi, cos, sin
import scipy.io.wavfile as waves
from typing import List
import csv

# let us try to grasp this idea for a small example


# INGRESO
archivo = 'test_audio.wav'
faudio, audio = waves.read(archivo)

def decimal_to_binary(numero_decimal,real):
    modulos = [0]*8 # la lista para guardar los módulos
    a=numero_decimal
    if numero_decimal>0:
        bit_signo=0
    else:
        bit_signo=1
    if  real:
        bit_complejo=0
    else:
        bit_complejo=1
    modulos[0]=bit_complejo
    modulos[1]=bit_signo
    numero_decimal=abs(numero_decimal)
    pos=7
    num_bin=0
    while numero_decimal != 0: # mientras el número de entrada sea diferente de cero
    # paso 1: dividimos entre 2
        modulo = numero_decimal % 2
        cociente = numero_decimal // 2
        modulos[pos]=modulo # guardamos el módulo calculado
        numero_decimal = cociente # el cociente pasa a ser el número de entrada
        pos=pos-1
    
   
    pos=0
    for digito in modulos[::-1]:
        num_bin=num_bin+digito*(2**pos)
        pos=pos+1
    return num_bin

def FFT_64(x):
    audio_len=len(x)
    samples_in=[0]*int(np.ceil(audio_len/64)*64)
    #output_vector=[0]*int(np.ceil(audio_len/64))
    #print(len(samples_in))
    samples_in[0:audio_len]=x
    #print(len(samples_in))
    #print(samples_in)
    bloque=[0]*64
    fft_out=[0]*int(64/2)
    for bloque_index in range(0,len(samples_in),64):
        bloque=samples_in[bloque_index:bloque_index+64]
        bloque_temp=np.fft.rfft(bloque)
        #print(len(bloque_temp[0:32]))
        if bloque_index==0:
            fft_out=bloque_temp[0:32]
        else:
            fft_out=np.concatenate((fft_out,bloque_temp[0:32]))
    #fft_out=np.around(fft_out)
    real=np.asarray((np.real(fft_out))/820, dtype = int)
    imag=np.asarray((np.imag(fft_out))/820, dtype = int)
    print(len(real),max(real),min(real))
    print(len(imag),max(imag),min(imag))
    for index in range(len(real)):
        real[index]=decimal_to_binary(real[index],True)
        imag[index]=decimal_to_binary(imag[index],False)
        
        
    print(len(real),max(real),min(real))
    print(len(imag),max(imag),min(imag))
    fft_out=np.real(np.concatenate((real,imag)))
    return fft_out

man = FFT_64(audio)


plt.title("FFT")
plt.plot(man)
plt.show()
#print(man)
#print(len(man))
#print(audio)
#print(man[388])
#n = np.fft.fft(audio)



textfile = open("encoder.txt", "w")
for element in man:
    textfile.write(str(element) + "\n")
textfile.close()







