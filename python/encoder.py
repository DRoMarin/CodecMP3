from decimal import ROUND_UP
from tkinter import N
import numpy as np
import matplotlib.pyplot as plt
from cmath import exp, log, pi, cos, sin
import scipy.io.wavfile as waves
import heapq
from collections import Counter
import pickle
import json

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


def tohex(val, nbits):
    return hex((val) & (2**nbits -1))


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
         
    fft_out = fft_out/416
    return fft_out

def get_probabilities(content):
    total = len(content) + 1 # Agregamos uno por el caracter FINAL
    print("content",len(content))
    c = Counter(content)
    res = {}
    for char,count in c.items():
        res[char] = float(count)/total
    res['end'] = 1.0/total
    return res

def make_tree(probs):
    q = []
    for ch,pr in probs.items():
        # La fila de prioridad está ordenada por prioridad y PROFUNDIDAD
        heapq.heappush(q,(pr,0,ch))

    while len(q) > 1:
        e1 = heapq.heappop(q)
        e2 = heapq.heappop(q)
        nw_e = (e1[0]+e2[0],max(e1[1],e2[1])+1,[e1,e2])
        heapq.heappush(q,nw_e)
    return q[0]

def make_dictionary(tree):
    res = {}
    search_stack = []
    search_stack.append(tree+("",)) # El último elemento de la lista es el prefijo!
    while len(search_stack) > 0:
        elm = search_stack.pop()
        if type(elm[2]) == list:
            prefix = elm[-1]
            search_stack.append(elm[2][1]+(prefix+"0",))
            search_stack.append(elm[2][0]+(prefix+"1",))
            continue
        else:
            res[elm[2]] =str(int('1'.join(elm[-1]),2))
            #print(a)
        pass
    return res

def compress(dic,content):
    compressed=[]
    for ch in content:
        code = dic[ch]
        compressed.append(code)
        #print(ch,code)
    return compressed

def store(compressed,dic,outfile):
    # Lo guardamos en un archivo
    outf = open(outfile+".txt",'w')
    for element in compressed:
        outf.write(element + "\n")
    outf.close()
    # Guardamos el diccionario en otro archivo
    outf = open(outfile+".dic",'w')
    json.dump(dic,outf)
    outf.close()
    pass


fft=FFT_64(audio)
cont=' '.join([str(item) for item in fft])

# Calculamos la distribución de probabilidad para cada símbolo
probs = get_probabilities(cont)
# Construimos el árbol de parseo! : )
tree = make_tree(probs)

# Construimos el diccionario para codificar
dic = make_dictionary(tree)

# Codificamos el contenido del archivo
compressed = compress(dic,cont)
#print(compressed)
# Guardamos todo en disco!
store(compressed,dic,"encoder")

print("Archivo comprimido!")
