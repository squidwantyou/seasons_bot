#!/usr/bin/env python
import requests
import json
import re
import analysis

apiurl = "http://www.loliapi.com/bg/"
# apiurl = "https://api.oick.cn/random/api.php?type=pe"

def edwcy(message,uid=0,gid=0):
    print(">>>>> Called edwcy")
    try:
        m = f'[CQ:image,file=edwcy.jpg]'
        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("啊，那个，有点故障...",uid=uid,gid=gid)

