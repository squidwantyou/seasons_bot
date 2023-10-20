#!/usr/bin/env python3
import base64
import sys,os
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patches as mpatches
import matplotlib
import random as rd
import pickle
import numpy as np
from analysis import source_mysql,send_msg
import analysis

''' mysql> describe bet;
+---------+---------------+------+-----+-------------------+-------------------+
| Field   | Type          | Null | Key | Default           | Extra             |
+---------+---------------+------+-----+-------------------+-------------------+
| id      | int           | NO   | PRI | NULL              | auto_increment    |
| ratio   | varchar(1024) | YES  |     | NULL              |                   |  ratio  "A:2.0,B:2.0,C:2.0"
| des     | varchar(4096) | YES  |     | NULL              |                   |  des  base64 encode 
| creator | varchar(1024) | YES  |     | 605378861         |                   |
| qqgroup | varchar(1024) | YES  |     | NULL              |                   |
| date    | timestamp     | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+---------+---------------+------+-----+-------------------+-------------------+

mysql> describe wealth;
+--------+---------------+------+-----+-------------------+-------------------+
| Field  | Type          | Null | Key | Default           | Extra             |
+--------+---------------+------+-----+-------------------+-------------------+
| qq     | varchar(20)   | YES  |     | NULL              |                   |
| wealth | int           | YES  |     | NULL              |                   |
| diff   | int           | YES  |     | NULL              |                   |
| reason | varchar(1024) | YES  |     | NULL              |                   |
| date   | timestamp     | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+--------+---------------+------+-----+-------------------+-------------------+

mysql> describe bat_wager;
+----------+---------------+------+-----+-------------------+-------------------+
| Field    | Type          | Null | Key | Default           | Extra             |
+----------+---------------+------+-----+-------------------+-------------------+
| id       | int           | NO   | PRI | NULL              | auto_increment    |
| bet_id   | int           | YES  |     | NULL              |                   |
| qq       | varchar(20)   | YES  |     | NULL              |                   |
| bet_item | varchar(1024) | YES  |     | NULL              |                   |
| wegar    | int           | YES  |     | NULL              |                   |
| date     | timestamp     | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+----------+---------------+------+-----+-------------------+-------------------+
'''

class Bet:
    def __init__(self):
        self.init = False
        pass
    def load_last_bet(self, qqgroup = gid ):
        result = source_mysql(f"select * from bet where qqgroup='qqgroup' ORDER BY id DESC LIMIT 1;")
        if len(result) == 0 :
            return
        else:
            self.init = True
            index = result[0][0]
            ratio = result[0][1]
            des = result[0][2]
            creator = result[0][3]
            qqgroup = result[0][4]
            des = analysis.b64d(des)
            self.items = list()
            self.ratio = list()
            for _ in ratio.split(","):
                self.items.append( _.split(":")[0] )
                self.ratio.append( float(_.split(":")[1]) )
            self.des = des 
            self.index = index
            self.creator = creator
            self.qqgroup = qqgroup
    
    def submit_bet(self,):
        pass
        

    

def bet( message, uid, gid ):
    path = ''
    try:
        path = " ".join(message.text.split()[1:])
    except:
        path = ''

    if path == '':    # no arguments, report 
        bet = load_last_bet()
        if not bet:
            analysis.send_msg(gid =gid, m ="当前没有盘口")
            return
        else:
            analysis.send_msg(f"当前盘口: {bet.show_str()} ")
            
         
    elif path == 'stop': # end current puzzle
        finish_puzzle(gid)
        analysis.send_msg(gid =gid, m ="Thank you for playing.")
        return 


