#!/usr/bin/env python
import requests
import json
import re
import analysis

apiurl = 'https://api.wqwlkj.cn/wqwlapi/kfcyl.php?type=json'


def xqs(message,uid=0,gid=0):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'From': 'youremail@domain.example', # This is another valid field,
            'referer':'www.baidu.com'
        }
        data = requests.get(apiurl,headers=headers)
        imgurl=json.loads(data.content)['msg']
        #imgurl = "https://" + imgurl.replace(" ","%20")
        m = imgurl
        print(m)
        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("更多欢乐尽在全拱门~",uid=uid,gid=gid)


# scy('',gid=144744787)
