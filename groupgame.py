#!/usr/bin/env python
import requests
import json
import re
import analysis
import chunyemen

tmp = '''
MariaDB [seasons]> describe groupgame;
+------------+---------------+------+-----+-------------------+----------------+
| Field      | Type          | Null | Key | Default           | Extra          |
+------------+---------------+------+-----+-------------------+----------------+
| id         | int(11)       | NO   | PRI | NULL              | auto_increment |
| groupn     | varchar(255)  | YES  |     | NULL              |                |
| numplayers | int(11)       | YES  |     | NULL              |                |
| players    | varchar(1023) | YES  |     | NULL              |                |
| gametype   | varchar(255)  | YES  |     | NULL              |                |
| starter    | varchar(255)  | YES  |     | NULL              |                |
| status     | varchar(255)  | YES  |     | NULL              |                |
| result     | text          | YES  |     | NULL              |                |
| time       | timestamp     | NO   |     | CURRENT_TIMESTAMP |                |
+------------+---------------+------+-----+-------------------+----------------+
'''


def fetch_last_game(uid,gid,i_id = None):
    if not i_id:
        cmd = f"select * from groupgame where groupn='{gid}' ORDER BY id DESC LIMIT 1;" 
        result = analysis.source_mysql(cmd)
        try:
            return result[0]
        except Exception as e:
            return [ 0,0,0,'','','','end','','' ]
    else:
        cmd = f"select * from groupgame where i_id='{i_id}' ;" 
        result = analysis.source_mysql(cmd)
        try:
            return result[0]
        except Exception as e:
            return [ 0,0,0,'','','','end','','' ]
    pass

def f_start_game(uid=uid,gid=gid):
    lastgame = fetch_last_game(uid=uid,gid=gid)
    i_id , groupn, numplayers, players, gametype, starter,status,result,time = lastgame
    if gametype=='cym':
        result = chunyemen.start_game(i_id)
        if not result:
            raise Exception
    else:
        raise Exception

def f_end_game(uid=uid,gid=gid):
    lastgame = fetch_last_game(uid=uid,gid=gid)
    i_id , groupn, numplayers, players, gametype, starter,status,result,time = lastgame
    if gametype=='cym':
        result = chunyemen.end_game(i_id)
        if not result:
            raise Exception
    else:
        raise Exception
        

def f_create_game(gametype,numplayers,uid,gid):
    try:
        if gametype == 'cym'
            game_index = chunyemen.create_game(numplayers,uid,gid)
        else:
            raise Exception
        return game_index
    except:
        return None

def f_status_game(uid,gid):
    try:
        lastgame = fetch_last_game(uid=uid,gid=gid)
        i_id , groupn, numplayers, players, gametype, starter,status,result,time = lastgame
        m = ''
        if status == 'end':
            m += "当前没有进行中的群游戏"
        else:
            if gametype == 'cym':
                m += "当前的游戏是 纯爷们地下城."
            
            m += f"游戏编号是{i_id}"

            if status == 'recruiting':
                n = len(players.split())
                m += f"目前正在招募玩家({n}/{numplayers}). "
                m += f"已加入玩家有 {players} . "
            elif status == 'ongoing':
                m += f"目前正在进行中. "
                m += f"玩家有 {players} . "
        analysis.send_msg(m,uid=uid,gid=gid)

    else:
        raise Exception
    except:
        analysis.send_msg("小触手状态不太好呢~",uid=uid,gid=gid)

def f_forprivate(m,uid,gid = None):
    try:
        items = m.text.split()
        i_id = int(items[0])
        current_game = fetch_last_game(uid=None,gid=None,i_id = i_id )
        i_id , groupn, numplayers, players, gametype, starter,status,result,time = current_game
        if gametype == 'cym' and status != 'end':
            chunyemen.forprivate(m,uid)

    except Exception as e:
        analysis.send_private_msg("error",uid=uid)
    

def create_game(message,uid=0,gid=0):
    try:
        items = m.text.split()
        gametype = items[2]
        numplayers = None
        try:
            numplayers = int(items[3])
        except:
            numplayers = None

        game_index = f_create_game(gametype = 'cym',numplayers = numplayers uid=uid,gid=gid,)
        
        if game_index:
            if numplayers:
                maxn = numplayers
            else:
                maxn = "infinity"
            analysis.send_msg(f"游戏已创建, 私信'/加入 {game_index}', 加入游戏. 人数达到{maxn}时游戏自动开始, 也可以由发起玩家({uid})发送'/gg start' 手动开始." )
        else :
            analysis.send_msg(f"游戏创建...欸? 失败?!" )

    except:
        analysis.send_msg(f"游戏创建...欸? 失败?!" )

def start_game(message,uid=0,gid=0):
    items = m.text.split()
    f_start_game(uid=uid,gid=gid)
    pass

def end_game(message,uid=0,gid=0):
    items = m.text.split()
    f_end_game(uid=uid,gid=gid)
    pass

def status_game(message,uid=0,gid=0):
    items = m.text.split()
    f_status_game(uid=uid,gid=gid)
    pass

def groupgame(m,uid=0,gid=0):
    try:
        items = m.text.split()
        if   items[1] in ("new",):
            create_game(m,uid=uid,gid=gid)
        elif items[1] in ("start",):
            start_game(m,uid=uid,gid=gid)
        elif items[1] in ("end",):
            end_game(m,uid=uid,gid=gid)
        elif items[1] in ("status",):
            status_game(m,uid=uid,gid=gid)
    except:
        analysis.send_msg("不太明白~")
    pass

def forprivate(m,uid=uid,gid=gid):
    f_forprivate(m,uid=uid,gid=gid)


