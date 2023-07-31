#!/usr/bin/env python
import re

infile = "tmp"
line = open(infile).readline()

pat = re.compile("\>(\d+.*?)\<\/h2\>")

s = pat.findall( line )

for  i in s:
    print(i)
