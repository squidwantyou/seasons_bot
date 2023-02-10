#!/usr/bin/env python
import subprocess
import sys,os
import analysis
import random as rd

def echo(message,uid=0,gid=0):
    try:
        items = message.text.split()[1:]
        c = " ".join(items)
        analysis.send_msg(c,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("?",uid=uid,gid=gid)

