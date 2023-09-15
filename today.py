#!/usr/bin/env python
import requests
import json
import re
import analysis
import time
import os


def today(message,uid=0,gid=0):
    try:
        timestr = f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}"
        if not os.path.isfile(f"data/images/news/{timestr}.jpg"):
            os.system(f"wget --no-check-certificate  -O data/images/news/{timestr}.jpg https://xvfr.com/60s.php")

        m = f'[CQ:image,file=news/{timestr}.jpg]'
        analysis.send_msg(m,uid=uid,gid=gid)
        

    except Exception as e:
        print(e)
        analysis.send_msg("今天小触手出了bug.",uid=uid,gid=gid)


# scy('',gid=144744787)
