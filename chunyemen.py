import analysis


def fetch_game_by_id(i_id):
    cmd = f"SELECT * from groupgame where id='{i_id}';"
    return analysis.source_mysql(cmd)[0]

class cym_game():
    def __init__(self, ,numplayers, players, guild = 'fighter'):
        self.create_variable()
        self.create_deck()
        self.create_equips()
        self.choose_seq()

    def dump_to_json(self):
        pass

    def restore_from_json(self,json):
        pass

    def insert_into_table(self):
        # insert into groupgame
        cmd = f"INSERT INTO groupgame (groupn,numplayers,players,gametype,starter,status,result) \
                            VALUES \
                        ( '{groupn}', {numplayers}, '{players}', '{gametype}', '{starter}','{status}','{result}' ); "
        analysis.source_mysql(cmd)
        cmd = f"SELECT id from groupgame where groupn='{gid}' ORDER BY id DESC LIMIT 1;"
        self.i_id = analysis.source_mysql(cmd)[0][0]
        
        self.dump_to_json()
        

def create_deck(guild = 'fighter'):
    
    pass
    

def create_game(numplayers,uid,gid):
    try:
        # create query in groupgame table
        if numplayers == 'infinity':
            numplayers = 999
        groupn = gid
        players = f"{uid} "
        gametype = "cym"
        starter = f"{uid}"

        # create game deck, insert into chunyemen table
        guild = 'fighter'
        cym = cym_game(numplayers = numplayers, players=players, guild=guild )
        cym.insert_into_table()
        i_id = cym.i_id

        m = f"纯爷们地下城 setup 完毕, 请私聊 '{i_id} 加入' 加入游戏! 当前的纯爷们有1/{numplayers}位, 是 {players} !"
        analysis.send_msg(m,uid=uid,gid=gid)

    except:
        analysis.send_msg("楚错了辣",uid=uid,gid=gid)
    

def start_game(i_id):
    game = fetch_game_by_id(i_id)
    i_id , groupn, numplayers, players, gametype, starter,status,result,time = game
    if status != 'recruiting':
        analysis.send_msg(f"游戏{i_id}已经开始或者已经结束,开始失败",uid=None,gid=groupn)
        return
    else:
        cmd = "UPDATE groupgame SET status='ongoing' WHERE id='{i_id}';"
        analysis.source_mysql(cmd)
        analysis.send_private_msg(f"游戏{i_id}开始")
        analysis.send_msg(f"游戏{i_id}开始, 纯爷们在酒馆开始畅饮了! 当前纯爷们{players}",uid=uid,gid=groupn)
    pass

def end_game(i_id):
    pass

def join_game(i_id,uid):
    game = fetch_game_by_id(i_id)
    i_id , groupn, numplayers, players, gametype, starter,status,result,time = game
    if status != 'recruiting':
        analysis.send_private_msg(f"游戏{i_id}已经开始或者已经结束,加入失败",uid=uid)
        return
    else:
        players += f"{uid} "
        cmd = "UPDATE groupgame SET players='{players}' WHERE id='{i_id}';"
        analysis.source_mysql(cmd)
        analysis.send_private_msg(f"您已加入游戏{i_id}")
        analysis.send_msg(f"{uid} 作为一个纯爷们加入了! 当前纯爷们{len(players.split())/{numplayers}",uid=uid,gid=groupn)
        

def forprivate(m,uid):
    pass



tmp = '''
MariaDB [seasons]> describe chunyemen;
+------------+---------------+------+-----+---------+----------------+
| Field      | Type          | Null | Key | Default | Extra          |
+------------+---------------+------+-----+---------+----------------+
| id         | int(11)       | NO   | PRI | NULL    | auto_increment |
| gameid     | int(11)       | YES  |     | NULL    |                |
| numplayers | int(11)       | YES  |     | NULL    |                |
| players    | varchar(1023) | YES  |     | NULL    |                |
| guild      | varchar(255)  | YES  |     | NULL    |                |
| deck       | varchar(1023) | YES  |     | NULL    |                |
| log        | varchar(1023) | YES  |     | NULL    |                |
| result     | varchar(1023) | YES  |     | NULL    |                |
+------------+---------------+------+-----+---------+----------------+

MariaDB [seasons]> describe chunyemen_log;
+-------------+---------+------+-----+---------+----------------+
| Field       | Type    | Null | Key | Default | Extra          |
+-------------+---------+------+-----+---------+----------------+
| id          | int(11) | NO   | PRI | NULL    | auto_increment |
| gameid      | int(11) | YES  |     | NULL    |                |
| stepid      | int(11) | YES  |     | NULL    |                |
| currentstep | int(11) | YES  |     | NULL    |                |
| status      | int(11) | YES  |     | NULL    |                |
+-------------+---------+------+-----+---------+----------------+

MariaDB [seasons]> describe chunyemen_status;
+---------------+---------------+------+-----+---------+----------------+
| Field         | Type          | Null | Key | Default | Extra          |
+---------------+---------------+------+-----+---------+----------------+
| id            | int(11)       | NO   | PRI | NULL    | auto_increment |
| deck          | varchar(1023) | YES  |     | NULL    |                |
| monsters      | varchar(1023) | YES  |     | NULL    |                |
| equips        | varchar(1023) | YES  |     | NULL    |                |
| songlist      | varchar(1023) | YES  |     | NULL    |                |
| yemenlist     | varchar(1023) | YES  |     | NULL    |                |
| battle_result | varchar(1023) | YES  |     | NULL    |                |
+---------------+---------------+------+-----+---------+----------------+
'''

