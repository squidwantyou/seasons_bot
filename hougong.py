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


def hougong(message,uid=0,gid=0):
    print(">>>>> Called hougong")
    try:
        pics = glob.glob("/root/moe/images/*jpg")
        a = rd.sample( pics, 5 )
        nickname = analysis.get_nick_name(message,gid,uid)


        im1 = Image.new('RGB', (800, 64), "#FFF6DC")
        draw = ImageDraw.Draw(im1)
        font = ImageFont.truetype('fonts/msyh.ttf', 20)

        text = f"{nickname} 的老婆们 :"
        draw.text((0,0), text, font=font, fill="#000000")
        text = "   " + " ".join( [ os.path.basename(x).strip(".jpg") for x in a ] )
        draw.text((0,32), text, font=font, fill="#000000")

        imlist = list()

        for b in a :
            im2 = Image.open(b)
            imlist.append(im2)


        width_l =   [ x.width  for x in imlist ]
        height_l  = [ x.height for x in imlist ]

        dst = Image.new('RGB', ( sum(width_l), max(height_l) + 64), "#FFF6DC" )
        dst.paste(im1, (0, 0))

        w = 0
        for im in imlist:
            dst.paste(im, (w, 64))
            w += im.width

        dst.save('data/images/hougong.jpg')

        m = "[CQ:image,file=hougong.jpg]"

        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("是个女人就是你老婆么?",uid=uid,gid=gid)





