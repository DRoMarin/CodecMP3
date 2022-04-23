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

def FFT(x):
    N=len(x)
    #print(N)
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
            yr[k+N//2]= yr[k+N//2]+z-z1 #parte real transformada posición k + N/2
            z=sin(-angulo1)
            z1=sin(-angulo2)
            z=z*x[2*i] #posición par
            z1=z1*x[2*i+1] #posición impar
            yi[k]=yi[k]+z+z1 #parte imaginaria transformada posición k
            yi[k+N//2]= yi[k+N//2]+z-z1 #parte imaginaria transformada posición k + N/2
        y[k]=yr[k]+1j*yi[k]
        y[k+N//2]=yr[k+N//2]+1j*yi[k+N//2]
        #print(k,i)
    return y

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
        print(len(bloque_temp[0:32]))
        if bloque_index==0:
            fft_out=bloque_temp[0:32]
        else:
            fft_out=np.concatenate((fft_out,bloque_temp[0:32]))
    fft_out=np.around(fft_out/415)
    return fft_out

man = FFT_64(audio)
print(max(man))
print(min(man))

plt.title("FFT")
plt.plot(man)
plt.show()
#print(man)
#print(len(man))
#print(audio)
#print(man[388])
#n = np.fft.fft(audio)

with open('encoder_signal_64.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(man)

textfile = open("encoder.txt", "w")
for element in man:
    textfile.write(str(element) + "\n")
textfile.close()







