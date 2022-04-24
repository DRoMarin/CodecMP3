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
with open("encoder.txt") as File:
    #total_rows = sum(1 for row in File)
    x=[0]*12448*2
    index=0
    for row in File:
        x[index]=int(row)
        index=index+1

print(len(x))


# INGRESO
archivo = 'test_audio.wav'
faudio, audio = waves.read(archivo)

def binary_to_decimal(numero_decimal):
    modulos = [0]*8 # la lista para guardar los módulos
    pos=7
    num_bin=0
    while numero_decimal != 0: # mientras el número de entrada sea diferente de cero
    # paso 1: dividimos entre 2
        modulo = numero_decimal % 2
        cociente = numero_decimal // 2
        modulos[pos]=modulo # guardamos el módulo calculado
        numero_decimal = cociente # el cociente pasa a ser el número de entrada
        pos=pos-1
    bit_signo=modulos[1]
    numero=modulos[2:8]
    if bit_signo==0:
        factor=1
    else:
        factor=-1
    pos=0
    for digito in numero[::-1]:
        num_bin=num_bin+digito*(2**pos)
        pos=pos+1
    num_bin=factor*num_bin
    return num_bin
        
 

def IFFT_64(x):
    fft_size=len(x)//2 
    ifft_out=[0]*64
    real=[0]*(fft_size)
    imag=[0]*(fft_size)
    pos_real=0
    pos_imag=0
    for number in x:
        if number<=128:
            real[pos_real]=binary_to_decimal(number)
            pos_real=pos_real+1
        else:
            imag[pos_imag]=binary_to_decimal(number)
            pos_imag=pos_imag+1
    
    real=np.array(real)*820
    imag=(np.array(imag)*8202)*1j 
    x=real+imag
    
    for bloque_index in range(0,fft_size,int(64/2)):
        bloque_temp=x[bloque_index:bloque_index+int(64/2)]
        output_temp=np.fft.irfft(bloque_temp)
        if bloque_index==0:
            ifft_out=output_temp
        else: 
            ifft_out=np.concatenate((ifft_out,output_temp))  
    ifft_out=np.asarray(np.around(ifft_out), dtype = int)
    return ifft_out




#n = np.fft.fft(x)
#ni= np.fft.irfft(x)
man=IFFT_64(x)

with open('decoder_signal_64.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(man)

plt.subplot(2,1,1)
plt.title("Time signal")
plt.plot(audio)

plt.subplot(2,1,2)
plt.title("IFFT")
plt.plot(man)

plt.show()

textfile = open("decoder.txt", "w")
for element in man:
    textfile.write(str(element) + "\n")
textfile.close()


