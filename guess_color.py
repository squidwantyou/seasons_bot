from analysis import source_mysql,send_msg
import random as rd
import sys,os

MAX_TRIAL=3
PRE_TRIAL=7
QQPC_LIMIT=30
n_trials = 0
L = 5
default_L = 5
K = 4
default_K = 4
KMAX = 6

def get_all_colors():
    return "红蓝黑白绿紫"[:K]

def error(gid = 0):
    send_msg(gid=gid,m="呜呜，又出错了")

def truncate( candidates, trials,answer ):
    remove = set()
    for trial in trials[-1:]:
        for c in candidates:
            a,b = analyze_query( answer,trial )
            ac,bc = analyze_query( c,trial )
            if a==ac and b==bc:
                pass
            else:
                remove.add(c)
    return candidates - remove

def create_query():
    global K
    global L
    q = ''
    for i in range(L):
        q += str( rd.randrange(K) )
    return q

def create_all_queries():
    global K
    global L
    s = set()
    for i in range( K**L ):
        q=''
        for j in range(1,L+1):
           q += str( i%(K**j)//(K**(j-1)))
        s.add(q)
    return s

def make_puzzle(gid=None):
    global n_trials
    global L
    n_trials = 0
    # answer = f"%0{L}d"%rd.randrange( 0, 10**L )
    answer = create_query()
    assert len(answer) == L 
    log = ''

    trials = list()
    candidates = create_all_queries()
    while(True):
        if len(candidates) <= 1:
            break
        trial = create_query()
        if trial != answer:
            a,b = analyze_query( answer,trial )
            trials.append(trial)
            log += f"{trial}:{a}:{b} "
        candidates = truncate( candidates, trials, answer )

    log = log.strip()
    cmd = f"INSERT INTO gnc ( answer,queries, status, qqgroup ) VALUES ( '{answer}', '{log}', 0, '{gid}' )"
    tmp = source_mysql(cmd)
    return

def analyze_query( answer, query ) :
    assert len(answer) == len(query)
    keys = set( list(answer) )
    a_count = dict()
    b_count = dict()
    for key in keys:
        a_count[key] = 0
        b_count[key] = 0
    a = 0
    b = 0
    for i,j in zip(answer,query):
        if i == j :
            a += 1
            a_count[i] += 1
    for key in keys:
        b_count[key] = min( answer.count(key), query.count(key) )
        b_count[key] -= a_count[key]
    b = sum(b_count.values())
    return (a,b)

def log_into_database(answer, log, gid, finished = 0):
    cmd = "SELECT * FROM gnc   where qqgroup='{gid}' ORDER BY id DESC LIMIT 1;" 
    result = source_mysql(cmd)
    index = int(result[0][0])
    # print(f"UPDATE gnc SET queries='{log}',status={finished} WHERE id={index} ")
    cmd = f"UPDATE gnc SET queries='{log}',status={finished} WHERE id={index} and qqgroup='{gid}' "
    result = source_mysql(cmd)
    return

def fetch_last_puzzle(gid):
    cmd = f"select * from gnc where qqgroup='{gid}' ORDER BY id DESC LIMIT 1;" 
    result = source_mysql(cmd)
    try:
        return result[0]
    except Exception as e:
        print(e)
        return [ 0,'','',1,None ]

def check_finished(gid):
    last_puzzle = fetch_last_puzzle(gid)
    print(last_puzzle)
    if int(last_puzzle[-2]) == 1:
        return True
    else:
        return False

def color_to_query(color):
    ctoq = { "红":'0' , "蓝":'1' , "黑":'2' , "白":'3', "绿":'4', "紫":'5',
             '🔴':'0' , '🔵':'1' , '⚫':'2' , '⚪':'3', "💚":'4', "💜":'5' }
    query = ''
    for i in color:
        query = query + ctoq[i]
    return query

def query_to_emoji(query):
    qtoe = { "0":'🔴' , "1":'🔵' , "2":'⚫' , "3":'⚪', "4":"💚", "5":"💜" }
    emoji = ''
    for i in query:
        emoji = emoji + qtoe[i]
    return emoji

def report_status(gid,uid=None):
    global QQPC_LIMIT
    tmp  = 0
    puzzle = fetch_last_puzzle(gid)
    log,status = puzzle[2:4]
    trials = log.split()
    all_m = list()
    cm = ''
    for trial in trials:
        query,A,B = trial.split(":")
        emoji = query_to_emoji(query)
        tmp += len(query)
        if tmp > QQPC_LIMIT:
            all_m.append(cm)
            cm = ''
            tmp = len(query)
        else:
            pass
        cm += f"{emoji}\t{A}A{B}B\n"

    all_m.append(cm)

    if status == 0:
        all_m[-1] += f"输入如 /guess {get_all_colors()} 继续猜，或者/guess stop 停止猜数"
    else:
        all_m[-1] += "正确，TQL"

    for m in all_m:
        send_msg(gid=gid,m=m)
    # print(m)
    return

def finish_puzzle(gid):
    try:
        puzzle = fetch_last_puzzle(gid)
        index = puzzle[0]
        cmd = f'UPDATE gnc SET status=1 WHERE id={index}'
        result = source_mysql(cmd)
    except Exception as e:
        print(e)
        return

# 猜数字                
def guess_color(message,uid,gid):
    global n_trials
    global L
    global default_L
    global K
    global default_K
    global KMAX
    color = ''
    try:
        color = message.text.split()[1]
    except:
        color = None

    if color == None:
        if check_finished(gid): # if finished
            color = 'new'
        else:
            report_status(gid)
        
    if color == 'stop':
        finish_puzzle(gid)
        send_msg(gid =gid, m ="Thank you for playing.")
        return 

    if color == 'new':
        finish_puzzle(gid)
        try:
            user_L = int(message.text.split()[2])
        except:
            user_L = default_L
        try:
            user_K = int(message.text.split()[3])
        except:
            user_K = default_K

        if user_K ** user_L >= 500000 or user_K > KMAX or user_L < 2 or user_K < 2:
            user_L = default_L
            user_K = default_K
        L = user_L
        K = user_K

    if color == 'cheat':
        finish_puzzle(gid)
        tmp,answer,log,status ,qqgroup= fetch_last_puzzle(gid)
        emoji = query_to_emoji(answer)
        send_msg(gid=gid,m=f'正确答案是：{emoji}, 放弃就是这种感觉，必可活用于下一次')
        return

    if check_finished(gid): # if finished
        # make new puzzle # log into database
        make_puzzle(gid)
        # report current status
        report_status(gid)
    else: # if not finished
        try:
            try:
                query = color_to_query(color)
            except:
                send_msg(gid=gid,m=f"你的颜色很美丽，而我只有{get_all_colors()}") 
                return
            print("Q",query,color)
            tmp,answer,log,status ,qqgroup = fetch_last_puzzle(gid)
            # query = message.text.split()[1]
            try:
                A,B = analyze_query(answer,query) # analysis new query
            except:
                send_msg(gid=gid,m=f"?") 
                return
            if A != L: # if not right
                n_trials += 1
                # log_into_database(answer, log, finished=0)# log into database
                # report_status(gid=gid) # report current status
                send_msg(gid=gid,m=f"{color} 不对哦，请再想想") 
                if n_trials >= MAX_TRIAL:
                # if len(log.split()) >= MAX_TRIAL - 1 :# if max trial
                    # Send End status, give answer
                    send_msg(gid=gid,m=f"Reach trial times limit. Stop.\nThe Answer is {answer}") 
                    finish_puzzle(gid) # finish current puzzle
            else: # if right
                emoji = query_to_emoji(query)
                send_msg(gid=gid,m=f"您TQL，没错，就是 {emoji}") 
                #log_into_database(answer, log+f" {query}:{A}:{B}", finished=1)# log into database
                #report_status(gid=gid) # report current status
                # finish current puzzle
                finish_puzzle(gid)
        except Exception as e :
            print(e)
            finish_puzzle(gid)
            error(gid=gid)

    pass

#print(analyze_query(sys.argv[1],sys.argv[2]))
#make_puzzle()
# report_status(gid=0)
# L = 4
# K = 3
# s = create_all_queries()
# print(s)

