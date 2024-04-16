#!/usr/bin/env python
import requests
import json
import re
import analysis
import sys,os
import PIL
from PIL import Image, ImageFont , ImageDraw
import glob
import random as rd


def rds(message,uid=0,gid=0):
    print(">>>>> Called random say")
    print(f">>>>> Called random say {message.text}")
    sys.stdout.flush()
    try:
        if len(message.text.split()) == 1:
            text = f"你要说什么???"
        else:
            text = " ".join( message.text.split()[1:]  )
            tmp = ''
            while True:
                if len(text) == 0:
                    break
                if len(text) >20:
                    tmp = tmp + "\n" + text[:20]
                    text = text[20:]
                else:
                    tmp = tmp + "\n" + text
                    text = ''
            text = tmp
        
        Nl = len(text.split("\n"))

        pics = glob.glob("/home/ffallrain/seasons_bot/moe/images_2/*jpg")
        a = rd.choice( pics )
        name = analysis.moe_name_back(os.path.basename(a).strip(".jpg"))
        laoponames,laopofiles = analysis.get_laopo(uid=uid,n=1)

        a = laopofiles[0]
        name = laoponames[0]
        
        nickname = analysis.get_nick_name(message,gid,uid)

        im1 = Image.new('RGB', (450, 32*Nl), "#FFF6DC")
        draw = ImageDraw.Draw(im1)
        font = ImageFont.truetype('fonts/msyh.ttf', 20)

        tmp = f"{name}: @{nickname}, {text}"
        text = tmp

        draw.text((0,0), text, font=font, fill="#000000")

        imlist = list()

        im2 = Image.open(a)
        w,h = im2.width, im2.height

        new_w = 450
        new_h = int(h*1.0 * new_w / w)
        im2 = im2.resize( (new_w,new_h) )

        dst = Image.new('RGB', ( 450,  new_h + 32*Nl ), "#FFF6DC" )

        dst.paste(im1, (10, 0) )
        dst.paste(im2, (0, 32*Nl) )
        dst.save('data/images/rds.jpg')

        m = "[CQ:image,file=rds.jpg]"

        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        sys.stdout.flush()
        analysis.send_msg("xoxo.sdfljifslefkjsel",uid=uid,gid=gid)



