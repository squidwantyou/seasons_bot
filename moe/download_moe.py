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

for line in open("moe_caracter.list"):
    line = line.strip()
    if ">>>" in line:
        continue
    print(f"CONDUCT {line}")
    try:
        filename = line.replace("(","@_").replace(")","_@").replace("/","@@")

        if  os.path.isfile(f"images_2/{filename}.jpg"):
            continue
        if  os.path.isfile(f"images_2/{filename}.err"):
            continue

        if os.path.isfile(f"images/{filename}.jpg"):
            os.system(f"cp images/{filename}.jpg images_2/")
            print(f"CP {line}")
            continue

        if os.path.isfile(f"images/{filename}.err"):
            os.system(f"cp images/{filename}.err images_2/")
            print(f"CPERR {line}")
            continue

        
        url = f"https://zh.moegirl.org.cn/{line}"

        r = requests.get(url, headers = headers )
        content = r.text
        soup = BeautifulSoup(content,"html.parser" )

        thiscate = None
        all_cate = soup.find_all("div",class_ = "moe-infobox" )

        if len(all_cate) < 1:
            all_cate = soup.find_all("table",class_ = "moe-infobox" )
        if len(all_cate) < 1:
            all_cate = soup.find_all("table",class_ = "infoboxSpecial" )
        if len(all_cate) < 1:
            all_cate = soup.find_all("div",class_ = "infotemplatebox")
        if len(all_cate) < 1:
            all_cate = soup.find_all("table",class_ = "infobox" )
            for c in all_cate:
                if "width:280px" in c.attrs["style"]:
                    thiscate = c
        else:
            thiscate = all_cate[0]

        if not thiscate:
            print("NOINFOBOX",line)
    #        os.system(f"touch images_2/{filename}.err")
            continue
        if len(all_cate) < 1:
            print("NOINFOBOX",line)
            os.system(f"touch images_2/{filename}.err")
            continue

        thiscate = all_cate[0]
        image = thiscate.find_all("a",class_="image")
        if len(image) < 1:
            print("NOIMAGE Image",line)
            os.system(f"touch images_2/{filename}.err")
            continue
        img = image[0].find_all("img")[0]
        iurl =  img["src"]
        print( iurl )
        r = requests.get(iurl, headers = headers )
        with open(f"images_2/{filename}.jpg",'wb') as ofp:
            ofp.write(r.content)

        sys.stdout.flush()
    except Exception as e:
        print(e)
        continue




