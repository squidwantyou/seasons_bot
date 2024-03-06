#!/usr/bin/env python3
import analysis 
import requests
import json
import time
import os,sys

def backup_member(gid,):
    time_str = "%4d%02d%02d"%( time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday )

    # make dir
    if not os.path.isdir(f"auto_backup/{gid}"):
        os.system(f"mkdir -p auto_backup/{gid}")

    # backup  group member
    if os.path.isfile(f"auto_backup/{gid}/{time_str}.membmer.json"):
        pass
    else:
        url = 'http://0.0.0.0:5700/get_group_member_list'
        data = {'group_id':int(gid), 'no_cache':True } 
        res = requests.post( url=url, data=data )
        reply_msg = json.loads( res.content )
        with open(f"auto_backup/{gid}/{time_str}.membmer.json",'w') as ofp:
            ofp.write(str(reply_msg))
        pass

def backup_files(gid):
    time_str = "%4d%02d%02d"%( time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday )

    # backup files
    file_root = f"auto_backup/{gid}/files"
    if not os.path.isdir( file_root ):
        os.system(f"mkdir -p {file_root}")

    url = 'http://0.0.0.0:5700/get_group_root_files'
    data = {'group_id':int(gid) } 
    res = requests.post( url=url, data=data )
    reply_msg = json.loads( res.content )
    file_list = reply_msg['data']['files']
    dir_list = reply_msg['data']['folders']

    # load file_id_list
    if not os.path.isfile( f"{file_root}/../bot_file_id_list" ):
        os.system(f"touch {file_root}/../bot_file_id_list" )
    file_id_list = [ x.strip() for x in open( f"{file_root}/../bot_file_id_list" ).readlines() ]

    for f in file_list:
        print(f['file_id'])
        print(f['file_name'])
        print(f['busid'])
        print(f['uploader'])

        if f['file_id'] not in file_id_list:
            url = 'http://0.0.0.0:5700/get_group_file_url'
            data = {'group_id':int(gid),'file_id': f['file_id'], 'busid':f['busid'] } 
            res = requests.post( url=url, data=data )
            url = json.loads( res.content )['data']['url']

            response = requests.get(url)
            if response.status_code == 200:
                with open(f"{file_root}/{f['file_name']}", 'wb') as ofp:
                    ofp.write(response.content)
            if os.path.isfile( f"{file_root}/{f['file_name']}" ):
                file_id_list.append( f['file_id'] )
            else:
                sys.stderr.write("##### Download file failed.")

        else:
            pass

    with open(f"{file_root}/../bot_file_id_list",'w') as ofp: 
        for _ in file_id_list:
            ofp.write(f"{_}\n")

def backupall():
    time_str = ""
    time_str = "%4d%02d%02d"%( time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday )

    all_group = list()
    res =  analysis.get_group_list() 

    for tmp in res['data']:
        all_group.append( tmp['group_id'] )

    for gid in all_group:
        if gid == 144744787:
            backup_member(gid)
            backup_files(gid)


backupall()

