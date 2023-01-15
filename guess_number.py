from analysis import source_mysql,send_msg
import random as rd
import sys,os

MAX_TRIAL=10
PRE_TRIAL=7
L = 4

def error(gid = 0):
    send_msg(gid=gid,m="呜呜，又出错了")

def make_puzzle():
    answer = f"%0{L}d"%rd.randrange( 0, 10**L )
    print("A",answer)
    assert len(answer) == L 
    log = ''
    for i in range(PRE_TRIAL):
        trial = f"%0{L}d"%rd.randrange( 0, 10**L )
        print("T",trial)
        if trial != answer:
            a,b = analyze_query( answer,trial )
            log += f"{trial}:{a}:{b} "
    log = log.strip()
    cmd = f"INSERT INTO gn ( answer,queries, status ) VALUES ( '{answer}', '{log}', 0 )"
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

def log_into_database(answer, log, finished = 0):
    cmd = "SELECT * FROM gn  ORDER BY id DESC LIMIT 1;" 
    result = source_mysql(cmd)
    index = int(result[0][0])
    print(f"UPDATE gn SET queries='{log}',status={finished} WHERE id={index} ")
    cmd = f"UPDATE gn SET queries='{log}',status={finished} WHERE id={index} "
    result = source_mysql(cmd)
    return

def fetch_last_puzzle():
    cmd = "select * from gn  ORDER BY id DESC LIMIT 1;" 
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
        m += "输入 /1a2b xxxx 继续猜，或者/1a2b stop 停止猜数"
    else:
        m += "正确，TQL"
    send_msg(gid=gid,m=m)
    # print(m)
    return

def finish_puzzle():
    puzzle = fetch_last_puzzle()
    index = puzzle[0]
    cmd = f'UPDATE gn SET status=1 WHERE id={index}'
    result = source_mysql(cmd)
    return

# 猜数字                
def guess_number(message,uid,gid):
    query = '8888'
    try:
        query = message.text.split()[1]
    except:
        query = '9999'
    if query == 'stop':
        finish_puzzle()
        send_msg(gid =gid, m ="Thank you for playing.")
        return 
    print("Q",query)
    if check_finished(): # if finished
        # make new puzzle # log into database
        make_puzzle()
        # report current status
        report_status(gid=gid)
    else: # if not finished
        try:
            print(query)
            tmp,answer,log,status = fetch_last_puzzle()
            # query = message.text.split()[1]
            A,B = analyze_query(answer,query) # analysis new query
            if A != L: # if not right
                log_into_database(answer, log+f" {query}:{A}:{B}", finished=0)# log into database
                report_status(gid=gid) # report current status
                if len(log.split()) >= MAX_TRIAL - 1 :# if max trial
                    # Send End status, give answer
                    send_msg(gid=gid,m=f"Reach trial times limit. Stop.\nThe Answer is {answer}") 
                    finish_puzzle() # finish current puzzle
            else: # if right
                log_into_database(answer, log+f" {query}:{A}:{B}", finished=1)# log into database
                report_status(gid=gid) # report current status
                # finish current puzzle
        except Exception as e :
            print(e)
            finish_puzzle()
            error(gid=gid)
    pass

#print(analyze_query(sys.argv[1],sys.argv[2]))
#make_puzzle()
# report_status(gid=0)

