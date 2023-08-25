#!/usr/bin/env python
import sys,os
import requests
from bs4 import BeautifulSoup
import re

headers =  {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6,lb;q=0.5",
    "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "referrer": "https://zh.moegirl.org.cn/m",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "body": "",
    "method": "GET",
    "mode": "cors",
    "credentials": "include",
}

os.system("mkdir images_2")
os.system("mkdir images_2/men")

for line in open("men.list"):
    line = line.strip()
    print(f"CONDUCT {line}")
    filename = line.replace("(","@_").replace(")","_@").replace("/","@@")

    if  os.path.isfile(f"images_2/{filename}.jpg"):
        os.system(f"mv images_2/{filename}.jpg images_2/men/")
        continue
    if  os.path.isfile(f"images_2/{filename}.err"):
        os.system(f"mv images_2/{filename}.err images_2/men/")
        continue

