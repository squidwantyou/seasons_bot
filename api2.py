import requests
import function as fc
from analysis import *
from guess_number import guess_number

def keyword(message,uid,gid = None):
    message = Message(message)
    # if gid == 144744787 or gid == 530879511:
    if True:
        if true_startswith( message, '/' ): 
            if true_startswith( message, '/help','/帮助' ): 
                fc.help(message,uid,gid)
            if true_startswith( message, '/笑话','/苏联笑话' ): 
                fc.xiaohua(message,uid,gid)
           # if true_startswith( message, '/色图','/瑟图','/setu' ): 
           #     fc.setu(message,uid,gid)
           # if true_startswith( message, '/添加色图','/加入瑟图','/添加瑟图','/加入色图'): 
           #     fc.add_setu(message,uid,gid)
            if true_startswith( message, '/+bga' ): 
                fc.addid(message,uid,gid)
            if true_startswith( message, '/?bga' ): 
                fc.getid(message,uid,gid)
            if true_startswith( message, '/roll' ): 
                fc.roll(message,uid,gid)
           # if true_startswith( message, '/语录' ): 
           #     fc.yvlu(message,uid,gid)
           # if true_startswith( message, '/添加语录','/加入语录' ): 
           #     fc.add_yvlu(message,uid,gid)
            if true_startswith( message, '/吃什么' ): 
                fc.meal(message,uid,gid)
            if true_startswith( message, '/加入菜单','/添加菜单' ): 
                fc.add_meal(message,uid,gid)
            if true_startswith( message, '/猜数字','/1a2b' ): 
                guess_number(message,uid,gid)


# keyword( '/+bga [CQ:at,qq=937404959]  zyyzxyz', '' , 144744787 )
