#!/usr/bin/env python
import requests
import json
import re
import analysis
import random as rd


def cat(message,uid=0,gid=0):
    c = rd.randrange(0,2)
    if c == 0:
        try:
            apiurl = 'https://api.thecatapi.com/v1/images/search?api_key=live_AR2lT9lfSR6LljTYLRyRC378I7kIimjIBPXPhiQKbhjfG4tcri0dOfali15kzF07'
            headers = {
                'User-Agent': 'My User Agent 1.0',
                'From': 'youremail@domain.example', # This is another valid field,
                'referer':'www.google.com'
            }
            data = requests.get(apiurl,headers=headers)
            imgurl=json.loads(data.content)[0]['url']
            m = f'[CQ:image,file={imgurl}]'
     #       print(m)
            analysis.send_msg(m,uid=uid,gid=gid)

        except Exception as e:
            print(e)
            analysis.send_msg("喵~",uid=uid,gid=gid)
    else:
        apiurl = "https://cataas.com/cat"
        try:
            headers = {
                'User-Agent': 'My User Agent 1.0',
                'From': 'youremail@domain.example',
                'referer':'www.google.com'
            }
            data = requests.get(apiurl,headers=headers,verify=False)
            data=data.content
            with open("data/images/cat.jpg",'wb') as ofp:
                ofp.write(data)
            m = f'[CQ:image,file=cat.jpg]'
            analysis.send_msg(m,uid=uid,gid=gid)

        except Exception as e:
            print(e)
            analysis.send_msg("喵~",uid=uid,gid=gid)


# scy('',gid=144744787)
