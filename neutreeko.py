import analysis 
import random as rd
import sys,os
from messageflowcontrol import Mfc
import numpy as np
from copy import deepcopy
import itertools
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patches as mpatches
import matplotlib

N = 5
margin = 0

def is_legal( commands ): #list
    if len(commands)<2:
        return False
    if commands[0].upper() in ("B1","B2","B3","W1","W2","W3"):
        if commands[1].upper() in ("N","W","S","E","NE","NW","SE","SW"):
            return True
    return False


class Board:
    def __init__(self, restore = False , first_player = None, first_uid = None):
        self.pieces = { "B1":( 1,0 ),
                        "B2":( 3,0 ),
                        "B3":( 2,3 ),
                        "W1":( 1,4 ),
                        "W2":( 3,4 ),
                        "W3":( 2,1 ),
        }
        self.log = list()

        if restore:
            self.load_from_text(restore)
        else:
            self.log = list()
            self.recruit = list()
            self.recruit.append( first_uid )
            self.add_log(f"{first_player} created the game.")
            # self.add_log("Initialized.")
            self.uid = dict()
            self.uid["B"] = None
            self.uid["W"] = None
            self.nickname = dict()
            self.nickname["B"] = None
            self.nickname["W"] = None
            self.winner = "XXXX"

        self.move_shift = dict()
        self.move_shift['N'] =  ( 0, 1) 
        self.move_shift['S'] =  ( 0,-1) 
        self.move_shift['W'] =  (-1, 0) 
        self.move_shift['E'] =  ( 1, 0) 
        self.move_shift['NW'] = (-1, 1) 
        self.move_shift['NE'] = ( 1, 1) 
        self.move_shift['SW'] = (-1,-1) 
        self.move_shift['SE'] = ( 1,-1) 
    
    def add_player(self, color , nickname, uid ):
        assert color in ("B","W")
        self.uid[color] = uid
        self.nickname[color] = nickname
        if color == "B":
            self.add_log(f"{nickname} play as Black.")
        if color == "W":
            self.add_log(f"{nickname} play as White.")
            

    def move(self, p, direct ,uid = None, nickname = None ):
        assert p[0] in "BW"
        assert uid == self.uid[p[0]]
        old_c = str(self.pieces[ p ])
        this_p = p[:2]
        this_direct = direct
        
        while True:
            s = self.move_shift[direct]
            c = self.pieces[ p ]
            new_c = (c[0]+s[0],c[1]+s[1])
            if self.is_free( new_c ):
                self.pieces[p] = new_c
            else:
                break
        last_c = str(self.pieces[p])
        self.add_log(f"{self.nickname[p[0]]}: {this_p} {this_direct} to {last_c}")

        return True

    def accept( self,p, direct,uid=None):
        if len(p) >=1 and p[0] not in "BW":
            return False
        if not uid == self.uid[ p[0] ]:
            return False

        if len(p) >=2 and p[1] in "123":
            p = p[:2]
        else:
            return False

        s = self.move_shift[direct]
        c = self.pieces[ p ]
        new_c = (c[0]+s[0],c[1]+s[1])

        if self.is_free( new_c ):
            return True
        else:
            return False

        return False

    def is_free(self,c):
        for i in self.pieces.values():
            if c == i:
                return False
        if 0 <= c[0] <= 4:
            if 0 <= c[1] <= 4:
                return True
        return False

    def check_win(self,uid):
        win = dict()
        win['B'] = None
        win['W'] = None
        for color in ("B","W"):
            for (a,b,c) in itertools.permutations( [self.pieces[f"{color}1"],self.pieces[f"{color}2"],self.pieces[f"{color}3"]] ):
                if (a[0] + 1 == b[0] and b[0] +1 == c[0]) or (a[0]  == b[0] and b[0] == c[0]) or (a[0] -1  == b[0] and b[0] -1 == c[0]) :
                    if (a[1] + 1 == b[1] and b[1] +1 == c[1]) or (a[1]  == b[1] and b[1] == c[1]) or (a[1] -1  == b[1] and b[1] -1 == c[1]) :
                            win[color] = True
        if win['B'] :
            self.add_log("Black Win!")
            self.set_winner( uid )
            return True
        if win['W'] :
            self.add_log("White Win!")
            self.set_winner( uid )
            return True
        
        return False
    
    def save(self,uid,gid,mfc):
        text = self.to_text() 
        cmd = f"INSERT INTO ntk ( boardtext, status, qqgroup ) VALUES ( '{text}', '{mfc.status}', '{gid}' )"
        analysis.source_mysql(cmd)

    def set_winner(self,uid):
        self.winner = uid

    def to_text(self):
        self.text = ""
        for k in ["B1","B2","B3","W1","W2","W3"]:
            self.text = self.text + f"{self.pieces[k][0]} {self.pieces[k][1]}  "
        self.text = self.text + f"{self.uid['B'] } "
        self.text = self.text + f"{self.uid['W'] } "
        self.text = self.text + f"{self.nickname['B'] } "
        self.text = self.text + f"{self.nickname['W'] } "
        self.text = self.text + f"{self.winner} "
        self.text = self.text + " ".join(self.log)
        return self.text
    
    def load_from_text(self,text):
        items = text.split()
        self.pieces = dict()
        i = 0
        for k in ["B1","B2","B3","W1","W2","W3"]:
            a = int( items[i] ) 
            b = int( items[i+1] )
            i += 2
            self.pieces[k] = (a,b)

        self.uid = dict()
        self.uid['B']  = items[i]
        i += 1
        self.uid['W']  = items[i]
        i += 1
        self.nickname = dict()
        self.nickname["B"] = items[i]
        i += 1
        self.nickname["W"] = items[i]
        i += 1
        self.winner = items[i]
        i += 1
        self.log = items[i:]

    def add_log(self,s):
        self.log.append(s.replace(" ","____") )

    def to_png(self,filepath = '' ):
        global margin
        plt.clf()
        Nx,Ny = 5,5
        fig,ax = plt.subplots(figsize = (N+7,N+1))
        ax.axis('off')

        # add boarder line
        linelist  = [   [(-0.5,-0.5),(-0.5,Ny-0.5)],
                [(-0.5,-0.5),(Nx-0.5,-0.5)],
                [(-0.5,Ny-0.5),(Nx-0.5,Ny-0.5)],
                [(Nx-0.5,-0.5),(Nx-0.5,Ny-0.5)] ]

        x = [ x[0] for x in linelist ]
        y = [ x[1] for x in linelist ]
        line_segs = LineCollection( linelist,lw=5,color='black',alpha = 0.7 ) 
        ax.add_collection( line_segs )

        # add inner line
        linelist = list()
        for i in range(Nx-1):
            linelist.append( ((0.5+i,-0.5),(0.5+i,Ny-0.5)) ) # v
        for i in range(Ny-1):
            linelist.append( ((-0.5,0.5+i),(Nx-0.5,0.5+i)) ) # h

        line_segs = LineCollection( linelist,lw=2,color='black',alpha = 0.3 ) 
        ax.add_collection( line_segs )

        ax.set_xlim( (-0.5-margin, Nx-0.5+margin + 6) )
        ax.set_ylim( (-0.7-margin, Ny-0.5+margin) )

        # add number 
        for k in ["B1","B2","B3"]:
            loc = self.pieces[k]
            text = k
            poly = mpatches.Circle( loc,radius=0.4,facecolor='black',)
            ax.add_artist( poly )
            ax.text(loc[0], loc[1], text, horizontalalignment='center', verticalalignment='center', fontsize=18, color = 'white' )

        for k in ["W1","W2","W3"]:
            loc = self.pieces[k]
            text = k
            poly = mpatches.Circle( loc,radius=0.4,facecolor='white',edgecolor = "black",lw = 5,)
            ax.add_artist( poly )
            ax.text(loc[0], loc[1], text, horizontalalignment='center', verticalalignment='center', fontsize=18, color = 'black' )


        myfont = matplotlib.font_manager.FontProperties(fname='fonts/msyh.ttf')

        # add log
        logtext = "\n".join( [x.replace("____"," ") for x in self.log] )
        # winner
        if self.winner == "XXXX" :
            logtext = logtext + "\n" + "Ongoing"
        else:
            logtext = logtext + "\n" + f"Winner: {self.winner} "
        ax.text(N+4, (N-1)/2, logtext,horizontalalignment='center', verticalalignment='center', fontsize=16 ,fontproperties = myfont)


        plt.savefig(filepath)
        plt.clf()
        

#mysql> describe ntk;
#+-----------+---------------+------+-----+---------+----------------+
#| Field     | Type          | Null | Key | Default | Extra          |
#+-----------+---------------+------+-----+---------+----------------+
#| id        | int           | NO   | PRI | NULL    | auto_increment |
#| boardtext | varchar(1024) | YES  |     | NULL    |                |
#| status    | varchar(255)  | YES  |     | NULL    |                |
#| qqgroup   | varchar(255)  | YES  |     | NULL    |                |
#+-----------+---------------+------+-----+---------+----------------+

def load_last_board(gid):
    cmd = f"select * from ntk where qqgroup='{gid}' ORDER BY id DESC LIMIT 1;" 
    result = analysis.source_mysql(cmd)
    board_text = result[0][1]
    board = Board( restore = board_text )
    return board

def report_status(board,uid,gid,mfc):
    png = board.to_png(f"data/images/mfc{gid}.png")
    next_text = None
    if board.winner != "XXXX":
        next_text = f"{board.winner} wins!"
    elif mfc.status == "Recruiting":
        next_text = f"Send '/ntk join' to accept challenge."
    elif "Wait" in mfc.status:
        next_text = f"Wait {mfc.status.split()[1]} to move"
    else:
        next_text = ''
    m = f"[CQ:image,file=mfc{gid}.png] {next_text}"
    analysis.send_msg(m,gid=gid)

def report_ilegal(uid,gid):
    m = f"=w= 好像有点错误了哦"
    analysis.send_msg(m,gid=gid)
    

mfcs = dict()
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
                if status == "Recruiting" or "Wait" in status:
                    board = load_last_board(gid)
                    # board.add_log(f"{uid} joined!")
                    board.add_player("W",nickname,uid) 
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


# b = Board( )
# b.add_player("B","Bp","123")
# b.add_player("W","Wp","456")
# mfc = Mfc()
# b.save("uid","gid",mfc)
# print(b.uid)
# print(b.nickname)
# print( b.accept("B1","NE","123") )
# print( b.accept("B1","NW","123") )
# b.move("B1","NW","123")
# print( b.check_win("WIN") )
# b.move("W3","NW","456")
# print( b.check_win("WIN") )
# b.move("B2","NW","123")
# print( b.check_win("WIN") )
# b.to_png("tmp.png")
# #print(b.assign(1,1,1,uid="test"))
# #b.to_png("a.png")

