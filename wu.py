#!/usr/bin/env python
import requests
import json
import re
import analysis

apiurl = 'https://api.wqwlkj.cn/wqwlapi/kfcyl.php?type=json'
apiurl = 'https://v.api.aa1.cn/api/api-saohua/index.php?type=json'


def wu(message,uid=0,gid=0):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'From': 'youremail@domain.example', # This is another valid field,
            'referer':'www.baidu.com'
        }
        data = requests.get(apiurl,headers=headers)
        imgurl=json.loads(data.content)['saohua']
        #imgurl = "https://" + imgurl.replace(" ","%20")
        m = imgurl
        print(m)
        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("富强、民主、文明、和谐，自由、平等、公正、法治，爱国、敬业、诚信、友善",uid=uid,gid=gid)


# scy('',gid=144744787)
