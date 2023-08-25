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
        self.add_text(f">>>>>>>----------------------->")
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
        self.add_common("comic","今日漫画")
        self.add_common("movie","今日电影")
        self.add_common("chaodai","最佳穿越朝代")
        self.fallasleep()
        self.sports()
        self.jrrp()
        self.attack()
        self.majong()
        self.add_text(f">>>>>>>----------------------->")
    
    
    def add_common(self, name, welcome ):
        all_choice = list()
        for line in open(f"suanming.data/{name}.list"):
            all_choice.append(line.strip())
        choice = self.get_choice( all_choice )
        self.add_text(f"{welcome} : {choice}" )
        pass

    def majong(self):
        self.add_text(f"今天也好好好打麻将, 您的幸运雀士:" )

        # chapterone
        all_choice = list()
        for line in open("data/images/majsoul/list"):
            all_choice.append( line.strip() )
        choice = self.get_choice( all_choice )
        im2 = Image.open(f"data/images/majsoul/{choice}.png") 
        im2 = im2.resize( (300, int(im2.height *1.0/im2.width * 300 ) ) )
        self.report_images.append( im2 )

        # yakuman
        all_yakuman = "天和,地和,四暗刻,国士无双,九莲宝灯,大三元,字一色,绿一色,清老头,小四喜,四杠子,四暗刻单骑,国士无双十三面,纯正九莲宝灯,大四喜".split(",")
        all_yakuman.append("累计役满")
        all_yakuman.append("役满?做梦吧你")
        yakuman = self.get_choice( all_yakuman )
        self.add_text(f"今日役满: {yakuman}" )

        all_condition = [ 
	    [ "拉新人打牌", "对方战斗力不足","被新人嚎成四位", ],
	    [ "焚香沐浴更衣", "排除毒素一身轻松","会把嚎运洗掉",] ,
	    [ "吃东西打牌", "谈笑间樯橹灰飞烟灭","顺势一波直接吃四", ],
	    [ "打牌时闲聊", "其他人频频判断失误","没有人回应话题，气氛尴尬", ],
	    [ "在雨天打麻将", "场地魔法卡！","淅淅沥沥拖拖拉拉毫无进张", ],
	    [ "与亲家对攻", "亲家都是大愚形空听不要虚","铳亲地狱绝张亲跳一波被带走", ],
	    [ "强凹役满", "神进张找回自信","打点再高，也怕断幺，牌型再吊，一番撂倒", ],
	    [ "招募新人", "你面前这位有成为雀士的潜质","打牌？斗地主？", ],
	    [ "去和新组织打", "让开，我要和他们谈笑风生","朱门酒肉臭，路有冻死骨", ],
	    [ "拒绝约战邀请", "每个月总有那么三十几天不想动","此时不战更待何时！", ],
	    [ "提出打钱", "千五标准只够塞牙缝","千一输光内裤", ],
	    [ "正午打牌", "吃我旭日东升啦！","不忍直视……", ],
	    [ "搓实体麻将", "甩棒拍桌轻松愉快","手抖眼斜强行诈和", ],
	    [ "搓网络麻将", "欲穷升段路，凤凰一日游","右4开黑携手三四", ],
	    [ "调整对局思路", "重拾对雀力的信心","自断经脉雀力尽失", ],
	    [ "做超过跳满的牌", "大力出奇迹，杠出个未来","强做跳满铳倍满", ],
	    [ "打比赛", "天下无双大杀四方","你的发挥如同天凤AI水平", ],
	    [ "靠科学打牌", "判断精准如有神助","看运气的垃圾游戏好比永远是对的", ],
	    [ "连续战斗", "一路高歌猛进","把吃回来的PT吐出去", ],
	    [ "缩着打", "怂出一片天","有和无铳四", ],
	    [ "提高立直率", "压着别家往死里打","不立直铳也要送根棒子", ],
	    [ "提高副露率", "侵略如火其急如风","三副露no听对战三家立直", ],
	    [ "终局狂日", "你将带头冲锋","自古南三出GG", ],
	    [ "愚形听牌", "纯全一杯三色确定立一摸","七搭子从不上张", ],
	    [ "和朋友讨论", "各种喜闻乐见的剧本","技术嚎运现充全面被晒", ],
	    [ "留安牌", "一发避铳扭转乾坤","留安留出事", ],
	    [ "研习科学理论", "贯彻落实科学发展观，雀力日进","没天赋还学人家打麻将，啧啧", ],
        ]
        
        for yaku in ["立平断", "小三元", "七对子", "纯全带", "一气通贯", "三色同顺", "三暗刻", "岭上开花", "海底捞月"]:
            all_condition.append( [ f"选择{yaku}役", "达成率显著提升","望山跑死马", ] )
        for pai in ["东", "南", "西", "北", "白", "发", "中", "三索", "七筒", "赤五万", "赤五索", "赤五筒", "万字", "索字", "筒字"]:
            all_condition.append( [ f"把{pai}牌留手里", "孤张摸成DORA面子","不是现物都是铳", ] )
        
        known = set()
        for i in (1,2,3,):
            select_condition = self.get_choice( all_condition )
            if select_condition[0].startswith("把"):
                k = 'ba'
            elif select_condition[0].startswith("选择"):
                k = 'xz'
            else:
                k = select_condition[0]
            if k not in known:
                known.add(k)
                self.add_text(f"    麻将宜: {select_condition[0]} -- {select_condition[1]}" )
        for i in (1,2,3,):
            select_condition = self.get_choice( all_condition )
            if select_condition[0].startswith("把"):
                k = 'ba'
            elif select_condition[0].startswith("选择"):
                k = 'xz'
            else:
                k = select_condition[0]
            if k not in known:
                known.add(k)
                self.add_text(f"    麻将忌: {select_condition[0]} -- {select_condition[2]}" )
        pass

    def attack(self):
        atk = self.get_choice( range(10,100) )
        defend =  self.get_choice( range(10,50) )
        hp = self.get_choice( range(200,500) )
        weapon = list()
        for line in open("suanming.data/weapon.list"):
            weapon.append(line.strip())
        weapon = self.get_choice(weapon) 
        self.add_text(f"攻击:{atk}  防御:{defend}  血量:{hp}" )
        self.add_text(f"武器:{weapon}" )
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
        im1 = Image.new('RGB', (600, 32), "#FFF6DC")
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
        im1 = Image.new('RGB', (300, 32), "#FFF6DC")
        draw = ImageDraw.Draw(im1)
        font = ImageFont.truetype('fonts/msyh.ttf', 20)
        draw.text((0,0), f"今日幸运数字: {choice} ", font=font, fill="#000000")
        self.report_images.append( im1 )
    
    def init_touhou(self):
        all_choice = list()
        for line in open("data/images/touhou/list"):
            all_choice.append( line.strip() )
        choice = self.get_choice( all_choice )

        im1 = Image.new('RGB', (300, 32), "#FFF6DC")
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

        print(" suanming debug: ",len(self.h))
        a = int( self.h[:n_d], 16 )
        self.h = self.h[n_d:]
        ratio = int( a*1.0/(16**n_d)*n  )
        return all_choice[ratio] 

    def draw(self):
        pass

    def report(self):
        width_l =   [ x.width  for x in self.report_images ]
        height_l  = [ x.height for x in self.report_images ]

        dst = Image.new('RGB', ( max(width_l), sum(height_l) ), "#FFF6DC" )
        h = 0
        for im in self.report_images:
            if im.mode == "RGBA":
                dst.paste(im, (0, h), mask = im)
            else:
                dst.paste(im, (0, h),)
                
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
        if salt == '':
            query = salt + str(uid) + str(b.tm_year) +str( b.tm_mon) +str( b.tm_mday ) 
            nickname = analysis.get_nick_name(message,gid,uid)
        else:
            query = salt 
            nickname = query

        yunshi = Yunshi( query, nickname )
        m = yunshi.report()
        analysis.send_msg(m,uid=uid,gid=gid)

        # 圣经
        # 幸运字
        # 幸运emoji
        # 水群强度
        # 表白用语
        # attack defend hp sp weapon
        # movie
        # beijing opera
        # 


    except Exception as e:
        print(e)
        analysis.send_msg("诸事皆宜...",uid=uid,gid=gid)




