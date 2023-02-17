#!/usr/bin/env python
import subprocess
import sys,os
import analysis

def loop(message,uid=0,gid=0):
    try:
        items = message.text.split()
        delay = int(items[1])
        time = int(items[2])
        interval = int(items[3])
        if time >= 3600*24 or time >=100 or interval < 60 :
            raise Exception

        text = '\'' + " ".join(items[4:]) + '\''
        p  = subprocess.Popen(" ".join( ["nohup", "./send_loop_message.py",str(uid),str(gid), str(delay),str(time),str(interval), text ]) , shell=True )
        stdout, stderr = p.communicate()

    except Exception as e:
        print(e)
        analysis.send_msg("啊!CPU爆炸了...",uid=uid,gid=gid)

