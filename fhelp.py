#!/usr/bin/env python
import requests
import json
import re
import analysis

def fhelp(message,uid=0,gid=0):
    try:
        m = '所有口令：\n'
        for line in open("api_puzzle.py"):
            if "true_startswith" in line:
                a = re.findall( "\'(.*?)\'",line)
                m = m + " ".join(list(a)) + "\n"
        m += "注：同一行的口令作用完全相同（\n"

        analysis.send_msg(m,uid=uid,gid=gid,to_image = True)
    except Exception as e:
        print(e)

