from collections import Counter
import heapq

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
    # Agregamos todos los símbolos a la pila
    for ch,pr in probs.items():
        # La fila de prioridad está ordenada por
        # prioridad y profundidad
        heapq.heappush(q,(pr,0,ch))

    # Empezamos a mezclar símbolos juntos
    # hasta que la fila tenga un elemento
    while len(q) > 1:
        e1 = heapq.heappop(q) # El símbolo menos probable
        e2 = heapq.heappop(q) # El segundo menos probable
        
        # Este nuevo nodo tiene probabilidad e1[0]+e2[0]
        # y profundidad mayor al nuevo nodo
        nw_e = (e1[0]+e2[0],max(e1[1],e2[1])+1,[e1,e2])
        heapq.heappush(q,nw_e)
    return q[0] # Devolvemos el arbol sin la fila

def make_dictionary(tree):
    res = {} # La estructura que vamos a devolver
    search_stack = [] # Pila para DFS
    # El último elemento de la lista es el prefijo!
    search_stack.append(tree+("",)) 
    while len(search_stack) > 0:
        elm = search_stack.pop()
        if type(elm[2]) == list:
            # En este caso, el nodo NO es una hoja del árbol,
            # es decir que tiene nodos hijos
            
            # El hijo izquierdo tiene "0" en el prefijo
            search_stack.append(elm[2][1]+(prefix+"0",))
            # El hijo derecho tiene "1" en el prefijo
            search_stack.append(elm[2][0]+(prefix+"1",))
            continue
        else:
            # El nodo es una hoja del árbol, así que
            # obtenemos el código completo y lo agregamos
            code = elm[-1]
            res[elm[2]] = code
        pass
    return res

def compress(dic,content):
    res = ""
    # Iteramos sobre cada elemento del archivo de entrada
    for ch in content:
        code = dic[ch]
        res = res + code
    # Agregamos el 1 a la izquierda, y el marcador de final
    # a la derecha
    res = '1' + res + dic['end']
    # Agregamos ceros para que la longitud del resultado
    # sea un múltiplo de 8
    res = res + (len(res) % 8 * "0")
    return int(res,2) # Convertimos a entero! (2 porque es base 2)

def store(data,dic,outfile):
    # Guardamos la cadena de bits en un archivo, que abrimos
    # en modo binario (por eso 'wb')
    outf = open(outfile,'wb')
    pickle.dump(compressed,outf)
    outf.close()

    # Guardamos el diccionario en otro archivo en formato JSON
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
store(compressed,dic,"enocder_huffman")