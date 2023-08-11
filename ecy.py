#!/usr/bin/env python
import requests
import json
import re
import analysis

apiurl = "http://www.loliapi.com/bg/"
# apiurl = "https://api.oick.cn/random/api.php?type=pe"

def ecy(message,uid=0,gid=0):
    print(">>>>> Called ecy")
    try:
        headers = {
            'User-Agent': 'My User Agent 1.0',
            'From': 'youremail@domain.example', 
            'referer':'www.baidu.com'
        }
        data = requests.get(apiurl,headers=headers,verify=False)
        data=data.content
        with open("data/images/ecy.jpg",'wb') as ofp:
            ofp.write(data)
        m = f'[CQ:image,file=ecy.jpg]'
        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("啊，那个，有点故障...",uid=uid,gid=gid)

