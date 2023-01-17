#!/usr/bin/env python
import requests
import json
import re
import analysis

apiurl = "https://img.paulzzh.com/touhou/random"

def touhou(message,uid=0,gid=0):
    try:
        headers = {
            'User-Agent': 'My User Agent 1.0',
            'From': 'youremail@domain.example', # This is another valid field,
            'referer':'www.baidu.com'
        }
        data = requests.get(apiurl,headers=headers)
        data=data.content
        with open("data/images/touhou.jpg",'wb') as ofp:
            ofp.write(data)
        m = f'[CQ:image,file=touhou.jpg]'
        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("哇~~~卡在隙间里了啦！~",uid=uid,gid=gid)

