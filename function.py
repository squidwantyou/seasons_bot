#!/usr/bin/env python
import sys,os
import random as rd
import requests
import pymysql
import json
import analysis
import base64
import glob

def b64e(s):
    return base64.b64encode(s.encode()).decode()

def b64d(s):
    return base64.b64decode(s).decode()

#### Error
def error(message,uid,gid = None):
    m = '''>>>>> 切,出错了'''
    data = {'group_id': gid  , 'message':m} 
    url = 'http://0.0.0.0:5700/send_group_msg'
    print(data, url)
    requests.post( url=url, data=data )

#### Help
def help(message,uid,gid = None):
    m = '''>>>>> 触手型自律机器人特性:
                /?bga  @波奇    
                /+bga  @元首 MimicBox  
                /吃什么 /加入菜单      
                /语录   /加入语录     
                /瑟图   /加入瑟图    
                /猜数字 /guess
                /摸鱼   /roll N         
                /诗词   /help           
                /abc def #自定义回复
        '''
    data = {'group_id': gid  , 'message':m} 
    url = 'http://0.0.0.0:5700/send_group_msg'
    print(data, url)
    requests.post( url=url, data=data )

#### 苏联笑话
if True:
    xiaohuas = dict()
    infile = 'xiaohua.list'
    index = 0
    current = ''
    for line in open(infile):
            if len(line.split()) >= 1:
                    try:
                            index = int(line)
                            xiaohuas[index] = ''
                    except:
                            xiaohuas[index] += line
            else:
                    pass
    print(">>>>> Xiaohua loaded")

def xiaohua(message,uid,gid = None):
    key  = rd.choice( list(xiaohuas.keys()) )
    m = f"{key}:\n" + xiaohuas[key] 
    m = "老大哥已经无了，不要再笑了"
    data = {'group_id': gid  , 'message':m} 
    url = 'http://0.0.0.0:5700/send_group_msg'
    print(data, url)
    requests.post( url=url, data=data )

# 获取食物
def meal(message,uid,gid = None):
    url = 'http://0.0.0.0:5700/send_group_msg'
    id = ''
    text = ''
    try:
        db = pymysql.connect(host='localhost', user='seasons', password='123', database='seasons')
        cursor = db.cursor()
        cursor.execute(f"select * from meal order by rand() limit 1")
        results = cursor.fetchall()
        id,text = results[0]
    except Exception as e:
        error(message,uid,gid)
    m = f"{id} {text}"
    data = {'group_id': gid  , 'message':m} 
    requests.post( url=url, data=data )

# 添加食物
def add_meal(message,uid,gid = None):
        try:
                reply_cq = ''
                for cq in message.cqs:
                        if cq.type == 'reply':
                                reply_cq = cq
                                break
                assert reply_cq != ''
                print(reply_cq.content)
                reply_id = reply_cq.content['id'][0]
                url = 'http://0.0.0.0:5700/get_msg'
                data = {'message_id':int(reply_id)} 
                res = requests.post( url=url, data=data )
                reply_msg = json.loads( res.content )['data']['message'] 
                reply_msg = analysis.Message(reply_msg)
                img_cq = ''
                for cq in reply_msg.cqs:
                        if cq.type == 'image':
                                img_cq = cq
                                break
                assert img_cq != ''

                text = cq.raw
                db = pymysql.connect(host='localhost', user='seasons', password='123', database='seasons')
                cursor = db.cursor()
                cursor.execute(f"insert into meal ( content ) values ( '{text}' ) ")
                db.commit()

                m = f'ok, 这原来可以吃的嘛?'
                url = 'http://0.0.0.0:5700/send_group_msg'
                data = {'group_id': gid  , 'message':m} 
                requests.post( url=url, data=data )
                db.close()

        except Exception as e:
                db.rollback()
                error(message,uid,gid)
                db.close()

# 瑟图
def setu(message,uid,gid = None):
    url = 'http://0.0.0.0:5700/send_group_msg'
    id = ''
    text = ''
    try:
        db = pymysql.connect(host='localhost', user='seasons', password='123', database='seasons')
        cursor = db.cursor()
        cursor.execute(f"select * from setu order by rand() limit 1")
        results = cursor.fetchall()
        id,text = results[0]
    except Exception as e:
        error(message,uid,gid)
    m = f"{id} {text}"
    data = {'group_id': gid  , 'message':m} 
    requests.post( url=url, data=data )

# 添加瑟图
def add_setu(message,uid,gid = None):
        try:
                reply_cq = ''
                for cq in message.cqs:
                        if cq.type == 'reply':
                                reply_cq = cq
                                break
                assert reply_cq != ''
                print(reply_cq.content)
                reply_id = reply_cq.content['id'][0]
                url = 'http://0.0.0.0:5700/get_msg'
                data = {'message_id':int(reply_id)} 
                res = requests.post( url=url, data=data )
                reply_msg = json.loads( res.content )['data']['message'] 
                reply_msg = analysis.Message(reply_msg)
                img_cq = ''
                for cq in reply_msg.cqs:
                        if cq.type == 'image':
                                img_cq = cq
                                break
                assert img_cq != ''

                text = cq.raw
                db = pymysql.connect(host='localhost', user='seasons', password='123', database='seasons')
                cursor = db.cursor()
                cursor.execute(f"insert into setu ( content ) values ( '{text}' ) ")
                db.commit()

                m = f'ok 的说~'
                url = 'http://0.0.0.0:5700/send_group_msg'
                data = {'group_id': gid  , 'message':m} 
                requests.post( url=url, data=data )
                db.close()

        except Exception as e:
                db.rollback()
                error(message,uid,gid)
                db.close()

# yvlu 
def yvlu(message,uid,gid = None):
    url = 'http://0.0.0.0:5700/send_group_msg'
    id = ''
    text = ''
    try:
        db = pymysql.connect(host='localhost', user='seasons', password='123', database='seasons')
        cursor = db.cursor()
        cursor.execute(f"select * from yvlu order by rand() limit 1")
        results = cursor.fetchall()
        id,text = results[0]
    except Exception as e:
        error(message,uid,gid)
    text = b64d(text)
    m = f"{id} {text}"
    data = {'group_id': gid  , 'message':m} 
    requests.post( url=url, data=data )

# add yvlu
def add_yvlu(message,uid,gid = None):
        try:
                reply_cq = ''
                for cq in message.cqs:
                        if cq.type == 'reply':
                                reply_cq = cq
                                break
                assert reply_cq != ''
                print(reply_cq.content)
                reply_id = reply_cq.content['id'][0]
                url = 'http://0.0.0.0:5700/get_msg'
                data = {'message_id':int(reply_id)} 
                res = requests.post( url=url, data=data )
                reply_msg = json.loads( res.content )['data']['message'] 
                reply_nickname = json.loads( res.content )['data']['sender']['nickname'] 
                text = b64e(reply_nickname + ":" +  reply_msg )

                db = pymysql.connect(host='localhost', user='seasons', password='123', database='seasons')
                cursor = db.cursor()
                cursor.execute(f"insert into yvlu ( content ) values ( '{text}' ) ")
                db.commit()

                m = f'Get daze~'
                url = 'http://0.0.0.0:5700/send_group_msg'
                data = {'group_id': gid  , 'message':m} 
                requests.post( url=url, data=data )
                db.close()

        except Exception as e:
                db.rollback()
                error(message,uid,gid)
                db.close()

# 添加BGAID
def addid(message,uid,gid = None):
        try:
                url = 'http://0.0.0.0:5700/send_group_msg'
                db = pymysql.connect(host='localhost', user='seasons', password='123', database='seasons')
                cursor = db.cursor()
                
                qq = ''
                nickname = ''
                bga = message.text.split()[-1]
                for cq in message.cqs:
                        if cq.type == 'at':
                                qq = cq.content['qq'][0]
                assert (qq != '')
                
                try:
                        print(f"delete from bga_id where qq = '{qq}'")
                        print(f"INSERT INTO bga_id ( qq, nickname, bga ) values ({qq},{nickname},{bga})")
                        cursor.execute(f"delete from bga_id where qq = '{qq}'")
                        cursor.execute(f"INSERT INTO bga_id ( qq, nickname, bga ) values ('{qq}','{nickname}','{bga}')")
                        db.commit()
                        m = f'已记录 {nickname} {qq} {bga} 呐~'
                        data = {'group_id': gid  , 'message':m} 
                        requests.post( url=url, data=data )
                except Exception as e:
                        db.rollback()
                        error(message,uid,gid)
                db.close()
        except Exception as e:
                error(message,uid,gid)
        
# 获取BGAID
def getid(message,uid,gid = None):
        try:
                qq = ''
                for cq in message.cqs:
                        if cq.type == 'at':
                                qq = cq.content['qq'][0]
                assert (qq != '')

                url = 'http://0.0.0.0:5700/send_group_msg'
                db = pymysql.connect(host='localhost', user='seasons', password='123', database='seasons')
                cursor = db.cursor()

                try:
                        print(f"SELECT * FROM bga_id where qq = '{qq}'")
                        cursor.execute(f"SELECT * FROM bga_id where qq = '{qq}'")
                        results = cursor.fetchall()
                        m = "\t".join(results[0])
                        # m = f'已记录 {nickname} {qq} {bga} 呐~'
                        data = {'group_id': gid  , 'message':m} 
                        requests.post( url=url, data=data )
                except Exception as e:
                        error(message,uid,gid)
                db.close()
        except Exception as e:
                error(message,uid,gid)

# 扔骰子
def roll(message,uid,gid):
        try:
                text = message.text
                number = int(text.split()[1])
                url = 'http://0.0.0.0:5700/send_group_msg'
                m = str(rd.randint(1,number))
                data = {'group_id': gid  , 'message':m} 
                requests.post( url=url, data=data )
        except:
                error(message,uid,gid)
        
# da
def answer(message,uid,gid):
    pass

# 诗词
def shici(message,uid,gid):
    data = requests.get("https://v1.jinrishici.com/all.json")
    text = json.loads(data.content)["content"]
    analysis.send_msg( text, uid=uid,gid=gid )
    
def tuweiqinghua(message,uid,gid):
    data = requests.get("https://api.vvhan.com/api/love")
    text = data.content.decode('utf-8')
    analysis.send_msg( text, uid=uid,gid=gid )

def qinghua(message,uid,gid):
    data = requests.get("https://api.lovelive.tools/api/SweetNothings")
    text = data.content.decode('utf-8')
    analysis.send_msg( text, uid=uid,gid=gid )

def kk(message,uid,gid):
    try:
        results = analysis.source_mysql(f"select * from kk order by rand() limit 1")
        text = analysis.b64d( results[0][1] )
        analysis.send_msg( text, uid=uid,gid=gid )
    except:
        analysis.send_msg( "程序沉醉于您的美貌,都停止运行了", uid=uid,gid=gid )

def gushi(message,uid,gid):
    try:
        shangju = message.text.split()[1]
        query = analysis.b64e(shangju)
        results = analysis.source_mysql(f"select xiaju from pnbs where shangju='{query}' limit 1")
        text = analysis.b64d( results[0][0] )
        analysis.send_msg( text, uid=uid,gid=gid )
    except:
        analysis.send_msg( "古籍浩如烟海,小触手Hold不住", uid=uid,gid=gid )

