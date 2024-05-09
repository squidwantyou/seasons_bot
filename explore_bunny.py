#!/usr/bin/env python
import requests
import json
import re
import analysis
import sys,os
import traceback

def seq(a,b):
    if a<b:
        return (a,b)
    else:
        return (b,a)

all_bunny = set()
all_pair = set()
for line in open("bunny.txt"):
    line = line.strip("\n")
    line = line.strip("\r")
    line = line.strip("\n")
    line = line.strip("\r")
    a,b = line.strip().split(" x ")
    all_pair.add( seq(a,b) )
    all_bunny.add(a)
    all_bunny.add(b)

all_count = dict()
for ba in all_bunny:
    for bb in all_bunny:
        if ba<=bb:
            continue
        both = set()
        for bc in all_bunny:
            if seq(ba,bc) in all_pair and seq(bb,bc) in all_pair:
                both.add(bc)
        all_count[ seq(ba,bb) ] = both

filtered = [ x for x in all_count if len(all_count[x]) != 0 ]
sort_key = sorted( filtered, key = lambda x:len(all_count[x]), reverse = True )

revo = dict()

for k in sort_key:
    if k not in all_pair: 
        v = tuple(all_count[k])
        if v not in revo:
            revo[v] = {k,}
        else:
            revo[v].add(k)
            
query = sys.argv[1]

for k in revo:
    for tmp in revo[k]:
        if query in tmp:
            print(">>>>> ", k) 
            print("  -->", tmp)

