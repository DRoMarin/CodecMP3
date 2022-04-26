from decimal import ROUND_UP, InvalidContext
from tkinter import N
import numpy as np
import matplotlib.pyplot as plt
import time
from cmath import exp, log, pi, cos, sin
import scipy.io.wavfile as waves
from typing import List
import csv


archivo = 'test_audio.wav'
faudio, audio = waves.read(archivo)

with open("audio.txt") as File:
    #total_rows = sum(1 for row in File)
    x=[0]*12448*2
    index=0
    for row in File:
        x[index]=int(row)
        index=index+1
      


waves.write("audio1.wav", 8000, np.array(audio))
waves.write("audio2.wav", 8000, np.array(x))


plt.subplot(2,1,1)
plt.title("Audio")
plt.plot(audio)

plt.subplot(2,1,2)
plt.title("Audio texto")
plt.plot(x)

plt.show()