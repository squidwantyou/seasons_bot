#!/usr/bin/env python
import sys,os
import importlib
sys.path.append("..")
import analysis


infile = "moe_caracter_group.list"

moe = dict()

current = None

for line in open(infile):
    line = line.strip()
    filename = line.replace("(","@_").replace(")","_@").replace("/","@@")
    if ">>>>>" in line:
        current = line.split()[1]
    else:
        if not os.path.isfile(f"/root/seasons_bot/moe/images_2/{filename}.jpg"):
            continue
        if current not in moe:
            moe[current] = set()
            moe[current].add( filename )
        else:
            moe[current].add( filename )

# analysis.source_mysql(f"DELETE FROM  moe_list ")
for k in moe:
    if len(moe[k])==0:
        continue
    print(k)
    c = analysis.b64e( "\t".join(moe[k]))  
    k = analysis.b64e(k)
    # analysis.source_mysql(f"INSERT INTO moe_list ( xp, list ) VALUES ( '{k}', '{c}' )")
