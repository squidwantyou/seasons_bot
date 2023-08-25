#!/usr/bin/env python
import requests
import json
import re
import analysis

apiurl = 'https://v.api.aa1.cn/api/api-wenan-anwei/index.php?type=json'


def anwei(message,uid=0,gid=0):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'From': 'youremail@domain.example', # This is another valid field,
            'referer':'www.baidu.com'
        }
        data = requests.get(apiurl,headers=headers,verify=False)
        imgurl=json.loads(data.content)['anwei']
        #imgurl = "https://" + imgurl.replace(" ","%20")
        m = imgurl
        print(m)
        m = f"/rds {m}"
        analysis.send_msg(m,uid=uid,gid=gid,at=True)

    except Exception as e:
        print(e)
        analysis.send_msg("摸摸~",uid=uid,gid=gid,at=True)


# scy('',gid=144744787)
