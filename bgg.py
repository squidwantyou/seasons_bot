#!/usr/bin/env python
import requests
import json
import re
import analysis

apiurl = "https://boardgamegeek.com/xmlapi/search?search=heat"

def ecy(message,uid=0,gid=0):
    try:
        headers = {
            'User-Agent': 'My User Agent 1.0',
            'From': 'youremail@domain.example', 
            'referer':'www.baidu.com'
        }
        data = requests.get(apiurl,headers=headers)
        data=data.content
        import xmltodict
        data = xmltodict.parse(data)
        #data = json.dumps(obj)
        #print(data[0])
        
        for bg in data['boardgames']['boardgame']:
            print(bg)

        import sys
        sys.exit()
        with open("data/images/ecy.jpg",'wb') as ofp:
            ofp.write(data)
        m = f'[CQ:image,file=ecy.jpg]'
        #analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        #analysis.send_msg("啊，那个，有点故障...",uid=uid,gid=gid)

ecy(0,0,0)
