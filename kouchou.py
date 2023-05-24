#!/usr/bin/env python
import requests
import json
import re
import analysis
import random as rd


def kouchou(message,uid=0,gid=0):
    apiurl = 'https://v.api.aa1.cn/api/api-wenan-ktff/index.php'
        
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'From': 'youremail@domain.example', # This is another valid field,
            'referer':'www.baidu.com'
        }
        
        t = rd.choice( [1,2,3,4,5] )
        aapiurl = apiurl + f"?type={t}"
        
        data = requests.get(aapiurl,headers=headers)
        imgurl=json.loads(data.content,strict=False)['text']
        #imgurl = "https://" + imgurl.replace(" ","%20")
        m = imgurl
        print(m)
        analysis.send_msg(m,uid=uid,gid=gid,at=True)

    except Exception as e:
        print(e)
        analysis.send_msg("你萌死了~",uid=uid,gid=gid,at=True)


# scy('',gid=144744787)
