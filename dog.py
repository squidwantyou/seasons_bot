#!/usr/bin/env python
import requests
import json
import re
import analysis

apiurl = 'https://api.thedogapi.com/v1/images/search?api_key=live_AR2lT9lfSR6LljTYLRyRC378I7kIimjIBPXPhiQKbhjfG4tcri0dOfali15kzF07'

def dog(message,uid=0,gid=0):
    try:
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
        analysis.send_msg("汪!汪!",uid=uid,gid=gid)

# scy('',gid=144744787)
