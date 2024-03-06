#!/usr/bin/env python
import requests
import json
import re
import analysis
from bs4 import BeautifulSoup
import sys

def gstone(message,uid=0,gid=0):
    try:
        # analyze query
        # query = " ".join(message.text.split()[1:])
        apiurl = f'https://www2.javdock.com/ja/video/arm-038/'
        headers = {
            'referer':'www.google.com',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6,lb;q=0.5",
            "Cache-Control": "max-age=0",
            "Cookie": "_scribe=true; _gid=GA1.2.867876680.1700618216; _ga_5V8QD089K8=GS1.1.1700618216.1.1.1700620073.0.0.0; _ga=GA1.1.57459727.1700618216; cf_clearance=FPSxDuadOeLaQRzvY1dkH.nnImBuSlvSq4AiqD9FMow-1700620073-0-1-53eb7c43.84e2f411.4ea23a3-0.2.1700620073",
            "If-Modified-Since":"Wed, 22 Nov 2023 01:56:54 GMT",
            "Sec-Ch-Ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Linux",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        }

        # search
        data = requests.get(apiurl,headers=headers)
        soup = BeautifulSoup(data.content, 'html.parser')
        bg_list = soup.find_all('img','data-no-lazy')
        print(bg_list[0])
        return
        
        # iterate board game
        flag = False
        for bg in bg_list:
            flag = True
            # get cover image
            a = bg.find_all('a')[0]
            cover_url = "http:" + a.find_all('img')[0]['src']
            data = requests.get(cover_url,headers=headers)
            with open("data/images/gstone.png",'wb') as ofp:
                ofp.write(data.content)

            # get board game page
            href = "https://www.gstonegames.com" + a["href"]
            data = requests.get(href,headers=headers)
            isoup = BeautifulSoup(data.content, 'html.parser')
            
            # get name and tags
            title_div = isoup.find_all('div','details-title')[0]        
            name = title_div.find_all('h2')[0].text
            tags = " ".join( [ x.text for x in title_div.find_all('p')[0].find_all('a')] )

            # get score and rank
            score_div = isoup.find_all('div','ddettop-right')[0]
            score = score_div.find_all('p')[0].text
            rank = score_div.find_all('span')[0].text

            # get number players
            #recommand = list()
            #support = list()
            #for line in data.content:
            #    if "playerNumList:" in line:
            #        tmp = line.split(":")[1].strip(",")
            #        tmp = tmp.lstrip("{").strip("}")
            #        for i in tmp.split(","):
            #            key,value = i.split(":")
            #            if value=="1":
            #                support.append( key.lstrip("\"").strip("\"") )
            #            if value=="2":
            #                recommand.append( key.lstrip("\"").strip("\"") )
    
            # get programa info 
            all_p = list()
            for div in isoup.find_all('div','programa01'):
                for p in div.find_all('p'):
                    all_p.append( p.text )
            all_p = "\n".join(all_p)
                
            # get bgg id
            pdiv = isoup.find_all('div','part-left')[0]
            bgg = None
            for ahref in pdiv.find_all('a'):
                if not ahref.has_attr("href"):
                    continue
                href = ahref["href"]
                if "boardgamegeek" in href:
                    bgg = href
                    break 
            try:
                bggid = int(bgg.split("/")[-1])
            except:
                bggid = 0

            # output
            m = f'[CQ:image,file=gstone.png]' # \n{name}\n{tags}\nScore {score} {rank}\nBGG_ID {bggid}\n{all_p}'
            #analysis.send_msg(m,uid=uid,gid=gid)
            m = f'{name}\n{tags}\nScore {score} {rank}\nBGG_ID {bggid}\n{all_p}'
            #analysis.send_msg(m,uid=uid,gid=gid,to_image=True)

            # only return one result 
            break

        if not flag:
            m = f'抱歉，木有找到~'
            #analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        #analysis.send_msg("摆烂了~",uid=uid,gid=gid)


gstone("")



