#!/usr/bin/env python
import requests
import json
import re
import analysis
import sys,os
import PIL
from PIL import Image, ImageFont , ImageDraw
import glob
import random as rd
import time

datafile = "./seasons_quest_data.csv"
background_color = "#B9D5F3"

def error(gid = 0,uid=0):
    analysis.send_msg(gid=gid,m="呜呜，又出错了")

def make_puzzle(gid=None, uid=0):
    datalines = open(datafile).readlines()
    questline = rd.choice(datalines)
    items = questline.strip().split("\t")
    game_id = items[0]
    start = items[1]
    player = items[2]
    yeguai = items[3]
    playerhands = items[4:13]
    yeguaihands = items[13:22]
    result = items[22]
    if start == "True":
        start = 1
    else:
        start = 0
    if result == "Win":
        result = 1
    else:
        result = 0
    
    a = rd.choice( [0,1] )
    if a == 0:
        pass
    else:
        start = 1-start
        result = 1-result
        playerhands, yeguaihands = yeguaihands,playerhands
        player,yeguai = yeguai, player

    strfmt = '%30s  %30s\n'
    quest_str = ''
    tmp = [u"先手",u"后手"]
    quest_str = quest_str + strfmt%("Player_A"+tmp[1-start],"Player_B"+tmp[start])
    for a,b in zip( playerhands, yeguaihands ):
        quest_str = quest_str + strfmt%(a,b)
    quest_str = quest_str + strfmt%("","Who will win ? reply A or B")
    answer = game_id, player, yeguai, result
    with open( f'seasons_quest_answer_{gid}','w')  as ofp:
        ofp.write(f"{game_id}\t{player}\t{yeguai}\t{result}\n")
        ofp.write("\n")
    return (quest_str, answer)

def analyze_query( answer, query ,all_info=None) :
    if all_info != None:
        game_id,player,yeguai,result_tmp = all_info 
    if result_tmp == 1 and player == query:
        return True
    if result_tmp == 0 and yeguai == query:
        return True
    query = query[0].upper()
    tmp = answer
    return query == tmp

def fetch_last_puzzle(gid):
    try:
        assert os.path.isfile( f'seasons_quest_answer_{gid}') 
        lines = open( f'seasons_quest_answer_{gid}').readlines()
        game_id,player,yeguai,result = lines[0].strip().split("\t")
        game_id = int(game_id)
        result = int(result)
        status = lines[1]
        answer = None
        if result == 1:
            answer = "A"
        else:
            answer = "B"
        all_info = game_id,player,yeguai,result
        return (answer,status,all_info)
    except Exception as e:
        print(e)
        return [ "X" ,'error','0','0' ]

def finish_puzzle(gid):
    try:
        assert os.path.isfile( f'seasons_quest_answer_{gid}') 
        os.system(f"mv seasons_quest_answer_{gid} seasonsquest_save/seasons_quest_answer_{gid}_{int(time.time())}")
    except Exception as e:
        print(e)
        return [ "ABC" ,'error' ]

# dm                
def seasonsquest(message,uid,gid):
    global n_trials
    color = ''
    try:
        color = message.text.split()[1]
    except:
        color = None

    if color == None:
        color = 'new'
    
    if color == 'new':
        quest_str, answer = make_puzzle( gid = gid,uid=uid )
        m = quest_str
        analysis.send_msg(m,uid=uid,gid=gid,to_image=True)

    else:
        try:
            query = color
            answer,status,all_info = fetch_last_puzzle(gid)
            print(answer, query, all_info)
            result = analyze_query(answer,query,all_info) # analysis new query
            tmp_str = None
            if not result:
                tmp_str = "猜错了捏~ "
            else:
                tmp_str = "您TQL! "
            sys.stdout.flush()
            game_id,player,yeguai,result_tmp = all_info 
            winner = None
            tmp_str = tmp_str + f"A是{player}, B是{yeguai}"
            if not result:
                tmp_str = tmp_str + "\n" + f"Winner is NOT {query}."
            else:
                tmp_str = tmp_str + "\n" + f"Winner is {query}.\n"
            tmp_str = tmp_str + f"回放在这: https://boardgamearena.com/table?table={game_id}"
            analysis.send_msg(tmp_str,uid=uid,gid=gid,)
            finish_puzzle(gid)
        except Exception as e:
            print(e)
            tmp_str = "有点迷惑..."
            analysis.send_msg(tmp_str,uid=uid,gid=gid,)
            

