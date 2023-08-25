import analysis 
import random as rd
import sys,os
from messageflowcontrol import Mfc
import numpy as np
from copy import deepcopy
import itertools
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib

N = 5
margin = 0
RAND_HINT = 0
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:N]
abc = "abcdefghijklmnopqrstuvwxyz"[:N]
a123 = "123456789abcdefg"[:N]

def to_alphabet(x,y):
    return ( ABC[x],str(y+1) )
def to_number(x,y):
    if x in ABC:
        return ( ABC.index(x)  ,int(y)-1 )
    elif x in abc:
        return ( abc.index(x)  ,int(y)-1 )

def is_legal( commands ): #list
    if len(commands)<3:
        return False
    if commands[0] in list( ABC+abc ):
        if commands[1] in list(a123) :
            if commands[2].isdigit() and 0<=int(commands[2]) <=8:
                return True
    return False


class Board:
    def __init__(self, size = (N,N) , restore = False):
        if restore:
            Nx = int(restore.split()[0])
            Ny = int(restore.split()[1])
        else:
            Nx,Ny = size
        self.board = np.ndarray( shape = size, dtype = int )  
        self.coords = list()
        self.log = list()
        self.winner = "XXXX"
        for i in range(Nx):
            for j in range(Ny):
                self.coords.append( (i,j) )
                self.board[i,j] = 9

        self.nb = dict()
        for i in range(Nx):
            for j in range(Ny):
                self.nb[ (i,j) ] = set()
                xlower = max( i-1, 0)
                xupper = min( i+1, Nx-1 ) 
                ylower = max( j-1, 0)
                yupper = min( j+1, Ny-1 ) 
                for x in range(xlower,xupper+1):
                    for y in range(ylower,yupper+1):
                        if (x,y) != (i,j):
                            self.nb[ (i,j) ].add( (x,y) )

        if RAND_HINT and not restore:
            self.update_nb()
            rh = RAND_HINT
            while True:
                x = rd.randrange(0,Nx)
                y = rd.randrange(0,Ny)
                h = rd.randrange(2,5)
                if self.assign(x,y,h):
                    rh -= 1
                    self.update_nb()
                    self.get_hints()
                if rh == 0:
                    break
            self.get_hints()
            self.update_nb()

        if restore:
            self.load_from_text(restore)
        else:
            self.add_log("Initialized.")

            

    def assign(self, x,y, num, uid = None ):
        hint_keys = [x[0] for x in self.get_hints()]
        if (x,y) not in hint_keys:
            if 0<=num<=len(self.nb[ (x,y) ] ):
                self.board[x,y] = num
                self.update_nb()
                self.get_hints()
                if uid:
                    nx,ny = to_alphabet(x,y)
                    self.add_log( f"{uid}: {nx} {ny} {num}" )
                return True
        return False

    def get_hints(self):
        hints = list()
        for c in self.coords:
            if self.board[c] != 9:
                hints.append( (c,self.board[c] ) )
        self.hints = sorted( hints, key = lambda x:x[1] , reverse = True)
        return self.hints

    def update_nb(self):
        for (h,x) in  self.get_hints():
            for b in self.nb:
                if h in self.nb[b]:
                    self.nb[b].remove(h)
        return self.nb

    def accept( self, c_h, hint_number ,case ):
        # print("X",c_h, hint_number,case)
        s = 0
        nb = self.nb[c_h]
        for c in case:
            if c in nb:
                s += 1
        # print( "Y", s,hint_number, s == hint_number )
        return s == hint_number

    def solve(self):
        nb_list = deepcopy( self.update_nb() )
        hlist = self.get_hints()

        c_c = set()
        knownpool = [ (), ]

        while True:
            # set current hint as first hint 
            c_h,hint_number = hlist.pop(0)
            # print("A",c_h,hint_number)

            # A 
            # get permutation coords
            a = nb_list[c_h]
            # print("B",a)

            tmp_a = a - c_c 
            # print("C",tmp_a)
            c_c = c_c | a
            # print("D",c_c)

            # permutation  coords
            pool = list()
            for i in range(0,hint_number+1):
                pool.extend( list(itertools.combinations(tmp_a,i) ) )
            # print("E",pool)

            # combine new permutation of known
            newpool = set()
            for tmpi in knownpool:
                for tmpj in pool :
                    newpool.add( tmpi + tmpj )
            knownpool = newpool 

            # check new hint
            tmp_knownpool = deepcopy( knownpool )
            for case in knownpool:
                if not self.accept( c_h, hint_number ,case ):
                    tmp_knownpool.remove( case )
            knownpool = tmp_knownpool

            if len(knownpool) == 0: # if no result:
                return False # return False
            else:
                if len(hlist) == 0 : # if no more hints:
                    print(knownpool)
                    x,y = self.board.shape
                    nh = len(self.get_hints())
                    nt = len(c_c)
                    nblank = x * y - nh - nt
                    assert nblank >= 0
                    return len(knownpool) * ( 2**nblank )

                else:
                    continue
                    # if only one result:
                        # return 1
                    # if multiple results:
                        # return N
    
    def save(self,uid,gid,mfc):
        text = self.to_text() 
        cmd = f"INSERT INTO mwb ( boardtext, status, qqgroup ) VALUES ( '{text}', '{mfc.status}', '{gid}' )"
        analysis.source_mysql(cmd)
        

    def set_winner(self,uid):
        self.winner = uid
    
    def check(self,uid=None):
        r = None
        if uid:
            self.add_log(f"{uid} checked all mine!")
        solutions = self.solve()
        if solutions <= 1:
            self.add_log(f"Well done!")
            r = True
        else:
            self.add_log(f"What a pity!")
            r = False
        return r
    

    def to_text(self):
        text = ""
        x,y = self.board.shape
        text = text + f"{x} {y} "
        for i in range(x):
            for j in range(y):
                text = text + f"{self.board[i][j]} "
        text = text + " " + self.winner 
        text = text + " " + " ".join( self.log ) 
        return text
    
    def load_from_text(self,text):
        items = text.split()
        Nx = int(items[0])
        Ny = int(items[1])
        i = 2
        for x in range(Nx):
            for y in range(Ny):
                self.board[x,y] = items[i]
                i += 1
        self.winner = items[i]
        i += 1
        self.log = items[i:]
        self.update_nb()

    def add_log(self,s):
        self.log.append(s.replace(" ","____") )

    def to_png(self,filepath = '' ):
        global margin
        plt.clf()
        Nx,Ny = self.board.shape
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

        # add tick 
        for x in range(Nx):
            sx,sNy = to_alphabet(x,0)
            ax.text(x, -1 , sx, horizontalalignment='center', verticalalignment='center', fontsize=40, color = 'cyan' )
        for y in range(Nx):
            sNx,sy = to_alphabet(0,y)
            ax.text(-1, y, sy, horizontalalignment='center', verticalalignment='center', fontsize=40 , color = 'cyan')

        ax.set_xlim( (-0.5-margin, Nx-0.5+margin + 6) )
        ax.set_ylim( (-0.7-margin, Ny-0.5+margin) )

        # add number 
        hints = self.get_hints()
        for loc,num in hints:
            ax.text(loc[0], loc[1], str(num),horizontalalignment='center', verticalalignment='center', fontsize=48 )

        myfont = matplotlib.font_manager.FontProperties(fname='fonts/msyh.ttf')

        # add log
        logtext = "\n".join( [x.replace("____"," ") for x in self.log] )
        # winner
        if self.winner == "XXXX" :
            logtext = logtext + "\n" + "Ongoing"
        else:
            logtext = logtext + "\n" + f"Winner: {self.winner} "
        ax.text(N+4, (N-1)/2, logtext,horizontalalignment='center', verticalalignment='center', fontsize=24 ,fontproperties = myfont)


        plt.savefig(filepath)
        plt.clf()
        

#mysql> describe mwb;
#+-----------+---------------+------+-----+---------+----------------+
#| Field     | Type          | Null | Key | Default | Extra          |
#+-----------+---------------+------+-----+---------+----------------+
#| id        | int           | NO   | PRI | NULL    | auto_increment |
#| boardtext | varchar(1024) | YES  |     | NULL    |                |
#| status    | varchar(255)  | YES  |     | NULL    |                |
#| qqgroup   | varchar(255)  | YES  |     | NULL    |                |
#+-----------+---------------+------+-----+---------+----------------+

def load_last_board(gid):
    cmd = f"select * from mwb where qqgroup='{gid}' ORDER BY id DESC LIMIT 1;" 
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
        next_text = f"Send '/mwb join' to accept challenge."
    elif "Wait" in mfc.status:
        next_text = f"Wait {mfc.status.split()[1]} to move"
    else:
        next_text = ''
    m = f"[CQ:image,file=mfc{gid}.png] {next_text}"
    analysis.send_msg(m,gid=gid)

def report_ilegal(uid,gid):
    m = f"混乱的，迷惑的，不太理解的，您到底要干什么 =w="
    analysis.send_msg(m,gid=gid)
    

#    cmd = f"INSERT INTO gnc ( answer,queries, status, qqgroup ) VALUES ( '{answer}', '{log}', 0, '{gid}' )"
#    tmp = source_mysql(cmd)
#    cmd = f"UPDATE gnc SET queries='{log}',status={finished} WHERE id={index} and qqgroup='{gid}' "
#    result = source_mysql(cmd)
#    cmd = f"select * from gnc where qqgroup='{gid}' ORDER BY id DESC LIMIT 1;" 
#    cmd = f'UPDATE gnc SET status=1 WHERE id={index}'

mfcs = dict()
def mwb(message,uid,gid):
    uid = analysis.get_nick_name(message,gid,uid)
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
            board = Board()
            mfc = Mfc()
            mfcs[gid] = mfc
            status = mfc.conduct(message,uid,gid)
            if status == "Recruiting":
                print(">>>>> A", mfc.account,mfc.recruit_left)
                sys.stdout.flush()
                board.add_log(f"{uid} Starts!")
                report_status(board,uid,gid,mfc)
                board.save(uid,gid,mfc)
        
        elif command == 'join':
            if mfc.recruit_left > 0 :
                status = mfc.conduct(message,uid,gid)
                if status == "Recruiting" or "Wait" in status:
                    board = load_last_board(gid)
                    board.add_log(f"{uid} joined!")
                    report_status(board,uid,gid,mfc)
                    board.save(uid,gid,mfc)
                elif status == "Ignore":
                    print(f">>> MFC ignored {uid}")
                    sys.stdout.flush()
            else:
                print(f">>>> Recruits denied")
                sys.stdout.flush()
            

        elif command == 'help':
            m = "[CQ:image,file=mwb_help.png]"
            analysis.send_msg(m,uid=uid,gid=gid)
        
        elif command == 'check':
            status = mfc.conduct(message,uid,gid)
            if status == "Ignore":
                pass
            else:
                board = load_last_board(gid)
                result = board.check(uid)
                if result:
                    board.set_winner(uid)
                    report_status(board,uid,gid,mfc)
                    board.save(uid,gid,mfc)
                else:
                    board.set_winner( status.split()[1] )
                    report_status(board,uid,gid,mfc)
                    board.save(uid,gid,mfc)
                mfcs.pop(gid)

        else:
            if is_legal( message.text.split()[1:] ) and uid in mfc.waiting:
                board = load_last_board(gid)
                x,y,n = message.text.split()[1:4]
                x,y = to_number(x,y)
                n = int(n)
                result = board.assign(x,y,n,uid=uid)
                if result :
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
        analysis.send_msg(gid=gid,m=f'MWF ERROR')


#b = Board( )
#print(b.assign(1,1,1,uid="test"))
#b.to_png("a.png")


