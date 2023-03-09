#!/usr/bin/env python
import subprocess
import sys,os
import analysis

def loop(message,uid=0,gid=0):
    try:
        items = message.text.split()
        time = int(items[1])
        interval = int(items[2])
        if time >10 or time * interval > 3600 :
            raise Exception

    
        text = '\'' + " ".join(items[3:]) + '\''
        p  = subprocess.Popen(" ".join( ["nohup", "./send_loop_message.py",str(uid),str(gid),str(time),str(interval), text ]) , shell=True )
        stdout, stderr = p.communicate()

    except Exception as e:
        print(e)
        analysis.send_msg("啊!CPU爆炸了...",uid=uid,gid=gid)

