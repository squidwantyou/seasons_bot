import analysis 
import sys,os

NAZO_DIR = 'nazo_1'
# 1 下一关的钥匙是"触手", 回复/nazo 触手前进吧!    触手
# 2 钥匙是带嘤的触手  tentacle
# 3 钥匙是钥匙的钥匙  defined-tentacle
# 4 将触手彻底分解为几部分, 最大的一块好像可以当作钥匙     887143
# 5 VGhlIGtleSBpcyBlbmNvZGVkIGFzIFkzbGlaWEl0ZEdWdWRHRmpiR1U9IA==   cyber-tentacle
# 6 Lrf, gurfr jbeqf jrer rapbqrq ol EBG13. Pbatengf, gur xrl vf ebg13gragnpyr.   rot13tentacle
# 7 触手nazo是一场苦修, 在每一层都不得不南冲北撞, 东奔西走, 而终极的答案在第114514层, 救赎之道,就在其中    红茶
# 8 福尔摩斯先生,我们已经来到第8层了. 但令人疑惑的是, 这里好像完全没有什么东西能够成为....线索.  不得不承认, 的确如此, 这真是令人感到沮丧,  在没有得到任何证据的情况下是不能进行推理的，那样的话，只能是误入歧途. 哦不, 等等,华生医生,你领子上的是什么? 天啊,这真是太不可思议了!   DetectiveTentacle
# 9 你是说..马来西亚航空370号班机空难?! 没错, 就是那个下落不明的飞行铁块. 没有人知道那个事件的真相...除了我, 2014年3月8日,哥打巴鲁上空, 云层中伸出了一只巨大的触手..像抓起一只塑料玩具一样, 轻易的就把那架可怜的小飞机虏进了云中. 等等, 这太夸张了, 你是说, 这本书上说的都是真的? 没错, 也只相信了, 也就是说, 那个塑料飞机十年后会回到我们的世界, 带着......启示......   10tentacles  future number  ( use /today )
# 10 触手在次元的间隙里 等你 THANKYOU

def nazo(message,uid,gid):
    try:
        keymap = dict()
        keymap['触手'] = 2
        keymap['tentacle'] = 3
        keymap['defined-tentacle'] = 4
        keymap['887143'] = 5
        keymap['cyber-tentacle'] = 6
        keymap['rot13tentacle'] = 7
        keymap['红茶'] = 8
        keymap['DetectiveTentacle'] = 9
        keymap['10tentacles'] = 10
        keymap['THANKYOU'] = 10.5

        items = message.text.split()
        if len(items) == 1:
            m = f"[CQ:image,file={NAZO_DIR}/1.png]"
            analysis.send_msg(m,uid=uid,gid=gid)
        elif items[1] in keymap:
            m = f"[CQ:image,file={NAZO_DIR}/{keymap[items[1]]}.png]"
            analysis.send_msg(m,uid=uid,gid=gid)
        else:
            m = f"[CQ:image,file={NAZO_DIR}/incorrect.png]"
            analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        sys.stdout.flush()
        analysis.send_msg(gid=gid,m=f'NAZO ERROR')

