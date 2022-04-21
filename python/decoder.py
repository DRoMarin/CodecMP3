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
#        print(row)
# 
x=[]
with open("encoder.txt") as File:
    for row in File:
        xsub=[]
        row=row.split(",")
        for string in row:
            characters = "[()]n'\]"
            for i in range(len(characters)):
                string = string.replace(characters[i],"")
                string = string.strip('\n')
            string=complex(string)
            xsub.append(string)
        x.append(xsub)
    



 


# let us try to grasp this idea for a small example


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
    n=len(x)
    N=n*64
    y=[0]*N
    ymed=[]
    k=0
    for xsub in x:
        ysub=IFFT(xsub)  
        ymed.append(ysub)  
    for i in range(n):
        for j in range(64):
            y[k]=ymed[i][j]
            print(k,y[k])
            k=k+1
    return y




n = np.fft.fft(audio)
ni= np.fft.ifft(n)
man=IFFT_64(x)


plt.subplot(2,3,1)
plt.title("Time signal")
plt.plot(audio)


plt.subplot(2,3,4)
plt.title("FFT numpy")
plt.plot(n)

plt.subplot(2,3,5)
plt.title("IFFT numpy")
plt.plot(ni)

plt.subplot(2,3,6)
plt.title("IFFT manual")
plt.plot(man)

plt.show()



