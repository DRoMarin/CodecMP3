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



#with open('encoder_signal_64.csv') as File:
#    reader = csv.reader(File, delimiter=',', quotechar=',',
#                        quoting=csv.QUOTE_MINIMAL)
#    for row in reader:
#        if len(row)>0:
#            x=[0]*len(row)
#            x[0:len(row)]=row
# 
#print(x)
with open("encoder2.txt") as File:
    #total_rows = sum(1 for row in File)
    x=[0]*12448*2
    index=0
    for row in File:
        x[index]=int(row)
        index=index+1




# INGRESO
archivo = 'test_audio.wav'
faudio, audio = waves.read(archivo)

def binary_to_decimal(numero_decimal):
    a=numero_decimal
    modulos = [0]*16 # la lista para guardar los módulos
    pos=7
    real=0
    imag=0
    while numero_decimal != 0: # mientras el número de entrada sea diferente de cero
    # paso 1: dividimos entre 2
        modulo = numero_decimal % 2
        cociente = numero_decimal // 2
        modulos[pos]=modulo # guardamos el módulo calculado
        numero_decimal = cociente # el cociente pasa a ser el número de entrada
        pos=pos-1
    
    bit_signo=modulos[0]
    numero=modulos[2:8]
    bit_signo_imag=modulos[8]
    numero_imag=modulos[9:16]
    if bit_signo==0:
        factor=1
    else:
        factor=-1
    if bit_signo_imag==0:
        factor_imag=1
    else:
        factor_imag=-1
    pos=0
    for digito in numero[::-1]:
        real=real+digito*(2**pos)
        pos=pos+1
    pos=0
    for digito in numero_imag[::-1]:
        imag=imag+digito*(2**pos)
        pos=pos+1
    real=factor*real
    imag=factor_imag*imag
    #print(a,modulos,numero,numero_imag,real,imag)
    complex=real+imag*1j
    return complex
        
 

def IFFT_64(x):
    fft_size=len(x)//2 
    ifft_out=[0]*64
    pos=0
    samples=[0]*len(x)
    for number in x:
        samples[pos]=binary_to_decimal(number)
        pos=pos+1
    
    for bloque_index in range(0,fft_size,int(64/2)):
        bloque_temp=samples[bloque_index:bloque_index+int(64/2)]
        output_temp=np.fft.irfft(bloque_temp)
        if bloque_index==0:
            ifft_out=output_temp
        else: 
            ifft_out=np.concatenate((ifft_out,output_temp))  
    ifft_out=np.asarray(np.around(ifft_out), dtype = int)
    ifft_out=ifft_out*406
    return ifft_out




#n = np.fft.fft(x)
#ni= np.fft.irfft(x)
man=IFFT_64(x)



plt.subplot(2,1,1)
plt.title("Time signal")
plt.plot(audio)

plt.subplot(2,1,2)
plt.title("IFFT")
plt.plot(man)

plt.show()

textfile = open("decoder2.txt", "w")
for element in man:
    textfile.write(str(element) + "\n")
textfile.close()


