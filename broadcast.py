#!/usr/bin/env python
import sys,os
import requests
import random as rd
import json
import analysis
import time

def send_fake_group_message(m,uid=0,gid=0):
    analysis.send_msg( m,uid=uid,gid=gid)

def broadcast_all( m ):
    all_group = list()
    res =  analysis.get_group_list() 
    
    for tmp in res['data']:
        all_group.append( tmp['group_id'] )

    for gid in all_group:
        if gid == 144744787:
            continue
        send_fake_group_message( m, gid = gid )
        time.sleep( 5 + rd.randrange(10) )


if __name__ == "__main__":
    assert len(sys.argv) > 1
    #cmd = " ".join(sys.argv[1:] )
    #broadcast_all(cmd)


