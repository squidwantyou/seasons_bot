import requests
import function as fc
from analysis import *
from guess_number_2 import guess_number
import guess_number_five 
import guess_number_six 
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
import cat
import dog
import say9
import gstone
import world
import douyinboy
import anwei
import xqs
import tiangou
import kouchou
import wu
import history 
import bf
import suanming
import suijilaopo
import suijilaogong
import hougong
import dianzan
import minesweeper_battle
import random_say
import neutreeko
import xp
import today
import nazo

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
            elif true_startswith( message, '/6a2b' ): 
                guess_number_six.guess_number(message,uid,gid)
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
            elif true_startswith( message, '/求安慰','/anwei','/安慰'):  # from weilan
                anwei.anwei(message,uid,gid)
            elif true_startswith( message, '/小姐姐','/四次元', '/girl','/臭鳜鱼'  ):  
                douyingirl.douyingirl(message,uid,gid)
            elif true_startswith( message, '/小哥哥','/boy','/烤鱼'):  
                douyinboy.douyinboy(message,uid,gid)
            elif true_startswith( message, '/猫猫','/cat', '/miao','/喵' ):  
                cat.cat(message,uid,gid)
            elif true_startswith( message, '/dog' ):  
                dog.dog(message,uid,gid)
            elif true_startswith( message, '/echo','/say', '/说' ): 
                echo.echo(message,uid,gid)
            elif true_startswith( message, '/9say' ): 
                say9.say9(message,uid,gid)
            elif true_startswith( message, '/xqs','/kfc','/KFC','/星期四' ): 
                xqs.xqs(message,uid,gid)
            elif true_startswith( message, '/pz','/碰撞' ): 
                pzjqr.pzjqr(message,uid,gid)
            elif true_startswith( message, '/gstone'): 
                gstone.gstone(message,uid,gid)
            elif true_startswith( message, '/tiangou','/舔狗'): 
                tiangou.tiangou(message,uid,gid)
            elif true_startswith( message, '/world'): 
                world.world(message,uid,gid)
            elif true_startswith( message, '/口臭','/口吐莲花','/芬芳','/nmsl'): 
                kouchou.kouchou(message,uid,gid)
            elif true_startswith( message, '/wu','/污'): 
                wu.wu(message,uid,gid)
            elif true_startswith( message, '/history','/历史今天'): 
                history.history(message,uid,gid)
            elif true_startswith( message, '/today','/今天','/yesterday'): 
                today.today(message,uid,gid)
            elif true_startswith( message, '/算命','/sm','/运势','/yunshi','/ys','/jrrp' ): 
                suanming.suanming(message,uid,gid)
            elif true_startswith( message, '/bf' ): 
                bf.bf(message,uid,gid)
            elif true_startswith( message, '/suijilaopo','/sjlp','/随机老婆' ,'/老婆','/lp'): 
                suijilaopo.suijilaopo(message,uid,gid)
            elif true_startswith( message, '/suijilaogong','/sjlg','/随机老公' ,'/老公'): 
                suijilaogong.suijilaogong(message,uid,gid)
            elif true_startswith( message, '/后宫', '/hougong','/hg' ): 
                hougong.hougong(message,uid,gid)
            elif true_startswith( message, '/dianzan', '/点赞' ): 
                dianzan.dianzan(message,uid,gid)
            elif true_startswith( message, '/mwb','/msb', '/扫雷','/猫尾巴' ): 
                minesweeper_battle.mwb(message,uid,gid)
            elif true_startswith( message, '/rds','/随机说'): 
                random_say.rds(message,uid,gid)
            elif true_startswith( message, '/ntk','/neutreeko','/三连棋'): 
                neutreeko.ntk(message,uid,gid)
            elif true_startswith( message, '/nazo'): 
                nazo.nazo(message,uid,gid)
            elif true_startswith( message, '/xp','/XP'): 
                xp.xp(message,uid,gid)
            elif true_startswith( message, '/-' ): 
                fother.other(message,uid,gid)
            else:
                other.other(message,uid,gid)


