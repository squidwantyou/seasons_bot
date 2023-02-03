import requests
import function as fc
from analysis import *
#from guess_number import guess_number
from guess_number_2 import guess_number
import guess_number_five 
import ecy
import scy
import touhou
import moyu
import guess_color
import other
import zaoan
import delay

def keyword(message,uid,gid = None):
    message = Message(message)
    if True:
        if true_startswith( message, '/' ): 
            if true_startswith( message, '/help','/帮助' ): 
                fc.help(message,uid,gid)
            elif true_startswith( message, '/笑话','/苏联笑话' ): 
                fc.xiaohua(message,uid,gid)
            elif true_startswith( message, '/+bga' ): 
                fc.addid(message,uid,gid)
            elif true_startswith( message, '/?bga' ): 
                fc.getid(message,uid,gid)
            elif true_startswith( message, '/roll' ): 
                fc.roll(message,uid,gid)
            elif true_startswith( message, '/语录' ): 
                fc.yvlu(message,uid,gid)
            elif true_startswith( message, '/添加语录','/加入语录' ): 
                fc.add_yvlu(message,uid,gid)
            elif true_startswith( message, '/吃什么' ): 
                fc.meal(message,uid,gid)
            elif true_startswith( message, '/加入菜单','/添加菜单' ): 
                fc.add_meal(message,uid,gid)
            elif true_startswith( message, '/猜数字','/1a2b' ): 
                guess_number(message,uid,gid)
            elif true_startswith( message, '/猜颜色','/guess' ): 
                guess_color.guess_color(message,uid,gid)
            elif true_startswith( message, '/5a2b' ): 
                guess_number_five.guess_number(message,uid,gid)
            elif true_startswith( message, '/诗词' ,'/一次元'): 
                fc.shici(message,uid,gid)
            elif true_startswith( message, '/摸鱼','/moyu' ): 
                moyu.moyu(message,uid,gid)
            elif true_startswith( message, '/早安','/晚安' ): 
                zaoan.zaoan(message,uid,gid)
            elif true_startswith( message, '/提醒','/delay' ): 
                delay.delay(message,uid,gid)
            else:
                other.other(message,uid,gid)


