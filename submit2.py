#!/usr/bin/env python3
import analysis 
import re

all_text2 = open("weilantxt/pnbs2.txt").read()
a = all_text2.split("\n")

for i in a:
    try:
        shangju,xiaju = i.split()
        shangju = "/" + shangju
        shangju =  analysis.b64e(shangju.lstrip().strip())  
        xiaju =  analysis.b64e(xiaju.lstrip().strip())  
        print(f"delete from zdy where query='{shangju}' ;")
    except:
        continue





