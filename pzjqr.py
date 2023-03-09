#!/usr/bin/env python3
import base64
import sys,os
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patches as mpatches
import random as rd
import pickle
import numpy as np
from analysis import source_mysql,send_msg
import analysis

FILENAME='pzjqr.png'
N = 16
margin = 0
# rd.seed(2)

def make_board(ax):
    global N
    global margin
    # add boarder line
    linelist  = [   [(-0.5,-0.5),(-0.5,N-0.5)],
            [(-0.5,-0.5),(N-0.5,-0.5)],
            [(-0.5,N-0.5),(N-0.5,N-0.5)],
            [(N-0.5,-0.5),(N-0.5,N-0.5)] ]
    x = [ x[0] for x in linelist ]
    y = [ x[1] for x in linelist ]
    line_segs = LineCollection( linelist,lw=5,color='black',alpha = 0.7 ) 
    ax.add_collection( line_segs )

    # add inner line
    linelist = list()
    for i in range(N-1):
        linelist.append( ((0.5+i,-0.5),(0.5+i,N-0.5)) ) # v
        linelist.append( ((-0.5,0.5+i),(N-0.5,0.5+i)) ) # h

    line_segs = LineCollection( linelist,lw=2,color='black',alpha = 0.3 ) 
    ax.add_collection( line_segs )

    return

def test(ax):
    poly = mpatches.RegularPolygon( (1,1),5,radius=0.4,color='r',alpha = 0.3)
    poly1 = mpatches.RegularPolygon( (2,2),5,radius=0.4,color='b',alpha = 0.3)
    poly2 = mpatches.RegularPolygon( (3,3),5,radius=0.4,color='g',alpha = 0.3)
    poly3 = mpatches.RegularPolygon( (4,4),5,radius=0.4,color='y',alpha = 0.3)
    poly4 = mpatches.RegularPolygon( (0,0),5,radius=0.4,color='pink',alpha = 0.3)
    ax.add_artist( poly )
    ax.add_artist( poly1)
    ax.add_artist( poly2)
    ax.add_artist( poly3)
    ax.add_artist( poly4)

def init():
    plt.clf()
    fig,ax = plt.subplots(figsize = (8,8))

    ax.set_xlim( (-0.5-margin, N-0.5+margin) )
    ax.set_ylim( (-0.5-margin, N-0.5+margin) )
    ax.axis('off')

    return fig,ax

def draw_wall(ax,walls,lw=8, color='#A84448',alpha = 0.7):
    for t,x,y in walls:
        if t == 'h':
            left = (x-0.5,y+0.5)
            right = (x+0.5,y+0.5)
        elif t == 'v':
            left = (x+0.5,y-0.5)
            right = (x+0.5,y+0.5)
        linelist  = [[left,right],]
        line_segs = LineCollection( linelist,lw=lw,color=color,alpha = alpha) 
        ax.add_collection( line_segs )

def draw_token(ax,locs,alpha = 0.7):
    for t,x,y in locs:
        if t in ['b','r','g','y','x']:
            if t != 'x':
                poly = mpatches.RegularPolygon( (x,y),3,radius=0.4,color=t,alpha = 0.5)
            else:
                poly = mpatches.RegularPolygon( (x,y),3,radius=0.4,color='black',alpha = 0.5)
            ax.add_artist( poly )
        if t in ['ro','bo','go','yo']:
            poly = mpatches.Circle( (x,y),radius=0.4,color=t[0],alpha = 0.9)
            ax.add_artist( poly )

def draw_center(ax):
    global N
    draw_wall(ax,[['h',7,6]],color = 'black',lw=5 )
    draw_wall(ax,[['h',8,6]],color = 'black',lw=5 )
    draw_wall(ax,[['h',7,8]],color = 'black',lw=5 )
    draw_wall(ax,[['h',8,8]],color = 'black',lw=5 )
    draw_wall(ax,[['v',6,7]],color = 'black',lw=5 )
    draw_wall(ax,[['v',6,8]],color = 'black',lw=5 )
    draw_wall(ax,[['v',8,7]],color = 'black',lw=5 )
    draw_wall(ax,[['v',8,8]],color = 'black',lw=5 )
    
class Board:
    def __init__(self):
        self.board1 =[ ['v',6,0  ], ['v',2,1  ], ['v',5,2  ], ['v',3,5  ], ['v',1,6  ],
            ['v',5,7 ], ['h',3, 1], ['h',5, 2], ['h',0, 3], ['h',4, 4],
            ['h',1, 5], ['h',5, 7],
            ]
        board2 =[ ['v',11,0 ],  ['v',9,2  ], ['v',12,4 ], ['v',8,5  ], ['v',14,6 ],
            ['h',10,2], ['h',13,3], ['h',15,4], ['h',8, 5], ['h',14,5],
            ]
        self.board2 = rotate_wall( board2,90 )
        board3 =[ ['v',2,9  ], ['v',6,12 ], ['v',1,13 ], ['v',3,14 ], ['v',1,15],
            ['h',3, 8], ['h',0, 9], ['h',6, 11], ['h',1,    13], ['h',4,    14],
            ]
        self.board3 = rotate_wall( board3,270 )
        board4 =[ ['v',11,9 ], ['v',13,10 ], ['v',9,13 ], ['v',12,14], ['v',11,15],
            ['h',11,9], ['h',14,9], ['h',15,11], ['h',9,    12], ['h',13,14],
            ]
        self.board4 = rotate_wall( board4,180 )
        self.all_boards = [ self.board1,self.board2,self.board3,self.board4 ]
        self.generate_target()
        self.generate_board()
        self.choose_target()
        self.generate_robots()
    
    def generate_target(self):
        target1 = [ ['b',1,6 ],['x',5,7],['g',4,5],['r',5,2],['y',3,1] ]
        target2 = [ ['b',2,5 ],['g',4,2],['r',5,7],['y',6,1] ]
        target3 = [ ['b',6,3 ],['g',2,1],['r',1,4],['y',3,6] ]
        target4 = [ ['b',6,2 ],['g',1,5],['r',2,1],['y',4,6] ]
        self.all_targets = [target1 , target2 , target3 , target4]

    def generate_board(self):
        tmp = self.all_boards # [self.board1,self.board2,self.board3,self.board4]
        tmp_tar = self.all_targets
        index = list( range(len(tmp)) )
        rd.shuffle( index )
        
        for i in range(4):
            tmp[ index[i] ] = rotate_wall( tmp[ index[i] ],90*i )
            tmp_tar[ index[i] ] = rotate_loc( tmp_tar[ index[i] ], 90*i )

        self.current_board = tmp[0] + tmp[1] + tmp[2] + tmp[3]
        self.current_targets = tmp_tar[0] + tmp_tar[1] + tmp_tar[2] + tmp_tar[3]


        self.obs = list()
        self.obs.append( (int(N/2),int(N/2)) )
        self.obs.append( (int(N/2-1),int(N/2)) )
        self.obs.append( (int(N/2),int(N/2-1)) )
        self.obs.append( (int(N/2-1),int(N/2-1)) )

        self.obs_wall = np.zeros( [N,N,N,N] )
        for i,x,y in self.current_board:
            if i=='v':
                self.obs_wall[x,y,x+1,y] = 1
                self.obs_wall[x+1,y,x,y] = 1
            if i=='h':
                self.obs_wall[x,y,x,y+1] = 1
                self.obs_wall[x,y+1,x,y] = 1
        return 

    def choose_target(self):
        self.target = rd.choice( self.current_targets )
    
    def check_goal(self):
        c,rx,ry = self.target
        r = c + 'o' 
        if c != 'x':
            for i,x,y in self.current_robots:
                if r==i and x == rx and y == ry :
                    return True
        else:
            for i,x,y in self.current_robots:
                if x == rx and y == ry :
                    return True
        return False

    def reset(self):
        self.current_robots = self.init_robots[:]

    def generate_robots(self):
        self.init_robots = list()
        known = set()
        for i in 'r','b','g','y':
            while True:
                x = rd.randrange(0,N)
                y = rd.randrange(0,N)
                if (x,y) not in self.obs:
                #     self.obs.append( (x,y) )
                #     break
                    if (x,y) not in known:
                        known.add( (x,y) )
                        self.init_robots.append( ( i+'o',x,y) )
                        break
        self.current_robots = self.init_robots[:]

    def conduct_path(self,path):
        for p in path.split():
            r = p[0]+'o'
            for d in p[1:]:
                self.move_once( r,d )
        pass

    def move_once(self,r,d):
        while True:
            result = self.move_one_step(r,d)# try to move one step
            if result:
                self.update_robot(r,result)
            else:
                break
    
    def update_robot(self,r,result):
        for i,loc in enumerate(self.current_robots):
            if loc[0] == r:
                #self.obs.remove( (loc[1],loc[2]) )
                #self.obs.append( tuple(result) )
                self.current_robots[i] = ( (r,result[0],result[1]) )

    def get_robot_loc(self, r ):
        assert r in ('ro','bo','go','yo' )
        for loc in self.current_robots:
            if loc[0] == r:
                return (loc[1],loc[2] )
    
    def move_one_step(self, r,d ):
        global N
        x,y = self.get_robot_loc( r )

        # generate shadow loc
        shadow_loc = (None,None)
        if d == 'u':
            shadow_loc = [x,y+1]
        elif d == 'd':
            shadow_loc = [x,y-1]
        elif d == 'l':
            shadow_loc = [x-1,y]
        elif d == 'r':
            shadow_loc = [x+1,y]

        # check outboard
        if not 0<=shadow_loc[0]<N :
            return False
        if not 0<=shadow_loc[1]<N :
            return False

        # check obs
        if tuple(shadow_loc) in self.obs :
            return False

        if ('ro',shadow_loc[0],shadow_loc[1] ) in self.current_robots:
            return False
        if ('bo',shadow_loc[0],shadow_loc[1] ) in self.current_robots:
            return False
        if ('go',shadow_loc[0],shadow_loc[1] ) in self.current_robots:
            return False
        if ('yo',shadow_loc[0],shadow_loc[1] ) in self.current_robots:
            return False

        # check wall
        check_obs = None
        if self.obs_wall[x,y,shadow_loc[0],shadow_loc[1]]:
            return False

        return shadow_loc

    def find_path(self,limit=8, cp = '',allcp = ''):
        if limit == 0:
            return False

        backup_current_robots = self.current_robots[:]
        self.conduct_path(cp)
        if self.check_goal():
            return allcp
        else:
            all_choices = self.get_choices()
            for tmpcp in all_choices:
                newcp = allcp + " " + tmpcp
                resultcp = self.find_path( limit-1,cp = tmpcp,allcp = newcp)
                if resultcp:
                    return resultcp 
        self.current_robots = backup_current_robots

    def get_choices(self,negative = False):
        global N
        all_choices = list()
        reverse_d = { 'u':'d', 'd':'u','l':'r','r':'l' }
        for r in ('r','b','g','y'):
            for d in ('u','d','l','r'):
                if negative and r == negative[0] and d == reverse_d[negative[1]]:
                    continue
                if negative and r == negative[0] and d == negative[1]:
                    continue

                x,y = self.get_robot_loc( r+'o' )

                shadow_loc = (None,None)
                if d == 'u':
                    shadow_loc = [x,y+1]
                elif d == 'd':
                    shadow_loc = [x,y-1]
                elif d == 'l':
                    shadow_loc = [x-1,y]
                elif d == 'r':
                    shadow_loc = [x+1,y]

                # check outboard
                if not 0<=shadow_loc[0]<N :
                    continue
                if not 0<=shadow_loc[1]<N :
                    continue

                # check obs
                if tuple(shadow_loc) in self.obs :
                    continue

                if ('ro',shadow_loc[0],shadow_loc[1] ) in self.current_robots:
                    continue
                if ('bo',shadow_loc[0],shadow_loc[1] ) in self.current_robots:
                    continue
                if ('go',shadow_loc[0],shadow_loc[1] ) in self.current_robots:
                    continue
                if ('yo',shadow_loc[0],shadow_loc[1] ) in self.current_robots:
                    continue

                # check wall
                if self.obs_wall[x,y,shadow_loc[0],shadow_loc[1]]:
                    continue

                all_choices.append( r+d )

        return all_choices
                
    def find_path_flood(self,start=0,states = [],limit = 6 ):
        if start == limit:
            return False
        
        if start == 0 :
            states = [ (self.current_robots,'',False) ]

        new_states = list()
        for robot_locs, path, last in states:
            choices = self.get_choices( negative = last )
            for c in  choices:
                new_path = path + " " + c
                self.current_robots = robot_locs[:]
                self.conduct_path( c )
                if self.check_goal():
                    return new_path
                else:
                    new_s = [ self.current_robots[:], new_path, c ]
                    new_states.append(new_s)

        return self.find_path_flood( start = start + 1, states = new_states, limit = limit )
                        
def rotate_wall( walls, angle ) :
    boardx = list()
    # rotate 180:
    if angle == 180:
        for i in walls:
            if i[0] == 'h':
                boardx.append( ['h',15-i[1],14-i[2] ] )
            if i[0] == 'v':
                boardx.append( ['v',14-i[1],15-i[2] ] )
    # rotate 90
    if angle == 90:
        for i in walls:
            if i[0] == 'h':
                boardx.append( ['v',i[2],15-i[1] ] )
            if i[0] == 'v':
                boardx.append( ['h',i[2],14-i[1] ] )
    # rotate 270
    if angle == 270:
        for i in walls:
            if i[0] == 'h':
                boardx.append( ['v',14-i[2],i[1] ] )
            if i[0] == 'v':
                boardx.append( ['h',15-i[2],i[1] ] )
    if angle == 0:
        return walls
    return boardx

def rotate_loc( locs, angle ) :
    nlocs = list()
    # rotate 180:
    if angle == 180:
        for i in locs:
            nlocs.append( [i[0],15-i[1],15-i[2] ] )
    # rotate 90
    if angle == 90:
        for i in locs:
            nlocs.append( [i[0],i[2],15-i[1] ] )
    # rotate 270
    if angle == 270:
        for i in locs:
            nlocs.append( [i[0],15-i[2],i[1] ] )
    if angle == 0:
        return locs
    return nlocs

def draw_state(board,outfile = 'tmp.png',title="",xlabel = '' ):
    global N 
    fig,ax = init()
    make_board(ax)
    draw_center(ax)
    draw_wall(ax, board.current_board ) 
    draw_token(ax, [board.target,] )
    draw_token(ax, board.current_robots )
    ax.set_title(title,fontsize=30)
    ax.text( N/2,-1,xlabel,horizontalalignment='center',verticalalignment='top',fontsize=20)
    plt.savefig(outfile)

def check_finished(gid):
    try:
        last_puzzle = fetch_last_puzzle(gid)
        if int(last_puzzle[2]) == 1:
            return True
        else:
            return False
    except:
        return True

def report_status(gid,i_d = None):
    global FILENAME
    #id int auto_increment, puzzle VARBINARY(1000), status int, steps int, path varchar(255), qqgroup varchar(255) , primary key(id));
    puzzle = fetch_last_puzzle(gid,i_d = i_d)
    
    i_d,blob ,status ,steps ,path,group,qq = puzzle[0:7]
    missing_padding = len(blob) % 4
    if missing_padding != 0:
        blob += '='* (4 - missing_padding)
    board = pickle.loads( base64.b64decode(blob) )
    title = f"#{i_d}"
    xlabel = f"Known best solution is {steps} steps.\n{path} BY @{qq}"
    draw_state(board,f"data/images/{gid}_{FILENAME}",title= title, xlabel=xlabel)
    send_msg(f"[CQ:image,file={gid}_{FILENAME}]",gid=gid)
    return

def finish_puzzle(gid):
    try:
        puzzle = fetch_last_puzzle(gid)
        index = puzzle[0]
        cmd = f'UPDATE gnc SET status=1 WHERE id={index}'
        result = source_mysql(cmd)
    except Exception as e:
        return
    pass

def update_puzzle(gid,steps ,path,qq="0",i_d = None):
    puzzle = fetch_last_puzzle(gid,i_d = i_d )
    index , blob ,status ,old_steps = puzzle[0:4]
    if old_steps <= steps:
        return
    else:
        cmd = f"UPDATE pzjqr SET steps={steps},path='{path}',solver='{qq}' WHERE id={index} and qqgroup='{gid}' "
        result = source_mysql(cmd)
    return

def make_puzzle(gid):
    board = Board()
    blob = pickle.dumps(board)
    blob = base64.b64encode(blob).decode()
    sys.stdout.flush()
    #id int auto_increment, puzzle VARBINARY(1000), status int, steps int, path varchar(255), qqgroup varchar(255) , primary key(id));
    cmd = f"INSERT INTO pzjqr ( puzzle ,status , steps , path , qqgroup,solver ) VALUES ( '{blob}' , 0, 9999, 'xx', '{gid}' ,'Cthulhu')"
    tmp = source_mysql(cmd)
    return

def fetch_last_puzzle(gid,i_d = None):
    if i_d == None:
        cmd = f"select * from pzjqr where qqgroup='{gid}' ORDER BY id DESC LIMIT 1;" 
    else:
        i_d = int(i_d)
        cmd = f"select * from pzjqr where qqgroup='{gid}' and id={i_d};"
    result = source_mysql(cmd)
    try:
        return result[0]
    except Exception as e:
        return [ 0,'',1,9999,'xx',None ]

def load_last_board(gid,i_d = None):
    board = None
    try:
        global FILENAME
        #id int auto_increment, puzzle VARBINARY(1000), status int, steps int, path varchar(255), qqgroup varchar(255) , primary key(id));
        puzzle = fetch_last_puzzle(gid,i_d = i_d)
        blob ,status ,steps = puzzle[1:4]
        missing_padding = len(blob) % 4
        if missing_padding != 0:
            blob += '='* (4 - missing_padding)
        board = pickle.loads( base64.b64decode(blob) )
    except Exception as e:
        send_msg("O_O",uid=0,gid=gid)
    return board

def sanitize_path(path):
    newpath = ''
    if not path:
        return ''
    for i in path.split():
        r = ''
        if i[0] not in "rgby":
            raise Exception
        else:
            r = i[0]
            for d in i[1:]:
                if d in "udlr":
                    r+=d
        newpath = newpath + " " + r
    return newpath


# create table pzjqr ( id int auto_increment, puzzle VARBINARY(1000), status int, qqgroup varchar(255) , primary key(id));
def pzjqr( message, uid, gid ):
    path = ''
    try:
        path = " ".join(message.text.split()[1:])
    except:
        path = ''

    if path == '':
        if check_finished(gid): # if finished
            path = 'new'
        else:
            report_status(gid)
            return
        
    if path == 'stop':
        finish_puzzle(gid)
        analysis.send_msg(gid =gid, m ="Thank you for playing.")
        return 

    elif path == 'new':    # make new puzzle
        finish_puzzle(gid)
        make_puzzle(gid)
        report_status(gid)

    elif check_finished(gid): # if finished
        make_puzzle(gid)
        report_status(gid)

    elif path == 'help':
        m = "[CQ:image,file=pzjqr_help.png]"
        analysis.send_msg(m,uid=uid,gid=gid)

    elif path.isdigit():  # if query historic puzzle
        try:
            report_status(gid,i_d = int(path) )
        except:
            analysis.send_msg("O_O 找不到捏",uid=uid,gid=gid)

    elif path.split()[0] == 'update':
        try:
            i_d = int(path.split()[1])
            path = " ".join( path.split()[2:] )
            path = sanitize_path(path)
            board = load_last_board(gid,i_d = i_d )
            steps = sum( [ len(x) -1 for x in path.split() ] )
            board.conduct_path(path)
            if board.check_goal():
                update_puzzle(gid,steps,path,qq=uid, i_d = i_d )
                analysis.send_msg(f"您的新解是:{path}",uid=uid,gid=gid)
                report_status(gid,i_d = i_d )
            else:
                draw_state(board,f"data/images/tmp_{gid}_{FILENAME}")
                send_msg(f"[CQ:image,file=tmp_{gid}_{FILENAME}]",gid=gid)
                analysis.send_msg("不太正确哦 =_=",uid=uid,gid=gid)
            pass
        except:
            analysis.send_msg("并不容易呢~",uid=uid,gid=gid)
            
        pass

    else: # conduct path
        try:
            # load board
            board = load_last_board(gid)
            path = sanitize_path(path)
            steps = sum( [ len(x) -1 for x in path.split() ] )
            board.conduct_path(path)

            print("result:",board.check_goal())
            sys.stdout.flush()
            if board.check_goal():
                update_puzzle(gid,steps,path,qq=uid)
                # draw_state(board,f"data/images/tmp_{gid}_{FILENAME}")
                # send_msg(f"[CQ:image,file=tmp_{gid}_{FILENAME}]",gid=gid)
                analysis.send_msg(f"TQL! 您的解是:{path}",uid=uid,gid=gid)
                report_status(gid)
            else:
                draw_state(board,f"data/images/tmp_{gid}_{FILENAME}")
                send_msg(f"[CQ:image,file=tmp_{gid}_{FILENAME}]",gid=gid)
                analysis.send_msg("似乎没有走到终点=_=",uid=uid,gid=gid)
            pass

        except Exception as e :
            print(e)
            sys.stdout.flush()
            analysis.send_msg("X=_=X 小触手看不懂这个耶",uid=uid,gid=gid)

#m = analysis.Message("")
#m.text = '/pz new'
#pzjqr( m, 0,0)

