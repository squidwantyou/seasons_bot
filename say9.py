#!/usr/bin/env python
import requests
import json
import re
import analysis
import sys,os

def say9(message,uid=0,gid=0):
    print(">>>>> Called say9")
    try:
        items = message.text.split()
        text = message.text.lstrip( items[0] ).lstrip().strip()
        with open("tmpsay9.txt",'w') as ofp:
            ofp.write(text)
        os.system('convert data/images/qln2.png -gravity north  -stroke "#666C" -strokewidth 2 -fill "#333333" -font \
                    "./fonts/unifont-15.0.01.ttf" -pointsize 50 -annotate +0+530 @tmpsay9.txt   data/images/qln_out.png' )

        m = f'[CQ:image,file=qln_out.png]'
        analysis.send_msg(m,uid=uid,gid=gid)

    except Exception as e:
        print(e)
        analysis.send_msg("啊，那个，有点故障...",uid=uid,gid=gid)

