#!/usr/bin/env python
import subprocess
import sys,os
import analysis

def delay(message,uid=0,gid=0):
    try:
        items = message.text.split()
        time = int(items[1])
        if time >= 3600*24:
            raise Exception

        text = '\'' + " ".join(items[2:]) + '\''
        p  = subprocess.Popen(" ".join( ["nohup", "./send_delay_message.py",str(uid),str(gid), str(time), text ]) , shell=True )
        stdout, stderr = p.communicate()

    except Exception as e:
        print(e)
        analysis.send_msg("啊!CPU过热了...",uid=uid,gid=gid)

