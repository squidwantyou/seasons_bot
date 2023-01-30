#!/usr/bin/env python
import requests
import json
import re
import analysis

# create table hello ( id int auto_increment, qq int, word varchar(255), time timestamp default current_timestamp, primary key(id) );

def login(uid):
    cmd = f"insert into hello ( qq, word ) values ( {uid} , 'morning' ) "
    analysis.source_mysql( cmd )

def logout(uid):
    cmd = f"insert into hello ( qq, word ) values ( {uid} , 'night' ) "
    analysis.source_mysql( cmd )
    pass

def get_status(uid):
    status = dict()
    cmd = f"select * from hello where qq={uid} and word = 'morning' and date(time) = curdate()"
    results = analysis.source_mysql( cmd )
    status['zao'] =( len(results) >= 1 )
    try:
        status['zao_time'] =results[0][3]
    except:
        status['zao_time'] = None
    cmd = f"select * from hello where qq={uid} and word = 'night' and date(time) = curdate()"
    results = analysis.source_mysql( cmd )
    status['wan'] =( len(results) >= 1 )
    try:
        status['wan_time'] =results[0][3]
    except:
        status['wan_time'] = None
    return status

def get_consecutive(uid):
    N = 0
    while (True ):
        cmd = f"select * from hello where qq={uid} and word = 'morning' and date(time) = curdate()-{N}"
        results = analysis.source_mysql( cmd )
        if ( len(results) >= 1 ):
            N += 1
        else:
            break
    return N

def get_awaketime(uid):
    cmd = f"select * from hello where qq={uid} and word = 'morning' and date(time) = curdate()"
    results = analysis.source_mysql( cmd )
    morning_time = results[0][3]


    cmd = f"select * from hello where qq={uid} and word = 'night' and date(time) = curdate()"
    results = analysis.source_mysql( cmd )
    night_time = results[0][3]

    d = night_time - morning_time 
    seconds = d.seconds
    hours = seconds//3600
    seconds -= 3600 * hours
    mins = seconds//60
    return f"{hours}h:{mins}m"

def greet_zao(uid,gid,nlogdays,zaotime=None):
    m = f'[CQ:at,qq={uid}] '
    m += f'早安! '
    m += f'这是您连续第{nlogdays}天向小触手打招呼了呢~ '
    m += f'新的一天要元气满满哦!'
    analysis.send_msg(m,uid=uid,gid=gid)

def greet_wan(uid,gid,awaketime):
    m = f'[CQ:at,qq={uid}] '
    m += f'晚安! '
    m += f'您今天的清醒时间是: {awaketime} '
    m += f'好好休息,会梦到触手play哒哟~'
    analysis.send_msg(m,uid=uid,gid=gid)
    pass

def complain(uid,gid):
    m = f'[CQ:at,qq={uid}] '
    m += f'哼,你今天都没有向在下问候早安! 明天不要忘了哦, 快去睡吧, 克苏鲁大人在梦里等你'
    analysis.send_msg(m,uid=uid,gid=gid)

def zaoan(message,uid=0,gid=0):
    try:
        if message.text.split()[0].strip() == '/早安':
            status = get_status(uid) # check status
            if status['wan']: # if already zao
                analysis.send_msg("您在梦游嘛?",uid=uid,gid=gid)
            elif status['zao']:
                analysis.send_msg("您已经打过招呼了哦~",uid=uid,gid=gid)
            else: # else
                login(uid) # login
                nlogin_days = get_consecutive(uid)
                # other info ?
                greet_zao(uid,gid,nlogin_days) # send message

        elif message.text.strip() == '/晚安':
            status = get_status(uid) # check status
            if status['zao']: # if already zao
                if status['wan']: # if alreay wan
                    analysis.send_msg("您已经睡着了哦~",uid=uid,gid=gid)
                    pass
                else:
                    logout(uid)
                    awaketime= get_awaketime(uid)
                    # other info ? 
                    greet_wan(uid,gid,awaketime) # send message
            else:
                complain(uid,gid) # complain
                login(uid) # login
                logout(uid)

        else:
            pass
    except Exception as e:
        print(e)
        analysis.send_msg("异常，这很异常",uid=uid,gid=gid)

