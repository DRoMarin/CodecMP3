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

# INGRESO
archivo = 'test_audio.wav'
faudio, audio = waves.read(archivo)


def IFFT_64(x):
    fft_size=len(x)//2 
    ifft_out=[0]*64

    for index in range(0,len(x)):
        x[index] = complex((x[index]&65280)/256,(x[index]&255))*416;
        if index < 2000 :
    	    print(x[index])
    

    
    for bloque_index in range(0,fft_size,int(64/2)):
        bloque_temp=x[bloque_index:bloque_index+int(64/2)]
        output_temp=np.fft.irfft(bloque_temp)
        if bloque_index==0:
            ifft_out=output_temp
        else: 
            ifft_out=np.concatenate((ifft_out,output_temp))  
    ifft_out=np.asarray(np.around(ifft_out/416), dtype = int)
    return ifft_out*32




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

