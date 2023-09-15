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

def suijilaogong(message,uid=0,gid=0):
    print(">>>>> Called suijilaopo")
    try:
        laoponames,laopofiles = analysis.get_laogong(uid,1)
        nickname = analysis.get_nick_name(message,uid=uid,gid=gid)
        laoponame = laoponames[0]
        a = laopofiles[0]

        im1 = Image.new('RGB', (400, 32), "#FFF6DC")
        draw = ImageDraw.Draw(im1)
        font = ImageFont.truetype('fonts/msyh.ttf', 20)
        text = f"{laoponame}"
        draw.text((0,0), text, font=font, fill="#000000")


        im2 = Image.open(a)


        width_l =   [ x.width  for x in (im1,im2) ]
        height_l  = [ x.height for x in (im1,im2) ]

        dst = Image.new('RGB', ( max(width_l), sum(height_l) ), "#FFF6DC" )
        h = 0
        for im in (im1,im2):
            dst.paste(im, (0, h))
            h += im.height

        dst.save('data/images/laogong.jpg')

        m = "[CQ:image,file=laogong.jpg]"

        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("遇见美好~",uid=uid,gid=gid)


