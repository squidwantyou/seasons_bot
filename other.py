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
            anwser = find_answer(items[0])
            if anwser:
                analysis.send_msg(anwser,uid=uid,gid=gid)
            else:
                return
        else:
            key = items[0]
            value = message.text.lstrip(key).lstrip()
            # if value.startswith('/'):
            if False:
                pass
            else:
                record_answer(key,value)
    except Exception as e:
        print(e)
        analysis.send_msg("见鬼，又是那个代码出故障了，我真想用靴子狠狠地踢它的屁股！",uid=uid,gid=gid)


