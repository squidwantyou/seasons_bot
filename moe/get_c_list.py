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


ofp = open("moe_caracter_group.list",'w') 

for line in open("all_moe.list"):
    try:
        line = line.strip()
        print(">>>>> " ,line)
        ofp.write(f">>>>> {line}\n")
        
        url = f"https://zh.moegirl.org.cn/Category:{line}"

        while True:
            known = list()
            r = requests.get(url, headers = headers )
            content = r.text
            # print(content)
            soup = BeautifulSoup(content,"html.parser" )
            all_cate = soup.find_all("div",class_ = re.compile("mw-category.*") )
            last_tmp = ""
            for cate in all_cate:
                for tmp in cate.find_all("li"):
                    ofp.write(str(tmp.string))
                    ofp.write("\n")
                    last_tmp = tmp.string
                    print(tmp.string)

            ofp.flush()
            break
            if last_tmp in known:
                break
            else:
                known.append(last_tmp)

            url = f"https://zh.moegirl.org.cn/index.php?title=Category:{line}&subcatfrom={last_tmp}"
    except Exception as e :
        print("ERROR,line,e")


