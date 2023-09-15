#!/usr/bin/env python
import sys,os
import re


for line in open("api_puzzle.py"):
    if "true_startswith" in line:
        a = re.findall( "\'(.*?)\'",line)
        print(" ".join(list(a)))
