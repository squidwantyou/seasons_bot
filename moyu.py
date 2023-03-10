#!/usr/bin/env python
import requests
import json
import re
import analysis

apiurl = "https://api.vvhan.com/api/moyu"

def moyu(message,uid=0,gid=0):
    try:
        headers = {
            'User-Agent': 'My User Agent 1.0',
            'From': 'youremail@domain.example', # This is another valid field,
            'referer':'www.baidu.com'
        }
        data = requests.get(apiurl,headers=headers)
        data=data.content
        with open("data/images/moyu.jpg",'wb') as ofp:
            ofp.write(data)
        m = f'[CQ:image,file=moyu.jpg]'
        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("好好工作，别摸了",uid=uid,gid=gid)

