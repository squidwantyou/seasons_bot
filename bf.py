#!/usr/bin/env python
import requests
import json
import re
import analysis
import sys,os
import subprocess

MAX_L = 1024

def bf(message,uid=0,gid=0):
    print(">>>>> Called bf")
    try:
        subp = subprocess.Popen("./bf",stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=False)
        items = message.text.split()
        i = message.text.lstrip( items[0] ).lstrip().strip()
        i = i.replace("\n","")
        i = i.replace("&#91;","[")
        i = i.replace("&#93;","]")
        assert "," not in i
        assert len(i)<MAX_L
        j = i.encode("ascii")
        out,err = subp.communicate(j,timeout=1)
        out = out.decode("ascii")
        subp.terminate()         
        analysis.send_msg(out,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("[+.><.-]",uid=uid,gid=gid)

