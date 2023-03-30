#!/usr/bin/env python3
import base64
import sys,os
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patches as mpatches
import matplotlib
import random as rd
import pickle
import numpy as np
from analysis import source_mysql,send_msg
import analysis

MAX_MOVE=5


table = '''
world_command_count
+----------+--------------+------+-----+-------------------+----------------+
| Field    | Type         | Null | Key | Default           | Extra          |
+----------+--------------+------+-----+-------------------+----------------+
| id       | int(11)      | NO   | PRI | NULL              | auto_increment |
| qq       | varchar(255) | YES  |     | NULL              |                |
| count    | int(11)      | YES  |     | 0                 |                |
| commands | mediumtext   | YES  |     | NULL              |                |
| time     | timestamp    | NO   |     | CURRENT_TIMESTAMP |                |
+----------+--------------+------+-----+-------------------+----------------+

world_player
+--------------+--------------+------+-----+-------------------+----------------+
| Field        | Type         | Null | Key | Default           | Extra          |
+--------------+--------------+------+-----+-------------------+----------------+
| id           | int(11)      | NO   | PRI | NULL              | auto_increment |
| name         | varchar(255) | YES  |     | NULL              |                |
| qq           | varchar(255) | YES  |     | NULL              |                |
| strength     | int(11)      | YES  |     | NULL              |                |
| intelligence | int(11)      | YES  |     | NULL              |                |
| san          | int(11)      | YES  |     | NULL              |                |
| knowledge    | int(11)      | YES  |     | NULL              |                |
| fame         | int(11)      | YES  |     | NULL              |                |
| weapon       | varchar(255) | YES  |     | NULL              |                |
| bag          | text         | YES  |     | NULL              |                |
| buffs        | mediumtext   | YES  |     | NULL              |                |
| time         | timestamp    | NO   |     | CURRENT_TIMESTAMP |                |
+--------------+--------------+------+-----+-------------------+----------------+
'''

def error(uid,gid):
    send_msg("错的不是我，是这个世界！",uid=uid,gid=gid)
    
def get_status(uid):
    cmd = f"select * from world_player where qq={uid} ORDER BY id DESC LIMIT 1;"
    result = source_mysql(cmd)
    if len(result) == 0:
        return False
    else:
        result = list(result[0])
        name = result[1]
        result[1] = analysis.b64d(name)
        return result

def create(args, uid,gid):
    stat = get_status(uid=uid)
    flag_create = False
    if not stat :
        flag_create = True
    else:
        if len(args) >= 1 and args[0] == '重启':
            flag_create = True
        else:
            name = stat[1]
            m = f"{name}, 您已经加入世界了哦, 请用“/加入世界 重启”命令强制新建人物"
            send_msg(m,uid=uid,gid=gid)
            report_status(uid=uid,gid=gid)
    if flag_create:
        name = analysis.b64e(analysis.get_nick_name("",uid=uid,gid=gid))
        qq = uid
        strength = rd.randrange(3,7)
        intelligence = rd.randrange(3,7)
        san = rd.randrange(3,7)
        knowledge = rd.randrange(3,7)
        fame = rd.randrange(3,7)
        init_weapons = ["桧木棍","竹竿","生锈小刀","沙袋"]
        weapon = analysis.b64e( rd.choice( init_weapons) )
        bag = analysis.b64e(" "+"====")
        buffs = analysis.b64e(" "+"====")
        cmd = f'INSERT INTO world_player (name,qq,strength, intelligence,san, knowledge, fame, weapon, bag,buffs ) \
               VALUES ( "{name}", "{qq}", {strength}, {intelligence}, {san}, {knowledge},{fame},"{weapon}","{bag}","{buffs}" );'
        result = analysis.source_mysql(cmd)
        report_status(uid=uid,gid=gid)

def duanlian(args, uid,gid):
    try:
        stat = get_status(uid)
        if not stat:
            return 
        i = stat[0]
        name = stat[1]
        strength = stat[3] + 1
        cmd = f"UPDATE world_player SET strength={strength} WHERE id={i};"
        analysis.source_mysql(cmd)
        m = f"疯狂撸了一会儿铁，{name} 感觉自己变强壮了一点！（力量+1）"
        move = add_command('D',uid=uid,gid=gid)
        m += f"\n（今日剩余口令次数: {MAX_MOVE-move}/{MAX_MOVE})"
        send_msg(m,uid=uid,gid=gid)
    except Exception as e:
        print(e)
        error(uid=uid,gid=gid)

def add_command(cmd,uid,gid):
    query = f"SELECT * from world_command_count WHERE qq={uid} AND date(time)=curdate();"
    result = analysis.source_mysql(query)
    if len(result) == 0:
        cmd = cmd
        count = 1
        query = f"INSERT INTO world_command_count (qq,count,commands) VALUES ('{uid}',{count},'{cmd}');"
        result = analysis.source_mysql(query)
        return count
    else:
        result = result[0]
        i = result[0]
        count = result[2]
        count += 1
        oldcmd = result[3]
        newcmd = oldcmd + " " + cmd
        query = f"UPDATE world_command_count SET count={count} WHERE id={i};"
        result = analysis.source_mysql(query)
        return count
        

def libai(args, uid,gid):
    try:
        stat = get_status(uid)
        if not stat:
            return 
        i = stat[0]
        name = stat[1]
        fame = stat[7] + 1
        cmd = f"UPDATE world_player SET fame={fame} WHERE id={i};"
        analysis.source_mysql(cmd)
        m = f"{name} 虔诚地向神明祷告，被路过的村民看到了（声望+1）"
        move = add_command('D',uid=uid,gid=gid)
        m += f"\n（今日剩余口令次数: {MAX_MOVE-move}/{MAX_MOVE})"
        send_msg(m,uid=uid,gid=gid)
    except Exception as e:
        print(e)
        error(uid=uid,gid=gid)
        pass

def xuexi(args, uid,gid):
    try:
        stat = get_status(uid)
        if not stat:
            return 
        i = stat[0]
        name = stat[1]
        san = stat[5] - 1
        knowledge = stat[6] + 1
        cmd = f"UPDATE world_player SET knowledge={knowledge} WHERE id={i};"
        analysis.source_mysql(cmd)
        cmd = f"UPDATE world_player SET san={san} WHERE id={i};"
        analysis.source_mysql(cmd)
        m = f"看了一会儿书，{name} 了解到了一些之前不知道的事情（知识+1,理智-1）"
        move = add_command('D',uid=uid,gid=gid)
        m += f"\n（今日剩余口令次数: {MAX_MOVE-move}/{MAX_MOVE})"
        send_msg(m,uid=uid,gid=gid)
    except Exception as e:
        print(e)
        error(uid=uid,gid=gid)

def bailan(args, uid,gid):
    try:
        stat = get_status(uid)
        if not stat:
            return 
        i = stat[0]
        name = stat[1]
        san = stat[5] + 1
        cmd = f"UPDATE world_player SET san={san} WHERE id={i};"
        analysis.source_mysql(cmd)
        m = f"什么都不想了，什么都不做了，{name} 决定放空自己（理智+1）"
        move = add_command('D',uid=uid,gid=gid)
        m += f"\n（今日剩余口令次数: {MAX_MOVE-move}/{MAX_MOVE})"
        send_msg(m,uid=uid,gid=gid)
    except Exception as e:
        print(e)
        error(uid=uid,gid=gid)
        pass

def dayouxi(args, uid,gid):
    try:
        stat = get_status(uid)
        if not stat:
            return 
        i = stat[0]
        name = stat[1]
        intelligence = stat[4] + 1
        cmd = f"UPDATE world_player SET intelligence={intelligence} WHERE id={i};"
        analysis.source_mysql(cmd)
        m = f"打了一会儿小游戏，虽然没什么用吧，但是{name}感觉神清气爽（脑力+1）"
        move = add_command('D',uid=uid,gid=gid)
        m += f"\n（今日剩余口令次数: {MAX_MOVE-move}/{MAX_MOVE})"
        send_msg(m,uid=uid,gid=gid)
    except Exception as e:
        print(e)
        error(uid=uid,gid=gid)
        pass

def waichu(args, uid,gid):
        pass
def gongji(args, uid,gid):
        pass
def genghuazhiye(args, uid,gid):
        pass

def report_status(uid,gid,only_move=False):
#'''| id | name    | qq   | strength | intelligence | san  | knowledge | fame | weapon   | bag  | buffs | time                |'''
    stat = get_status(uid=uid)
    if not stat:
        raise Exception
        return
    else:
        name = stat[1]
        strength = stat[3]
        intelligence = stat[4]
        san = stat[5]
        knowledge = stat[6]
        fame = stat[7]
        weapon = analysis.b64d(stat[8])
        bag = analysis.b64d(stat[9])
        buff = analysis.b64d(stat[10])
        work = '无'
        move = can_move(uid,gid)
        m = f'''{name}\t{work}\n力量：{strength}\t脑力：{intelligence}\t理智：{san}\n知识：{knowledge}\t声望：{fame}\n武器：{weapon}\n'''
        if move:
            m+=f"今日已活动次数:{move}/{MAX_MOVE}"
        else:
            m+="今日已活动次数已用完"
        send_msg(m,uid=uid,gid=gid)
    pass

def rename(args,uid,gid):
    try:
        stat = get_status(uid)
        i = stat[0]
        name = stat[1]
        if len(args)==0:
            m += f"用法是：/world 改名 '新名字'"
            send_msg(m,uid=uid,gid=gid)
            return
        else:
            newname = "_".join(args)

        cmd = f"UPDATE world_player SET name='{analysis.b64e(newname)}' WHERE id={i};"
        analysis.source_mysql(cmd)
        m = f"{name}觉得自己名字不太好听，于是改成了{newname}"
        move = add_command('D',uid=uid,gid=gid)
        m += f"\n（今日剩余口令次数: {MAX_MOVE-move}/{MAX_MOVE})"
        send_msg(m,uid=uid,gid=gid)
        
    except Exception as e:
        print(e)
        error(uid=uid,gid=gid)

def can_move(uid,gid):
    query = f"SELECT * from world_command_count WHERE qq={uid} AND date(time)=curdate();"
    result = analysis.source_mysql(query)
    if len(result) == 0:
        return True
    else:
        result = result[0]
        count = result[2]
        if count >= MAX_MOVE:
            return False
        else:
            return MAX_MOVE-count

def show_help(uid,gid):
    m = '''试试 /world [口令] \n当前可用口令口前有：加入世界 改名 锻炼 礼拜 学习 摆烂 打游戏 状态\n今后将陆续推出各种元素（虽然可能很慢）'''
    analysis.send_msg(m,uid=uid,gid=gid)

def world(message,uid=0,gid=0):
    try:
        args = message.text.split()[1:]
        
        if len(args) == 0:   # no argument: report character status
            report_status(uid=uid,gid=gid)
            
        else:
            first_arg = args[0]
            if first_arg == "help":  # print help message
                    show_help(uid=uid,gid=gid)
                    pass
            else:
                if not can_move(uid=uid,gid=gid):  # reach max limit
                    report_status(uid=uid,gid=gid,only_move=True)
                else:
                    if first_arg == "加入世界":   #  create
                        create(args[1:], uid=uid,gid=gid)
                    elif first_arg == "改名":   #  rename   
                        rename(args[1:], uid=uid,gid=gid)
                    elif first_arg == "锻炼":   #  + strength   
                        duanlian(args[1:], uid=uid,gid=gid)
                    elif first_arg == "礼拜":   #  + fame
                        libai(args[1:], uid=uid,gid=gid)
                    elif first_arg == "学习":   #  + knowledge
                        xuexi(args[1:], uid=uid,gid=gid)
                    elif first_arg == "摆烂":   #  + san
                        bailan(args[1:], uid=uid,gid=gid)
                    elif first_arg == "打游戏": #  + intelligence
                        dayouxi(args[1:], uid=uid,gid=gid)
                    elif first_arg == "状态": #  + intelligence
                        report_status(uid=uid,gid=gid)
                    #elif first_arg == "外出":   #  oppunity to get items
                    #    waichu(args[1:], uid=uid,gid=gid)
                    #elif first_arg == "攻击":   #  
                    #    gongji(args[1:], uid=uid,gid=gid)
                    #elif first_arg == "更换职业":   #
                    #    genghuazhiye(args[1:], uid=uid,gid=gid)
                    else:
                        pass
        
    except Exception as e:
        print(e)
        error(uid=uid,gid=gid)
   
    
m = analysis.Message(" ")
# m.text="/world 加入世界"
# world(m,6,0)
# m.text="/world 锻炼"
# world(m,6,0)
# m.text="/world 学习"
# world(m,6,0)
# m.text="/world 摆烂"
# world(m,6,0)
# m.text="/world 打游戏"
# world(m,6,0)
# m.text="/world 礼拜"
# world(m,6,0)
# m.text="/world 改名"
# world(m,6,0)
# m.text="/world 改名 状态"
# world(m,6,0)
