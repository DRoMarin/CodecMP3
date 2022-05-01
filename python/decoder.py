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
import json
import pickle

# INGRESO
archivo = 'test_audio.wav'
faudio, audio = waves.read(archivo)

infile="encoder"
f = open(infile+".dic")
dic = json.load(f)
nwdic = {}
for i,e in dic.items(): nwdic[e] = i
f.close()

f = open("encoder.txt")
codes=[]
for code in f:
    codes.append(code)
f.close()




def decode(val,dic):
    for key, value in dic.items():
        if int(val) == int(value):
           return key

def huffman_decode(codes,dic):
    fft=[0]*12448*2
    index=0
    complejo=[]
    for code in codes:
        char=decode(code,dic)
        if int(code)==427 or int(code)==7935:
            complejo=complex(''.join(complejo))
            fft[index]=complejo
            complejo=[]
            index=index+1
        else:
            complejo.append(char)
    return fft

fft=huffman_decode(codes,dic)
print(len(fft))


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
    ifft_out=ifft_out*416
    return ifft_out

man=IFFT_64(fft)



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

