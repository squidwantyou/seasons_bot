#!/usr/bin/env python
import requests
import json
import re
import analysis

apiurl = u'https://zh.moegirl.org.cn/灰原哀'

def scy(message,uid=0,gid=0):
    try:
        headers = {
            'User-Agent': 'My User Agent 1.0',
            'From': 'youremail@domain.example', # This is another valid field,
            'referer':'www.baidu.com'
        }
        data = requests.get(apiurl,headers=headers)
        print(data.content.decode("utf-8"))
 #       print(m)

    except Exception as e:
        print(e)

