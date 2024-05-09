#!/usr/bin/env python
import requests
import json
import re
import analysis
import random as rd

def zun(message,uid=0,gid=0):
    try:
        ids = [ x.strip() for x in open("zun.list") ]
        i = rd.choice(ids)
        m = f'[CQ:music,type=163,id={i}]'
        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)

