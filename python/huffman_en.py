#!/usr/bin/env python3
import sys
import heapq
from collections import Counter
import pickle
import json

def get_probabilities(content):
    total = len(content) + 1 # Agregamos uno por el caracter FINAL
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
            res[elm[2]] = elm[-1]
        pass
    return res

def compress(dic,content):
    res = ""
    for ch in content:
        code = dic[ch]
        res = res + code
        print(ch,code)
    res = '1' + res + dic['end'] # Agregamos el caracter final y el 1 inicial
    res = res + (len(res) % 8 * "0") # Agregamos ceros para convertir en multiplo de 8
    return int(res,2)

def store(data,dic,outfile):
    # Lo guardamos en un archivo
    outf = open(outfile,'wb')
    pickle.dump(compressed,outf)
    outf.close()

    # Guardamos el diccionario en otro archivo
    outf = open(outfile+".dic",'w')
    json.dump(dic,outf)
    outf.close()
    pass


inf = open('encoder.txt')
cont = inf.read()
inf.close()
# Calculamos la distribución de probabilidad para cada símbolo
probs = get_probabilities(cont)
# Construimos el árbol de parseo! : )
tree = make_tree(probs)
# Construimos el diccionario para codificar
dic = make_dictionary(tree)
# Codificamos el contenido del archivo
compressed = compress(dic,cont)
# Guardamos todo en disco!
store(compressed,dic,"encoder_huf")

print("Archivo comprimido!")