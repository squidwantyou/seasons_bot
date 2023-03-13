import requests
import function as fc
from analysis import *
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
import choose
import echo
import fsort
import douyingirl
import loop
import fother
import pzjqr
import fhelp

def keyword(message,uid,gid = None):
    message = Message(message)
    if True:
        if true_startswith( message, '/' ): 
            if true_startswith( message, '/help','/list','/帮助' ): 
                fhelp.fhelp(message,uid=uid,gid=gid)
            elif true_startswith( message, '/笑话','/苏联笑话' ): 
                fc.xiaohua(message,uid,gid)
#            elif true_startswith( message, '/色图','/瑟图','/setu' ): 
#                fc.setu(message,uid,gid)
            elif true_startswith( message, '/添加色图','/加入瑟图','/添加瑟图','/加入色图'): 
                fc.add_setu(message,uid,gid)
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
            elif true_startswith( message, '/土味' ,'/twqh','/土味情话'): 
                fc.tuweiqinghua(message,uid,gid)
            elif true_startswith( message, '/情话' ,'/qh'): 
                fc.tuweiqinghua(message,uid,gid)
            elif true_startswith( message, '/二次元','/ecy' ,'/水煮鱼' ): 
                ecy.ecy(message,uid,gid)
            elif true_startswith( message, '/三次元','/scy','/酸菜鱼' ): 
                scy.scy(message,uid,gid)
            elif true_startswith( message, '/车万','/touhou','/松鼠鱼' ): 
                touhou.touhou(message,uid,gid)
            elif true_startswith( message, '/摸鱼','/moyu' ): 
                moyu.moyu(message,uid,gid)
            elif true_startswith( message, '/早安','/晚安' ): 
                zaoan.zaoan(message,uid,gid)
            elif true_startswith( message, '/提醒','/delay' ): 
                delay.delay(message,uid,gid)
            elif true_startswith( message, '/循环','/loop' ): 
                loop.loop(message,uid,gid)
            elif true_startswith( message, '/选择','/choose','/choice' ): 
                choose.choose(message,uid,gid)
            elif true_startswith( message, '/排序','/sort'): 
                fsort.fsort(message,uid,gid)
            elif true_startswith( message, '/夸我','/kk', '/kw' ):  # from weilan
                fc.kk(message,uid,gid)
            elif true_startswith( message, '/小姐姐','/四次元', '/girl','/臭鳜鱼' ):  
                douyingirl.douyingirl(message,uid,gid)
            elif true_startswith( message, '/echo','/say', '/说' ): 
                echo.echo(message,uid,gid)
            elif true_startswith( message, '/pz','/碰撞' ): 
                pzjqr.pzjqr(message,uid,gid)
            elif true_startswith( message, '/-' ): 
                fother.other(message,uid,gid)
            else:
                other.other(message,uid,gid)


