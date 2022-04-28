#!/usr/bin/env python3
import sys
import json
import pickle


def decode(dic, bitstr):
    res = []
    length = bitstr.bit_length() - 1
    if bitstr >> length != 1:
        raise Error("Corrupt file!")
    done = False
    while length > 0 and not done:
        shift = length - 1
        while True:
            num = bitstr >> shift
            bitnum = bin(num)[3:] # Quitamos '0b1' - el 1 inicial y el 0b de formato
            if bitnum not in dic:
                shift -= 1
                continue
            char = dic[bitnum]
            if char == 'end':
                done = True
                break
            res.append(char)
            bitstr = bitstr - ((num - 1) << shift)
            length = shift
    return ''.join(res)


infile="encoder_huf"
f = open(infile+".dic")
dic = json.load(f)
nwdic = {}
for i,e in dic.items(): nwdic[e] = i
f.close()

f = open(infile,'rb')
bstr = pickle.load(f)
f.close()

content = decode(nwdic,bstr)

f = open("decoder_huf",'w')
f.write(content)
f.close()
print("File decompressed!")