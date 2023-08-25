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

ofp = open("new_moe.list",'w') 

for line in open("moe.list"):

    line = line.strip()
    print(line)
    
    url = f"https://zh.moegirl.org.cn/Category:{line}"

    known = list()
    r = requests.get(url, headers = headers )
    content = r.text
    # print(content)
    soup = BeautifulSoup(content,"html.parser" )
    all_cate = soup.find_all("div",class_ = re.compile("CategoryTreeItem") )
    last_tmp = ""
    for cate in all_cate:
        for tmp in cate.find_all("a",class_ = "CategoryTreeLabel" ):
            ofp.write(tmp.string)
            ofp.write("\n")
            print(tmp.string)

        # ofp.flush()
        # break
        # if last_tmp in known:
        #     break
        # else:
        #     known.append(last_tmp)

        # url = f"https://zh.moegirl.org.cn/index.php?title=Category:{line}&subcatfrom={last_tmp}"



