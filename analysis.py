import re
import json
from urllib.parse import parse_qs
import pymysql
import requests
import base64
import sys,os
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import io
import random as rd
import glob
# import api_puzzle

def b64e(s):
    return base64.b64encode(s.encode()).decode()

def b64d(s):
    return base64.b64decode(s).decode()

def send_msg(m,uid=0,gid=0,at = False,to_image=False):
    if not m.startswith("/"):
        if at:
            data = { 'group_id': gid  , 'message':f"[CQ:at,qq={uid}] " + m } 
        else:
            data = { 'group_id': gid  , 'message':m } 
        url = 'http://0.0.0.0:5700/send_group_msg'
        print(">>>>> send_msg:",data, url)
        if not to_image:
            requests.post( url=url, data=data )
        else:
            word_size = 16
            word_css = 'fonts/msyh.ttf'
            font = ImageFont.truetype(word_css,word_size,encoding='unic') 
            #font = ImageFont.core.getfont(word_css,word_size,encoding='unic') 
            text_width, text_height = font.getsize( m )
            text_height = len(m.split("\n")) * 20 + 16
            text_width  = max( [ 10*len(x) for x in m.split("\n") ] )

            img = Image.new('RGB', (text_width + 20 , text_height + 20 ),(255,255,255))
            d = ImageDraw.Draw(img)
            d.text( (10, 10), m, fill=(0, 0, 0),font=font )

            s = io.BytesIO()
            img.save(s, 'png')
            in_memory_file = s.getvalue()
            with open("data/images/tmp_text2png.png",'wb') as ofp:
                ofp.write(in_memory_file)
            data = { 'group_id': gid  , 'message':'[CQ:image,file=tmp_text2png.png]' } 
            requests.post( url=url, data=data )

    else:
        data = { 'message_type':'group',
                'group_id':gid,
                'sender': { 'user_id' : uid },
                'raw_message': m }
        url = 'http://0.0.0.0:5701'
        print(">>>>> send_msg (fake message) :",data, url)
        requests.post( url=url, json=data )

def true_startswith(string, *query):
        patt = re.compile("\[CQ:.*?\]")
        text = re.sub( patt,'', string ).lstrip()
        for q in query:
            if text.startswith(q):
                return True
        return False

class Message( str ):
        def __init__(self,message):
                super(str,self).__init__()
                patt = re.compile("\[CQ:.*?\]")
                self.text = re.sub( patt,'', message ).lstrip()
                cqs = re.findall( r'\[CQ:(.*?),(.*?)\]', message )
                cqs_text = re.findall( r'(\[CQ:.*?,.*?\])', message )
                self.cqs = list()
                for cq,cq_text in zip(cqs,cqs_text):
                        tmpcq = CQ()
                        tmpcq.type = cq[0]
                        tmpcq.content = parse_qs( cq[1], separator=',' )
                        tmpcq.raw = cq_text
                        self.cqs.append( tmpcq )

class CQ:
        def __init__(self):
                self.type=''
                self.content=''
                self.raw=''

def source_mysql(cmd):
    print(cmd)
    sys.stdout.flush()
    db = pymysql.connect(host='localhost', user='seasons', password='123', database='seasons')
    results = 'ERROR'
    try:
        cursor = db.cursor()
        print(cmd)
        sys.stdout.flush()
        cursor.execute(cmd)
        results = cursor.fetchall()
        db.commit()
        db.close()
    except Exception as e:
        print(e)
        db.rollback()
        db.close()

    return results

def get_reply(message,uid,gid):
    reply_cq = ''
    for cq in message.cqs:
        if cq.type == 'reply':
            reply_cq = cq
            break
    assert reply_cq != ''
    reply_id = reply_cq.content['id'][0]
    url = 'http://0.0.0.0:5700/get_msg'
    data = {'message_id':int(reply_id)} 
    res = requests.post( url=url, data=data )
    reply_msg = json.loads( res.content )['data']['message'] 
    reply_msg = Message(reply_msg)
    return reply_msg

def get_nick_name(message,gid,uid):
    try:
        url = 'http://0.0.0.0:5700/get_group_member_info'
        data = {'group_id':int(gid), 'user_id':int(uid) } 
        res = requests.post( url=url, data=data )
        reply_msg = json.loads( res.content )['data']['nickname'] 
        return reply_msg
    except:
        return "Cthulhu"

def send_private_msg(m,uid):
    data = { 'user_id': uid  , 'message':m } 
    url = 'http://0.0.0.0:5700/send_msg'
    print(">>>>> send_priveate_msg:",data )
    requests.post( url=url, data=data )
    return

def moe_name_back(a):
    b = a.replace("@_","(").replace("_@",")") 
    return b

def get_laopo(uid, n = 1):
    laoponames = list()
    laopofiles = list()

    result = source_mysql(f"select p from xp where uid = '{uid}'" )
    if not result:
        pics = glob.glob("/root/seasons_bot/moe/images_2/*jpg")
        b = rd.sample( pics, n )
        for a in b:
            laoponames.append( moe_name_back(os.path.basename(a).strip(".jpg")) )
            laopofiles.append( a )
    else:
        xps = set()
        for tmp in result:
            xps.add( f"'{tmp[0]}'" )
        s = ','.join(xps)
        result = source_mysql( f"select list from moe_list where xp in ({s})" )
        all_names = list()
        for r in result:
            all_names.extend( b64d(r[0]).split('\t') )
        b = rd.sample( all_names, n )
        for a in b:
            laoponames.append( moe_name_back(a) )
            laopofiles.append( "/root/seasons_bot/moe/images_2/"+a+".jpg" )

    return (laoponames,laopofiles )

# m = '/+bga [CQ:at,qq=937404959] zyyzxyz'
# m = Message(m)
# print(m.cqs[0].type)
# print(m.cqs[0].content)
# print(m.cqs[0].raw)
