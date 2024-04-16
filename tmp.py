#!/usr/bin/env python
import requests
import json
import re
import analysis
import sys,os

all_bunny = dict()
for line in open("bunny.txt"):
    line = line.strip("\n")
    line = line.strip("\r")
    line = line.strip("\n")
    line = line.strip("\r")
    a,b = line.strip().split(" x ")
    if a not in all_bunny:
        all_bunny[a] = set()
    if b not in all_bunny:
        all_bunny[b] = set()
    all_bunny[a].add(b)
    all_bunny[b].add(a)
print(all_bunny)
