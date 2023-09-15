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

W = 280

def hougong(message,uid=0,gid=0):
    print(">>>>> Called hougong")
    try:
        laoponames, laopofiles = analysis.get_laopo(uid,5)

        pics = glob.glob("/root/seasons_bot/moe/images_2/*jpg")
        # a = rd.sample( pics, 5 )
        a = laopofiles
        nickname = analysis.get_nick_name(message,gid,uid)


        im1 = Image.new('RGB', (800, 96), "#FFF6DC")
        draw = ImageDraw.Draw(im1)
        font = ImageFont.truetype('fonts/msyh.ttf', 20)

        text = f"五等分的花嫁 -> {nickname} "
        draw.text((0,0), text, font=font, fill="#000000")
        text = "   " + "|".join( laoponames[:3] )
        draw.text((0,32), text, font=font, fill="#000000")
        text = "   " + "|".join( laoponames[3:] )
        draw.text((0,64), text, font=font, fill="#000000")

        imlist = list()

        for b in a :
            im = Image.open(b)
            if im.mode in ('RGBA', 'LA'):
                background = Image.new(im.mode[:-1], im.size, "#FFFFFF")
                background.paste(im, im.split()[-1]) # omit transparency
                im = background
            imlist.append(im)

        imlist = sorted( imlist, key = lambda x:(x.height*1.0/x.width), reverse = True )

        width_l =   [ x.width  for x in imlist ]
        height_l  = [ x.height for x in imlist ]
        
        tmp = list()
        for im in imlist:
            im = im.resize( (W, int( W*im.height*1.0/im.width)), Image.ANTIALIAS ) 
            tmp.append(im)
        imlist = tmp
        
        width_l =   [ x.width  for x in imlist ]
        height_l  = [ x.height for x in imlist ]

        H = height_l[0] + height_l[2] 
        ratio = H*1.0/ ( height_l[1]+ height_l[3]+ height_l[4] ) 
        sW = int( W  * ratio )

        tW = W + sW
        tH = H

        for i in (1,3,4):
        # for im in (imlist[1], imlist[3], imlist[4] ):
            newsize = (sW, int(imlist[i].height*ratio))
            imlist[i] = imlist[i].resize( newsize, Image.ANTIALIAS ) 

        dst = Image.new('RGB', ( tW, tH + 96), "#FFF6DC" )
        dst.paste(im1, (0, 0))

        #w = 0
        #for im in imlist:
        #    dst.paste(im, (w, 96))
        #    w += im.width
        dst.paste( imlist[0], (0,96) )
        dst.paste( imlist[2], (0,96+ imlist[0].height ) )
        dst.paste( imlist[3], (W, 96) )
        dst.paste( imlist[4], (W, 96 + imlist[3].height ) )
        dst.paste( imlist[1], (W, 96 + imlist[3].height + imlist[4].height ) )

        dst.save('data/images/hougong.jpg')

        m = "[CQ:image,file=hougong.jpg]"

        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("是个女人就是你老婆么?",uid=uid,gid=gid)



