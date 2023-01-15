import re
import json
from urllib.parse import parse_qs
import pymysql
import requests

def send_msg(m,uid=0,gid=0):
    data = {'group_id': gid  , 'message':m} 
    url = 'http://0.0.0.0:5700/send_group_msg'
    print(">>>>> send_msg:",data, url)
    requests.post( url=url, data=data )

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
    db = pymysql.connect(host='localhost', user='seasons', password='123', database='seasons')
    results = 'ERROR'
    try:
        cursor = db.cursor()
        cursor.execute(cmd)
        results = cursor.fetchall()
        db.commit()
        db.close()
    except Exception as e:
        print(e)
        db.rollback()
        db.close()

    return results

# m = '/+bga [CQ:at,qq=937404959] zyyzxyz'
# m = Message(m)
# print(m.cqs[0].type)
# print(m.cqs[0].content)
# print(m.cqs[0].raw)
