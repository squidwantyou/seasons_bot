#!/usr/bin/env python
import requests
import json
import re
import analysis

def fhelp(message,uid=0,gid=0):
    try:
        command_list = [ [ '/help','/list','/帮助' ],
        [ '/roll'],
        [ '/语录' ],
        [ '/添加语录','/加入语录' ],
        [ '/吃什么' ],
        [ '/加入菜单','/添加菜单' ],
        [ '/猜数字','/1a2b' ],
        [ '/猜颜色','/guess' ],
        [ '/5a2b' ],
        [ '/诗词' ,'/一次元'],
        [ '/土味' ,'/twqh','/土味情话'],
        [ '/情话' ,'/qh'],
        [ '/二次元','/ecy' ,'/水煮鱼' ],
        [ '/三次元','/scy','/酸菜鱼' ],
        [ '/车万','/touhou','/松鼠鱼'],
        [ '/摸鱼','/moyu' ],
        [ '/早安','/晚安' ],
        [ '/提醒','/delay' ],
        [ '/循环','/loop' ],
        [ '/选择','/choose','/choice' ],
        [ '/排序','/sort'],
        [ '/夸我','/kk', '/kw'],
        [ '/小姐姐','/四次元', '/girl'],
        [ '/echo','/say', '/说' ],
        [ '/pz','/碰撞' ],
        [ '/猫猫','/cat', '/miao','/喵' ],  
        [ '/dog', ],  
        [ '/9say', ],  
        [ '/boy',],
        [ '/anwei',],
        [ '/舔狗',],
        [ '/nmsl',],
        [ '/-' ], ]
        m = '所有口令：\n'
        for l in command_list:
            m += '\t'
            m += " ".join(l)
            m += '\n'
        m += "注：同一行的口令作用完全相同（\n"

        analysis.send_msg(m,uid=uid,gid=gid)
    except Exception as e:
        print(e)

