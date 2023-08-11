#!/usr/bin/env python
import requests
import json
import re
import analysis

#apiurl = "https://tuapi.eees.cc/api.php?category=meinv"
apiurl = 'https://3650000.xyz/api/?type=json'
apiurl = "https://api.xiaobaibk.com/api/pic/?pic=meizi"



def scy(message,uid=0,gid=0):
    try:
        headers = {
            'User-Agent': 'My User Agent 1.0',
            'From': 'youremail@domain.example', # This is another valid field,
            'referer':'www.baidu.com'
        }
        data = requests.get(apiurl,headers=headers)
        if True:
            with open("data/images/scy.jpg","wb") as ofp:
                ofp.write( data.content )
            m = f'[CQ:image,file=scy.jpg]'
        else:
            imgurl=json.loads(data.content)['url']
            m = f'[CQ:image,file={imgurl}]'
        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("愚蠢的三次元也故障",uid=uid,gid=gid)

# scy('',gid=144744787)
