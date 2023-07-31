#!/usr/bin/env python
import requests
import json
import re
import analysis

apiurl = 'https://api.wqwlkj.cn/wqwlapi/kfcyl.php?type=json'
apiurl = 'https://v.api.aa1.cn/api/api-saohua/index.php?type=json'
apiurl = 'https://zj.v.api.aa1.cn/api/bk/'


def history(message,uid=0,gid=0):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'From': 'youremail@domain.example', # This is another valid field,
            'referer': 'https://api.aa1.cn/'
        }
        data = requests.get(apiurl,headers=headers)
        imgurl=json.loads(data.content)['msg']
        #imgurl = "https://" + imgurl.replace(" ","%20")
        m = imgurl
        print(m)
        if not m:
            raise Exception

        analysis.send_msg(m,uid=uid,gid=gid)
        

    except Exception as e:
        print(e)
        analysis.send_msg("今天小触手出了bug.",uid=uid,gid=gid)


# scy('',gid=144744787)
