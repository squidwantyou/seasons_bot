#!/usr/bin/env python
import requests
import json
import re
import analysis
import base64

def b64e(s):
    return base64.b64encode(s.encode()).decode()

def b64d(s):
    return base64.b64decode(s).decode()

def find_answer(key):
    key=b64e(key)
    try:
        cmd = f"select * from zdy where query='{key}' order by id desc limit 1"
        result = analysis.source_mysql(cmd)
        return b64d(result[0][2])
    except Exception as e:
        return False

def record_answer(key,value):
    key = b64e(key)
    value = b64e(value)
    try:
        analysis.source_mysql(f"insert into zdy ( query, answer ) values ( '{key}', '{value}' ) ")
    except:
        raise Exception

def other(message,uid=0,gid=0):
    try:
        items = message.text.split()
        if len(items) == 1:
            if items[0] == '/我要入群':
                reply = '''三国版杀单挑版631105718
冰火版杀混将版390192333
冰火魔兽地图版572739859
召唤师战争版杀1093402862
截码战版杀105519002
行动代号版杀105519002
猜灯谜105519002
猜人物105519002
狼人真言版杀105519002
冰火版杀三国版726626754
三国卡牌地图版
AA版杀792928487
足球经理版杀695306632
宋金战争版杀526356041
电厂版杀696424142
GH版杀
深入绝地版杀813706399
日本战国地图版542073634
战争之匣版杀
马尼拉版杀199137991
冰火3V3单挑943076369'''
                analysis.send_msg(reply,uid=uid,gid=gid)
                return
                
            anwser = find_answer(items[0])
            if anwser:
                analysis.send_msg(anwser,uid=uid,gid=gid)
            else:
                return
        else:
            key = items[0]
            value = message.text.lstrip(key).lstrip()
            if value.startswith('/'):
            # if False:
                pass
            else:
                record_answer(key,value)
    except Exception as e:
        print(e)
        analysis.send_msg("见鬼，又是那个代码出故障了，我真想用靴子狠狠地踢它的屁股！",uid=uid,gid=gid)


