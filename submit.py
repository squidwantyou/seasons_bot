#!/usr/bin/env python3
import analysis 
import re

all_text = open("weilantxt/pnbs.txt").read()

a = all_text.split("\n")

for i in a:
    try:
        shangju,xiaju = i.split()
    except:
        continue
    shangju = "/" + shangju
    shangju =  analysis.b64e(shangju.lstrip().strip())  
    xiaju =  analysis.b64e(xiaju.lstrip().strip())  
    print(f"insert into zdy ( query, answer ) values ('{shangju}','{xiaju}') ;")





