from analysis import source_mysql,send_msg
import random as rd
import sys,os

MAX_TRIAL=5
PRE_TRIAL=7
L = 6
n_trials = 0

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

def make_puzzle():
    global n_trials
    n_trials = 0
    if rd.random()>0.1:
        answer = f"%0{L}d"%rd.randrange( 0, 10**L )
    else:
        answer = "114514"

    assert len(answer) == L 
    log = ''

    trials = list()
    candidates = set([ f"%0{L}d"%x for x in range(10**L) ])
    while(True):
        if len(candidates) > 1:
            pass
        else:
            break
        trial = f"%0{L}d"%rd.randrange( 0, 10**L )
        if trial != answer:
            a,b = analyze_query( answer,trial )
            trials.append(trial)
            log += f"{trial}:{a}:{b} "
        candidates = truncate( candidates, trials, answer )

    log = log.strip()
    cmd = f"INSERT INTO gn6 ( answer,queries, status ) VALUES ( '{answer}', '{log}', 0 )"
    tmp = source_mysql(cmd)
    #print(answer)
    #print(log)
    #print(candidates)
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

def log_into_database(answer, log, finished = 0):
    cmd = "SELECT * FROM gn6  ORDER BY id DESC LIMIT 1;" 
    result = source_mysql(cmd)
    index = int(result[0][0])
    print(f"UPDATE gn6 SET queries='{log}',status={finished} WHERE id={index} ")
    cmd = f"UPDATE gn6 SET queries='{log}',status={finished} WHERE id={index} "
    result = source_mysql(cmd)
    return

def fetch_last_puzzle():
    cmd = "select * from gn6  ORDER BY id DESC LIMIT 1;" 
    result = source_mysql(cmd)
    return result[0]

def check_finished():
    last_puzzle = fetch_last_puzzle()
    if int(last_puzzle[-1]) == 1:
        return True
    else:
        return False

def report_status(uid=None,gid=None):
    puzzle = fetch_last_puzzle()
    log,status = puzzle[2:4]
    trials = log.split()
    m = ''
    for trial in trials:
        query,A,B = trial.split(":")
        m += f"{query}\t{A}A{B}B\n"
    if status == 0:
        m += "输入 /6a2b xxxxxx 继续猜，或者/6a2b stop 停止猜数"
    else:
        m += "正确，TQL"
    send_msg(gid=gid,m=m)
    # print(m)
    return

def finish_puzzle():
    puzzle = fetch_last_puzzle()
    index = puzzle[0]
    cmd = f'UPDATE gn6 SET status=1 WHERE id={index}'
    result = source_mysql(cmd)
    return

# 猜数字                
def guess_number(message,uid,gid):
    global n_trials
    query = '88888'
    try:
        query = message.text.split()[1]
    except:
        query = 'xxxxx'
    if query == 'stop':
        finish_puzzle()
        send_msg(gid =gid, m ="Thank you for playing.")
        return 
    if check_finished(): # if finished
        # make new puzzle # log into database
        make_puzzle()
        # report current status
        report_status(gid=gid)
    else: # if not finished
        try:
            print("Q",query)
            tmp,answer,log,status = fetch_last_puzzle()
            # query = message.text.split()[1]
            A,B = analyze_query(answer,query) # analysis new query
            if A != L: # if not right
                n_trials += 1
                # log_into_database(answer, log, finished=0)# log into database
                report_status(gid=gid) # report current status
                if not query == "xxxxxx":
                    send_msg(gid=gid,m=f"{query} 不对哦，请再想想") 
                if n_trials >= MAX_TRIAL:
                # if len(log.split()) >= MAX_TRIAL - 1 :# if max trial
                    # Send End status, give answer
                    send_msg(gid=gid,m=f"Reach trial times limit. Stop.\nThe Answer is {answer}") 
                    finish_puzzle() # finish current puzzle
            else: # if right
                send_msg(gid=gid,m=f"您TQL，没错，就是 {answer}") 
                if query == "114514":
                    send_msg(gid=gid,m="/dianzan 野兽先辈") 
                else:
                    send_msg(gid=gid,m="/dianzan") 
                #log_into_database(answer, log+f" {query}:{A}:{B}", finished=1)# log into database
                #report_status(gid=gid) # report current status
                # finish current puzzle
                finish_puzzle()
        except Exception as e :
            print(e)
            finish_puzzle()
            error(gid=gid)
    pass

#print(analyze_query(sys.argv[1],sys.argv[2]))
# make_puzzle()
# report_status(gid=0)



