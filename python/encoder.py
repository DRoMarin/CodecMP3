from tkinter import N
import numpy as np
import matplotlib.pyplot as plt
import time
from cmath import exp, pi, cos, sin
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
    n=len(x)
    xnew=[]
    xsub=[0]*64
    ynew=[]
    ynumpy=[]
    for k in range(0,n,64):
        for i in range(64):
            if k+i<n:
                xsub[i]=x[k+i]
        ysub=FFT(xsub)
        ysub1=np.fft.fft(xsub)
        xnew.append(xsub)
        xsub=[0]*64
        ynew.append(ysub)
        ynumpy.append(ysub1)
    return ynew, ynumpy

man,n = FFT_64(audio)
#print(audio)
#print(man[388])
#n = np.fft.fft(audio)

#with open('encoder_signal_64.csv', 'w') as f:
 #   write = csv.writer(f)
 #   write.writerow(man)

textfile = open("encoder.txt", "w")
for element in man:
    textfile.write(str(element) + "\n")
textfile.close()



plt.subplot(2,3,1)
plt.title("FFT numpy")
plt.plot(n[0])

plt.subplot(2,3,4)
plt.title("FFT manual")
plt.plot(np.real(man[0]))

plt.subplot(2,3,2)
plt.title("FFT numpy")
plt.plot(n[194])

plt.subplot(2,3,5)
plt.title("FFT manual")
plt.plot(np.real(man[194]))

plt.subplot(2,3,3)
plt.title("FFT numpy")
plt.plot(n[388])

plt.subplot(2,3,6)
plt.title("FFT manual")
plt.plot(np.real(man[388]))

plt.show()













