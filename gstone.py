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
        query = " ".join(message.text.split()[1:])
        apiurl = f'https://www.gstonegames.com/game/?keyword={query}'
        headers = {
            'User-Agent': 'My User Agent 11.0',
            'From': 'ffallrain@gmail.com', # This is another valid field,
            'referer':'www.gstonegames.com'
        }

        # search
        data = requests.get(apiurl,headers=headers)
        soup = BeautifulSoup(data.content, 'html.parser')
        bg_list = soup.find_all('div','goods-list')
        
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
            m = f'[CQ:image,file=gstone.png] BGG_ID:{bggid} \n{all_p}'
            analysis.send_msg(m,uid=uid,gid=gid)

            # only return one result 
            break

        if not flag:
            m = f'抱歉，木有找到~'
            analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("摆烂了~",uid=uid,gid=gid)


