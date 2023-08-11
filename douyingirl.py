#!/usr/bin/env python
import requests
import json
import re
import analysis

apiurl = 'https://zj.v.api.aa1.cn/api/video_dyv2'
apiurl = 'https://v.api.aa1.cn/api/api-dy-girl/index.php?aa1=json'
apiurl = 'https://v.api.aa1.cn/api/api-girl-11-02/index.php?type=json'
apiurl = 'https://tucdn.wpon.cn/api-girl/index.php?wpon=json'

def douyingirl(message,uid=0,gid=0):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'From': 'youremail@domain.example', # This is another valid field,
            'referer':'www.baidu.com'
        }
        data = requests.get(apiurl,headers=headers,verify=False)
        imgurl=json.loads(data.content)['mp4'].lstrip("//")
        imgurl = "https://" + imgurl.replace(" ","%20")
        if False:
            m = f'[CQ:video,file={imgurl},c=3]'
            print(m)
        else:
            with open("data/videos/girl.mp4",'wb') as ofp:
                data = requests.get(imgurl,headers=headers,verify=False)
                ofp.write( data.content )
                m = f'[CQ:video,file=girl.mp4]'
        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("小姐姐不在呢~",uid=uid,gid=gid)


# scy('',gid=144744787)
