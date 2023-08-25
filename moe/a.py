#!/usr/bin/env python
import sys,os
import requests
from bs4 import BeautifulSoup

url = "https://zh.moegirl.org.cn/Category:%E6%8C%89%E5%A7%93%E6%B0%8F%E5%88%86%E7%B1%BB"

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

ofp = open("cate.list",'w') 
while True:
    r = requests.get(url, headers = headers )
    content = r.text
    soup = BeautifulSoup(content,"html.parser" )
    all_cate = soup.find_all("a","CategoryTreeLabel")
    last_tmp = ""
    for tmp in all_cate:
        ofp.write(tmp.string)
        ofp.write("\n")
        last_tmp = tmp.string
        print(tmp)
    if "乾姓" in last_tmp:
        last_tmp = "宫本姓"
    if  "Zwingli" in last_tmp:
        sys.exit()
    ofp.flush()
    url = f"https://zh.moegirl.org.cn/index.php?title=Category:%E6%8C%89%E5%A7%93%E6%B0%8F%E5%88%86%E7%B1%BB&subcatfrom={last_tmp}"



