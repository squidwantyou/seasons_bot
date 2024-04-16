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


def dianzan(message,uid=0,gid=0):
    print(">>>>> Called dianzan")
    print(f">>>>> select dianzan {message.text}")
    sys.stdout.flush()
    try:
        if len(message.text.split()) > 1 and os.path.isfile(f"/home/ffallrain/seasons_bot/moe/images_all/{message.text.split()[1]}.jpg"):
            name = message.text.split()[1]
            nickname = analysis.get_nick_name(message,gid,uid)
            a = f"/home/ffallrain/seasons_bot/moe/images_all/{name}.jpg"
        else:
            pics = glob.glob("/home/ffallrain/seasons_bot/moe/images_2/*jpg")
            a = rd.choice( pics )
            name = os.path.basename(a).strip(".jpg")
            nickname = analysis.get_nick_name(message,gid,uid)

        im1 = Image.new('RGB', (400, 32), "#FFF6DC")
        draw = ImageDraw.Draw(im1)
        font = ImageFont.truetype('fonts/msyh.ttf', 20)

        text = f"TQL, {analysis.moe_name_back(name)} 给你点个赞!"
        draw.text((0,0), text, font=font, fill="#000000")

        imlist = list()

        im2 = Image.open(a)
        w,h = im2.width, im2.height

        new_w = 300
        new_h = int(h*1.0 * new_w / w)
        im2 = im2.resize( (new_w,new_h) )

        imt = Image.open("thumb.png")
        imt = imt.resize( (100,100) )

        dst = Image.new('RGB', ( 400,  new_h+32 ), "#FFFFFF" )

        dst.paste(im1, (0, 0) )
        dst.paste(im2, (0, 32) )
        dst.paste(imt, (300, int(32 + new_h/2 - 50) ) )
        dst.save('data/images/dianzan.jpg')

        m = "[CQ:image,file=dianzan.jpg]"

        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        sys.stdout.flush()
        analysis.send_msg("你好棒哦",uid=uid,gid=gid)




