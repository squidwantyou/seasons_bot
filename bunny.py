#!/usr/bin/env python
import requests
import json
import re
import analysis

#apiurl = "https://tuapi.eees.cc/api.php?category=meinv"
apiurl = 'https://3650000.xyz/api/?type=json'
apiurl = "https://api.xiaobaibk.com/api/pic/?pic=meizi"



def bunny(message,uid=0,gid=0):
    try:
        l = message.text.lstrip("/bunny ")
        all_bunny = dict()
        for line in open("bunny.txt"):
            a,b = line.strip().split(" x ")
            if a not in all_bunny:
                all_bunny[a] = set()
            if b not in all_bunny:
                all_bunny[b] = set()
            all_bunny[a].add(b)
            all_bunny[b].add(a)

        if "/bunny" in message.text and "map" not in message.text:
            for line in l.split("\n"):
                a,b = line.strip().split(" x ")
                if a not in all_bunny:
                    all_bunny[a] = set()
                if b not in all_bunny:
                    all_bunny[b] = set()
                all_bunny[a].add(b)
                all_bunny[b].add(a)
            
            with open("bunny.txt",'w') as ofp:
                for a in all_bunny:
                    for b in all_bunny[a]:
                        ofp.write(f"{a} x {b}\n")

            analysis.send_msg("知道啦~",uid=uid,gid=gid)

        elif "/checkbunny" in message.text:
            query = message.text.split()[1]
            m = "\n".join( sorted(all_bunny[query]) )
            m = "Partners: \n" + m 
            analysis.send_msg(m,uid=uid,gid=gid)

        elif "/explorebunny" in message.text:
            query = message.text.split()[1]
            known_bunny = all_bunny[query]
            new_bunny = set()
            pass

        elif "/bunnymap" in message.text:
            query = message.text.split()[1]
            i = int(query)
            assert 0<i<=27
            m = f"[CQ:image,file=bunnymap/{i}.png]"
            analysis.send_msg(m,uid=uid,gid=gid)
        else:   
            pass
            


    except Exception as e:
        print(e)
        analysis.send_msg("故障",uid=uid,gid=gid)

# scy('',gid=144744787)

# W-3-1 x W-4-1
