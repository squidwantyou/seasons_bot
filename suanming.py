#!/usr/bin/env python
import requests
import json
import re
import analysis
import sys,os
import time
import hashlib
import PIL
from PIL import Image, ImageFont , ImageDraw
import math

def fhash( query ):
    result = hashlib.sha256( query.encode("utf8") ).hexdigest()
    return result

class Yunshi:
    def __init__(self, query, nickname):
        self.const_h = fhash( query )
        self.h = self.const_h
        self.report_images = list()
        self.add_text("Hello," + nickname + ",这是您今天的运势:" )

        self.init_touhou()
        self.lucky_num()
        self.direct()
        self.lucky_color()
        self.lucky_time()
        self.xingzuo()
        self.yiji()
        self.boardgame()
        self.game()
        self.novel()
        self.xinfan()
        self.quanzi()
        self.zhongzu()
        self.zhexue()
        self.food()
        self.yijushi()
        self.puzzlegame()
        self.jianzhen()
        self.avgirl()
        self.program()
        self.touhoumusic()
        self.cnsinger()
        self.add_common("eusinger","今日欧美歌手")
        self.add_common("jpsinger","今日日本歌手")
        self.add_common("mgmusicer","今日音游曲师")
        self.add_common("rockroll","今日摇滚乐队")
        self.fallasleep()
        self.sports()
        self.jrrp()
    
    
    def add_common(self, name, welcome ):
        all_choice = list()
        for line in open(f"suanming.data/{name}.list"):
            all_choice.append(line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"{welcome} : {choice}" )
        pass

    def jrrp(self):
        all_choice = list()
        for i in range(121):
            all_choice.append( f"{i}%" )
        for i in ("Inf", "-Inf", "NaN", "-1%", "没眼看了", "A","B","C","D","枪兵" ):
            all_choice.append( i )
        choice = self.get_choice( all_choice )
        self.add_text(f"今日人品: {choice}" )
        pass

    def sports(self):
        all_choice = list()
        for line in open("suanming.data/sports.list"):
            for j in ("高强度","中强度","低强度","看别人"):
                all_choice.append(j+line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"今日适宜运动 : {choice}" )
        pass


    def fallasleep(self):
        all_choice = list()
        for i in (21,22,23,0,1,2):
            for j in range(60):
                all_choice.append( "%d:%02d"%(i,j) )
        for k in range(20):
            all_choice.append("不睡了")
            all_choice.append("你这个年纪睡得着觉？")
        choice = self.get_choice( all_choice )
        self.add_text(f"最佳入睡时刻 : {choice}" )
        

    def add_text(self, text, color = "#000000" ):
        im1 = Image.new('RGB', (600, 32), "#ffffff")
        draw = ImageDraw.Draw(im1)
        font = ImageFont.truetype('fonts/msyh.ttf', 20)
        draw.text((0,0), text, font=font, fill=color)
        self.report_images.append( im1 )

    def cnsinger(self):
        all_choice = list()
        for line in open("suanming.data/cnsinger.list"):
            all_choice.append(line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"今日华语歌手 : {choice}" )
        pass

    def boardgame(self):
        all_choice = list()
        for line in open("suanming.data/boardgame.list"):
            all_choice.append(line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"今日桌游 : {choice}" )
        pass

    def touhoumusic(self):
        all_choice = list()
        for line in open("suanming.data/touhoumusic.list"):
            all_choice.append(line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"今日车万BGM : {choice}" )
        pass

    def program(self):
        all_choice = list()
        for line in open("suanming.data/program.list"):
            all_choice.append(line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"今日编程语言 : {choice}" )
        pass

    def avgirl(self):
        all_choice = list()
        for line in open("suanming.data/avgirl.list"):
            if len(line.strip()) > 2:
                all_choice.append(line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"今日av女优 : {choice}" )
        pass

    def jianzhen(self):
        all_choice = "1450 自干五 小粉红 吃瓜 反贼 入关 皇汉 润族 左派 保守派 加速加速 逆民 谜语人 乐子人 果粉 神友 精日 印吹".split()
        choice = self.get_choice( all_choice )
        self.add_text(f"今日减震阵营 : {choice}" )
        pass

    def puzzlegame(self):
        all_choice = list()
        for line in open("suanming.data/puzzlegame.list"):
            all_choice.append(line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"今日解谜 : {choice}" )
        pass

    def yijushi(self):
        all_choice = list()
        for line in open("suanming.data/yijushi.list"):
            all_choice.append(line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"每日一句诗 : {choice}" )
        pass

    def food(self):
        from food import breakfast,dinner,other
        all_choice = breakfast 
        zao = self.get_choice( all_choice )
        all_choice = dinner 
        wan = self.get_choice( all_choice )
        all_choice = other 
        oth = self.get_choice( all_choice )
        self.add_text(f"今日最佳饮食 : {zao}+{wan}+{oth} " )
        pass

    def zhexue(self):
        all_choice = list()
        for line in open("suanming.data/zhexue.list"):
            all_choice.append(line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"今日哲学学派 : {choice}" )
        pass

    def zhongzu(self):
        all_choice = list()
        for line in open("suanming.data/zhongzu.list"):
            all_choice.append(line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"今日种族 : {choice}" )
        pass

    def quanzi(self):
        all_choice = list()
        for line in open("suanming.data/quanzi.list"):
            all_choice.append(line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"宜混圈子 : {choice}" )
        pass

    def xinfan(self):
        all_choice = list()
        for line in open("suanming.data/xinfan.list"):
            all_choice.append(line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"今日补番 : {choice}" )
        pass

    def novel(self):
        all_choice = list()
        for line in open("suanming.data/novel.list"):
            all_choice.append(line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"今日轻小说 : {choice}" )
        pass

    def game(self):
        all_choice = list()
        for line in open("suanming.data/game.list"):
            all_choice.append(line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"今日宜玩游戏 : {choice}" )
        pass

    def yiji(self):
        all_choice = "祭祀 安葬 嫁娶 出行 祈福 动土 安床 开光 纳采 入殓 移徙 破土 解除 入宅 修造 栽种 开市 移柩 订盟 拆卸 立卷 交易 求嗣 上梁 纳财 起基 斋醮 赴任 冠笄 安门 修坟 挂匾".split()
        choice = self.get_choice( all_choice )
        self.add_text(f"宜 : {choice}" )
        choice = self.get_choice( all_choice )
        self.add_text(f"忌 : {choice}" )
        pass

    def xingzuo(self):
        all_choice = "白羊座,金牛座,双子座,巨蟹座,狮子座,处女座,天秤座,天蝎座,射手座,魔羯座,水瓶座,双鱼座,蛇夫座,局座,一切星座,一等座".split(",")
        choice = self.get_choice( all_choice )
        self.add_text(f"今日宜交星座:{choice}" )
        

    def lucky_color(self):
        all_choice = list()
        for line in open("suanming.data/color.list"):
            items = line.split("\t")
            all_choice.append( (items[0],items[1],items[2]) )
        choice = self.get_choice( all_choice )
        self.add_text(f"今日幸运颜色:{choice[0]}  {choice[1]}  {choice[2]}", color = choice[2] )

    def lucky_time(self):
        all_choice = list()
        for a in list("子丑寅卯辰巳午未申酉戌亥"):
            for b in ("","一刻","二刻","三刻"):
                all_choice.append( a+b )
        choice = self.get_choice( all_choice )
        self.add_text(f"今日命运时刻:{choice}" )
    
    def direct(self):
        all_choice = "东,南,西,北,东北,西北,东南,西南".split(",")
        choice = self.get_choice( all_choice )
        self.add_text(f"今日幸运方位:{choice}")
        pass

    def lucky_num(self):
        all_choice = range(16)
        choice = self.get_choice( all_choice )
        im1 = Image.new('RGB', (300, 32), "#ffffff")
        draw = ImageDraw.Draw(im1)
        font = ImageFont.truetype('fonts/msyh.ttf', 20)
        draw.text((0,0), f"今日幸运数字: {choice} ", font=font, fill="#000000")
        self.report_images.append( im1 )
    
    def init_touhou(self):
        all_choice = list()
        for line in open("data/images/touhou/list"):
            all_choice.append( line.strip() )
        choice = self.get_choice( all_choice )

        im1 = Image.new('RGB', (300, 32), "#ffffff")
        draw = ImageDraw.Draw(im1)
        font = ImageFont.truetype('fonts/msyh.ttf', 20)
        draw.text((0,0), f"今日老婆: {choice} ", font=font, fill="#000000")
        self.report_images.append( im1 )

        im2 = Image.open(f"data/images/touhou/{choice}.png") 
        self.report_images.append( im2 )
    
    def get_choice(self, all_choice):
        n = len(all_choice)
        n_d = math.ceil( math.log(n,16) )
        if len(self.h) < n_d:
            self.h = self.const_h
        a = int( self.h[:n_d], 16 )
        self.h = self.h[n_d:]
        ratio = int( a*1.0/(16**n_d)*n  )
        return all_choice[ratio] 

    def draw(self):
        pass

    def report(self):
        width_l =   [ x.width  for x in self.report_images ]
        height_l  = [ x.height for x in self.report_images ]

        dst = Image.new('RGB', ( max(width_l), sum(height_l) ), "#ffffff" )
        h = 0
        for im in self.report_images:
            dst.paste(im, (0, h))
            h += im.height

        dst.save('data/images/suanming.jpg')
        m = "[CQ:image,file=suanming.jpg]"
        return(m)

def suanming(message,uid=0,gid=0):
    print(">>>>> Called suanming")
    try:
        items = message.text.split()
        if len(items) > 1:
            salt = items[1]
        else:
            salt = ''

        b = time.gmtime()
        query = salt + str(uid) + str(b.tm_year) +str( b.tm_mon) +str( b.tm_mday ) 
        
        nickname = analysis.get_nick_name(message,gid,uid)

        yunshi = Yunshi( query, nickname )
        m = yunshi.report()
        analysis.send_msg(m,uid=uid,gid=gid)

        # 短评
        ### 幸运数字
        ### 方位
        ### 颜色
        ### 吉时
        ### 星座
        ### 宜
        ### 忌
        ### 车万伴侣 
        ### 桌游
        ### 游戏
        ### 小说
        ### 新番
        ### 圈子
        ### dnd 角色
        ### 哲学
        ### 饮食
        ### 解谜游戏
        ### 女优
        ### 诗歌
        ### 建镇阵营
        ### 幸运优
        ### 编程语言
        ### touhou music
        ### eu singer
        ### rockroll
        ### music game musisian
        ### cn歌手
        ### 运动时间
        ### 入睡时刻
        # 圣经
        # 幸运字
        # 表白用语
        # 水群强度


    except Exception as e:
        print(e)
        analysis.send_msg("诸事皆宜...",uid=uid,gid=gid)




