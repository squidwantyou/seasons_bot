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

N = 4 
W = 280
n_trials = 0
MAX_TRIAL = 3
background_color = "#B9D5F3"

def error(gid = 0,uid=0):
    analysis.send_msg(gid=gid,m="呜呜，又出错了")

def make_puzzle(gid=None, uid=0):
    template_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    answer = list(range(N))
    rd.shuffle(answer)
    answer_str = ""
    for i in answer:
        answer_str = answer_str + template_str[i]

    laoponames, laopofiles = analysis.get_laopo(uid,N)

    a = laopofiles
    nickname = analysis.get_nick_name(None,gid,uid)

    # ABC line
    im1 = Image.new('RGB', (280 * N , 48), background_color)
    draw = ImageDraw.Draw(im1)
    font = ImageFont.truetype('fonts/msyh.ttf', 40)
    for i in range(N):
        draw.text( ( W*(i+0.5),0 ) , template_str[i], font=font, fill="#000000")

    # images line
    imlist = list()
    for b in a :
        im = Image.open(b)
        if im.mode in ('RGBA', 'LA'):
            background = Image.new(im.mode[:-1], im.size, "#FFFFFF")
            background.paste(im, im.split()[-1]) # omit transparency
            im = background
        imlist.append(im)

    width_l =   [ x.width  for x in imlist ]
    height_l  = [ x.height for x in imlist ]
    tmp = list()
    for im in imlist:
        im = im.resize( (W, int( W*im.height*1.0/im.width)), Image.ANTIALIAS ) 
        tmp.append(im)
    imlist = tmp
    
    # quest line
    im2 = Image.new('RGB', (280 * N , 48), background_color)
    draw = ImageDraw.Draw(im2)
    font = ImageFont.truetype('fonts/msyh.ttf', 20)
    text = f"   写出这{N}位的顺序:"
    for i in answer:
        text = text + laoponames[i] + "    "
    text = text[:-3]
    draw.text((0,0), text, font=font, fill="#000000")

    # total
    tW = W * N
    tH = max( height_l ) + 96 

    dst = Image.new('RGB', ( tW, tH ), background_color )
    dst.paste(im1, (0, 0))
    for i in range(N):
        dst.paste( imlist[i], (W*i,48) )

    dst.paste(im2, (0, 48+max(height_l)))

    dst.save(f'data/images/girlquest_{gid}.jpg')

    with open(f'girlquest_answer_{gid}','w') as ofp:
        ofp.write( answer_str )
        ofp.write("\n")
        ofp.write("new")

    return

def analyze_query( answer, query ) :
    query = "".join(query.split())
    assert len(query) >= N
    query = query[:N].upper()
    return query == answer


def fetch_last_puzzle(gid):
    try:
        assert os.path.isfile( f'girlquest_answer_{gid}') 
        lines = open( f'girlquest_answer_{gid}').readlines()
        answer = lines[0].strip()
        status = lines[1]

        return (answer,status)
    except Exception as e:
        print(e)
        return [ "ABC" ,'error' ]

def finish_puzzle(gid):
    try:
        assert os.path.isfile( f'girlquest_answer_{gid}') 
        lines = open( f'girlquest_answer_{gid}').readlines()
        answer = lines[0]
        status = lines[1]
        
        with open( f'girlquest_answer_{gid}', 'w') as ofp:
            ofp.write(answer)
            ofp.write("\n")
            ofp.write("done")
        return

    except Exception as e:
        print(e)
        return [ "ABC" ,'error' ]

# dm                
def dm(message,uid,gid):
    global n_trials
    color = ''
    try:
        color = message.text.split()[1]
    except:
        color = None

    if color == None:
        color = 'new'
    
    if color == 'new':
        make_puzzle( gid = gid,uid=uid)
        m = f'[CQ:image,file=girlquest_{gid}.jpg]'
        analysis.send_msg(m,uid=uid,gid=gid)
        n_trials = 0

    else:
        query = color
        answer,status = fetch_last_puzzle(gid)
        result = analyze_query(answer,query) # analysis new query

        if not result:
            n_trials += 1
            analysis.send_msg(gid=gid,m=f"{color} 不对,您肯定是不认识 ") 
            if n_trials >= MAX_TRIAL:
                analysis.send_msg(gid=gid,m=f"Reach trial times limit. Stop.\nThe Answer is {answer}") 
                finish_puzzle(gid) # finish current puzzle
        else: # if right
            analysis.send_msg(gid=gid,m=f"您TQL，没错，就是 {answer}") 
            finish_puzzle(gid)

