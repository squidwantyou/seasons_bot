#!/usr/bin/env python
import requests
import json
import re
import analysis
import sys,os
import traceback

def seq(a,b):
    if a<b:
        return (a,b)
    else:
        return (b,a)

def sanitize(t):
    if '-' not in t:
        d = re.findall("[nNsScCwWeE\?]+",t)[0]
        num = re.findall("\d+",t)[0]
        e = 1
        if 'x' in t:
            e = 2
        if 'y' in t:
            e = 3
        if 'z' in t:
            e = 4
        out = f"{d.upper()}-{num}-{e}"
        out = out.replace("NW","NW?").replace("NE","NE?").replace("SW","SW?").replace("SE","SE?")
        return out
    else:
        return t

def bunny(message,uid=0,gid=0):
    try:
        l = message.text.lstrip("/bunny ")
        all_bunny = dict()
        for line in open("bunny.txt"):
            line = line.strip("\n")
            line = line.strip("\r")
            line = line.strip("\n")
            line = line.strip("\r")
            a,b = line.strip().split(" x ")
            if a not in all_bunny:
                all_bunny[a] = set()
            if b not in all_bunny:
                all_bunny[b] = set()
            all_bunny[a].add(b)
            all_bunny[b].add(a)

        if message.text.split()[0] == '/bunny':
            for line in l.split("\n"):
                line = line.strip("\n")
                line = line.strip("\r")
                line = line.strip("\n")
                line = line.strip("\r")
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

        elif "/checkbunny" in message.text or '/bunnycheck' in message.text:
            query = message.text.split()[1]
            query = query.strip().lstrip()
            query = sanitize(query)
            m = "\n".join( sorted(all_bunny[query]) )
            m = "Partners: \n" + m 
            analysis.send_msg(m,uid=uid,gid=gid,to_image=True)

        elif "/explorebunny" in message.text:
            query = message.text.split()[1]
            query = sanitize(query)
            all_bunny = set()
            all_pair = set()
            for line in open("bunny.txt"):
                line = line.strip("\n")
                line = line.strip("\r")
                line = line.strip("\n")
                line = line.strip("\r")
                a,b = line.strip().split(" x ")
                all_pair.add( seq(a,b) )
                all_bunny.add(a)
                all_bunny.add(b)

            all_count = dict()
            for ba in all_bunny:
                for bb in all_bunny:
                    if ba<=bb:
                        continue
                    both = set()
                    for bc in all_bunny:
                        if seq(ba,bc) in all_pair and seq(bb,bc) in all_pair:
                            both.add(bc)
                    all_count[ seq(ba,bb) ] = both

            filtered = [ x for x in all_count if len(all_count[x]) != 0 ]
            sort_key = sorted( filtered, key = lambda x:len(all_count[x]), reverse = True )

            revo = dict()
            for k in sort_key:
                if k not in all_pair: 
                    v = tuple(all_count[k])
                    if v not in revo:
                        revo[v] = {k,}
                    else:
                        revo[v].add(k)

            m = ''
            for k in revo:
                for tmp in revo[k]:
                    if query in tmp:
                        p = list(tmp)
                        p.remove(query)
                        m = m + f"Possible Partner: {p[0]}\n"
                        m = m + f"          Common: {' '.join(k)}\n\n"
            analysis.send_msg(m,uid=uid,gid=gid,to_image = True)

        elif "/bunnymap" in message.text:
            query = message.text.split()[1]
            i = int(query)
            assert 0<i<=27
            m = f"[CQ:image,file=bunnymap/{i}.png]"
            analysis.send_msg(m,uid=uid,gid=gid)
        elif "/bunnycmp" in message.text:
            a = message.text.strip().split()[1]
            b = message.text.strip().split()[2]
            pair = list()
            for t in a,b:
                t = sanitize(t)
                pair.append(t)
            a,b = pair
            set1 = set(all_bunny[a])
            set2 = set(all_bunny[b])
            only1 = set1-set2 -set([b,])
            only2 = set2-set1 -set([a,])
            both = set1 & set2
            m = ''
            m = m + f"Only in {a}:\n\t" + "\n\t".join(sorted(only1)) + '\n'
            m = m + f"Only in {b}:\n\t" + "\n\t".join(sorted(only2)) + '\n'
            m = m + f"In Both:\n\t" + "\n\t".join(sorted(both))
            analysis.send_msg(m,uid=uid,gid=gid,to_image=True)
        else:   
            pass

    except Exception as e:
        traceback.print_exc()
        analysis.send_msg("要来点兔子么?",uid=uid,gid=gid)

