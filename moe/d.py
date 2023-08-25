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


for line in open("caracter.list"):
    line = line.strip()
    filename = line.replace("(","@_").replace(")","_@").replace("/","@@")

    if  os.path.isfile(f"images/{filename}.jpg"):
        continue
    if  not os.path.isfile(f"images/{filename}.err"):
        continue

    print(f"CONDUCT {line}")
    
    url = f"https://zh.moegirl.org.cn/{line}"

    r = requests.get(url, headers = headers )
    content = r.text
    soup = BeautifulSoup(content,"html.parser" )
    all_cate = soup.find_all("table",class_ = "moe-infobox" )
    if len(all_cate) < 1:
        print("NOINFOBOX",line)
#        os.system(f"touch images/{filename}.err")
        continue
    thiscate = all_cate[0]
    image = thiscate.find_all("a",class_="image")
    if len(image) < 1:
        print("NOIMAGE Image",line)
#        os.system(f"touch images/{filename}.err")
        continue
    img = image[0].find_all("img")[0]
    iurl =  img["src"]
    print( iurl )
    r = requests.get(iurl, headers = headers )
    with open(f"images/{filename}.jpg",'wb') as ofp:
        ofp.write(r.content)
    os.system(f"rm images/{filename}.err")
    sys.stdout.flush()




