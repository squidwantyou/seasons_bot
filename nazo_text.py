import analysis 
import random as rd
import sys,os
import numpy as np
from copy import deepcopy
import itertools
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patches as mpatches
import matplotlib

# nazo concept
# per group   
# text / picture 
# use self ability maximum 
# ten questions for the first puzzle
    # 1 下一关的钥匙是"触手", 回复/nazo 触手前进吧!    触手
    # 2 钥匙是带嘤的触手  tentacle
    # 3 钥匙是钥匙的钥匙  defined-tentacle
    # 4 将触手彻底分解为几部分, 最大的一块好像可以当作钥匙     887143
    # 5 VGhlIGtleSBpcyBlbmNvZGVkIGFzIFkzbGlaWEl0ZEdWdWRHRmpiR1U9IA==   cyber-tentacle
    # 6 future number  ( use /today )
    

N = 5
margin = 0

class Nazo:
    def __init__(self, restore = False , first_player = None, first_uid = None):
def ntk(message,uid,gid):
    nickname = analysis.get_nick_name(message,gid,uid)
    uid = str(uid)

    global mfcs 
    if gid in mfcs:
        mfc = mfcs[gid] 
    else:
        mfc = Mfc()
        mfcs[gid] = mfc
    
    try:
        command = ''
        try:
            command = message.text.split()[1]
        except:
            command = None

        if command == None:
            command = 'help'
            
        elif command == 'stop':
            return 

        elif command == 'new':
            board = Board(first_player = nickname)
            board.add_player("B",nickname,uid)
            mfc = Mfc()
            mfcs[gid] = mfc
            status = mfc.conduct(message,uid,gid)
            if status == "Recruiting":
                print(">>>>> A", mfc.account,mfc.recruit_left)
                sys.stdout.flush()
                #board.add_log(f"{uid} Starts!")
                report_status(board,uid,gid,mfc)
                board.save(uid,gid,mfc)
        
        elif command == 'join':
            if mfc.recruit_left > 0 :
                status = mfc.conduct(message,uid,gid)
                    report_status(board,uid,gid,mfc)
                    board.save(uid,gid,mfc)
                elif status == "Ignore":
                    print(f">>> MFC ignored {uid}")
                    sys.stdout.flush()
            else:
                print(f">>>> Recruits denied")
                sys.stdout.flush()
            

        elif command == 'help':
            m = "[CQ:image,file=ntk_help.png]"
            analysis.send_msg(m,uid=uid,gid=gid)
        
        else:
            if is_legal( message.text.split()[1:] ) and uid in mfc.waiting:
                board = load_last_board(gid)
                p,d = message.text.split()[1:3]
                p = p.upper()
                d = d.upper()
                # d = int(d)
                result = board.accept(p,d,uid=uid)
                if result :
                    board.move(p,d,uid=uid)
                    if board.check_win(nickname):
                        status = mfc.conduct(message,uid,gid)
                        report_status(board,uid,gid,mfc)
                        board.save(uid,gid,mfc)
                        mfcs.pop(gid)
                    else:
                        status = mfc.conduct(message,uid,gid)
                        report_status(board,uid,gid,mfc)
                        board.save(uid,gid,mfc)
                else:
                    report_ilegal(uid,gid)
            else:
                    report_ilegal(uid,gid)



    except Exception as e:
        print(e)
        sys.stdout.flush()
        analysis.send_msg(gid=gid,m=f'NTK ERROR')

