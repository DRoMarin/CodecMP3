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
    x=[0]*12448
    index=0
    for row in File:
        x[index]=complex(row)
        index=index+1





# INGRESO
archivo = 'test_audio.wav'
faudio, audio = waves.read(archivo)

def IFFT(x):
    N=len(x)
    print(N)
    angulo1=0
    angulo2=0
    z=0
    z1=0
    delta=4*pi/N
    yr=[0]*N
    yi=[0]*N
    y=[0]*N
    for k in range(0,N//2,1):
        for i in range(N//2):
            angulo1=i*delta*k  # n*k*2*pi/(N/2)
            angulo2=angulo1+(delta/2)*k #n*k*2*pi/(N/2)  + 2*pi/N
            z=cos(angulo1)
            z1=cos(angulo2)
            z=z*x[2*i] #posición par
            z1=z1*x[2*i+1] #posición impar
            yr[k]=yr[k]+z+z1 #parte real transformada posición k
            yr[N-1-k]= yr[N-1-k]+z+z1 #parte real transformada posición k + N/2
            z=sin(angulo1)
            z1=sin(angulo2)
            z=z*x[2*i] #posición par
            z1=z1*x[2*i+1] #posición impar
            yi[k]=yi[k]+z+z1 #parte imaginaria transformada posición k
            yi[N-1-k]= yi[N-1-k]+z+z1 #parte imaginaria transformada posición k + N/2
        print(k,i)
        y[k]=(yr[k]+1j*yi[k])
        y[N-1-k]=(yr[N-1-k]-1j*yi[N-1-k])
        
    return y

def IFFT_64(x):
    fft_size=len(x) 
    ifft_out=[0]*64
    x= np.multiply(x, 415)
    for bloque_index in range(0,fft_size,int(64/2)):
        bloque_temp=x[bloque_index:bloque_index+int(64/2)]
        output_temp=np.fft.irfft(bloque_temp)
        if bloque_index==0:
            ifft_out=output_temp
        else: 
            ifft_out=np.concatenate((ifft_out,output_temp))  
    ifft_out=np.around(ifft_out)   
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



