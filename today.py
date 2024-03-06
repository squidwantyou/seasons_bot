#!/usr/bin/env python
import requests
import json
import re
import analysis
import time
import os
import datetime


def today(message,uid=0,gid=0):
    print(">>>>> called today")
    try:
        current = datetime.datetime.now()
        
        if message.text.split()[0] == '/yesterday':
            shift = -1
            query_time = current + datetime.timedelta(days=shift)
        elif len(message.text.split()) > 1:
            shift = int( message.text.split()[1])
            if shift > 20000000:
                year = shift//10000
                month = shift%10000//100
                day = shift%100
                query_time = datetime.datetime(  year=year,month=month,day = day )
            else:
                query_time = current + datetime.timedelta(days=shift)
        else:
            query_time = current

        timestr = f"{query_time.year}-{query_time.month}-{query_time.day}"

        if not os.path.isfile(f"data/images/news/{timestr}.jpg") or len(open(f"data/images/news/{timestr}.jpg").read()) <10 :
            if current == query_time:
                os.system(f"wget --no-check-certificate  -O data/images/news/{timestr}.jpg https://xvfr.com/60s.php")
            else:
                pass

        if os.path.isfile(f"data/images/news/{timestr}.jpg"):
            m = f'[CQ:image,file=news/{timestr}.jpg]'
        else:
            m = f'那是不平凡的一天,小触手也不知道发生了什么'

        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("今天小触手出了bug.",uid=uid,gid=gid)


