#!/usr/bin/env python
import sys,os
import random as rd
import requests
import json

gid = 144744787
url = 'http://0.0.0.0:5700/get_msg'
#requests.post( url=url, data=data )
headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.example', # This is another valid field,
    'referer':'www.baidu.com'
}
data = requests.get("https://api.xiaobaibk.com/api/pic/?pic=meizi",headers=headers)
data=data.content
with open("data/images/scy.jpg",'wb') as ofp:
    ofp.write(data)
import re

sys.exit()
pat = re.compile('getimagesize\\(((?:.|\n|\r).*)')
imgurl = re.search(pat, data)[1].strip()
m = f'[CQ:image,file={imgurl},c=3,cache=0]'
data = {'group_id': gid  , 'message':m} 
url = 'http://0.0.0.0:5700/send_group_msg'
requests.post( url=url, data=data )
