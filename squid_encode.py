#!/usr/bin/env python
import sys,os
import PIL
from PIL import Image, ImageFont , ImageDraw

instring = "ABCDEFG"

tmp = """A: 爱丽丝·玛格特罗依德
B: 圣白莲
C: 橙
D: 哆来咪·苏伊特
E: 八意永琳
F: 芙兰朵露·斯卡蕾特
G: G
H: 键山雏
I: 永江衣玖
J: 纯狐
K: 蓬莱山辉夜
L: 莉莉霍瓦特
M: 雾雨魔理沙
N: 封兽鵺
O: 摩多罗隐岐奈
P: 帕秋莉·诺蕾姬
R: 博丽灵梦
S: 十六夜咲夜
T: 比那名居天子
U: 灵乌路空
V: V
W: 若鹭姬
Y: 魂魄妖梦
Z: ZUN"""

tname = dict()
for line in tmp.split("\n"):
    k = line.split()[0].strip(":")
    v = line.split()[1]
    tname[k] = v


W = 140
H = 200

def make_fig(s ):
    imlist = list()
    for c in list(s):
        c = c.upper()
        assert ord("A") <= ord(c) <= ord("Z")
        b = f"data/images/touhou/{tname[c]}.png"
        im = Image.open(b)
        if im.mode in ('RGBA', 'LA'):
            background = Image.new(im.mode[:-1], im.size, "#FFFFFF")
            background.paste(im, im.split()[-1]) # omit transparency
            im = background
        im = im.resize( (W,H) , Image.ANTIALIAS ) 
        imlist.append(im)

    dst = Image.new('RGB', ( W*len(imlist), H), "#FFFFFC" )
    i = 0 
    for im in imlist:
        dst.paste(im, (i*W, 0))
        i += 1
    return dst
    
dst = make_fig(sys.argv[1])
dst.save(sys.argv[2])

