#!/usr/bin/env python
import analysis
import sys,os

def xp(message,uid=0,gid=0):
    print(">>>>> Called xp")
    try:
        items = message.text.split()
        if items[1] == "add":
            p = items[2]
            ep = analysis.b64e(p)
            result = analysis.source_mysql(f"select xp from moe_list where xp='{ep}'")
            if result:
                analysis.source_mysql(f"INSERT INTO xp (uid,p) VALUES ('{uid}','{ep}' )")
                analysis.send_msg("啊这... 好吧,明白了...",uid=uid,gid=gid)
            else:
                raise Exception

        elif items[1] == "remove":
            p = items[2]
            ep = analysis.b64e(p)
            analysis.source_mysql(f"DELETE FROM  xp where (uid='{uid}' AND p='{ep}' ) " )
            analysis.send_msg(f"好de,明白了",uid=uid,gid=gid)

        elif items[1] == "set":
            p = items[2]
            ep = analysis.b64e(p)
            result = analysis.source_mysql(f"select xp from moe_list where xp='{ep}'")
            if result:
                analysis.source_mysql(f"DELETE FROM  xp where (uid='{uid}') " )
                analysis.source_mysql(f"INSERT INTO xp (uid,p) VALUES ('{uid}','{ep}' )")
                analysis.send_msg(f"好de,明白了",uid=uid,gid=gid)
            else:
                raise Exception

        elif items[1] == "list":
            result = analysis.source_mysql(f"select p from  xp where uid='{uid}' " )
            s = ''
            for tmp in result:
                s = s+ analysis.b64d(tmp[0]) + ","
            analysis.send_msg(s,uid=uid,gid=gid,at=True)

    except Exception as e:
        analysis.send_msg("您的xp好怪哦,小触手理解不了",uid=uid,gid=gid)


