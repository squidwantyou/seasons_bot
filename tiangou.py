#!/usr/bin/env python
import requests
import json
import re
import analysis

apiurl = 'https://v.api.aa1.cn/api/tiangou/index.php'

def tiangou(message,uid=0,gid=0):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'From': 'youremail@domain.example', # This is another valid field,
            'referer':'www.baidu.com'
        }
        data = requests.get(apiurl,headers=headers,verify=False)
        #imgurl=json.loads(data.content)['msg']
        imgurl=data.content
        imgurl = imgurl.decode('utf8').lstrip('\n<p>').strip('</p>')
        m = imgurl
        print(m)
        m = f"/rds {m}"
        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("舔狗舔狗，舔到最后，一无所有~",uid=uid,gid=gid)

# scy('',gid=144744787)
