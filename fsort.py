#!/usr/bin/env python
import subprocess
import sys,os
import analysis
import random as rd

def fsort(message,uid=0,gid=0):
    try:
        items = message.text.split()[1:]
        rd.shuffle(items)
        c = " ".join(items)
        analysis.send_msg(c,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("好难排序啊",uid=uid,gid=gid)

