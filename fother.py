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
        cmd = f"select * from zdy where answer='{key}' order by id desc limit 1"
        result = analysis.source_mysql(cmd)
        return b64d(result[0][1])
    except Exception as e:
        return False

def other(message,uid=0,gid=0):
    try:
        items = message.text.split()
        if len(items) == 1:
            anwser = find_answer(items[0].lstrip("/-"))
            if anwser:
                analysis.send_msg(anwser.lstrip("/") ,uid=uid,gid=gid)
            else:
                return
        else:
            return
    except Exception as e:
        print(e)
        analysis.send_msg("哦我的上帝啊,又是哪个该死的代码不工作了！",uid=uid,gid=gid)


