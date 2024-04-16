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

def backup_files( gid, root = True, file_root = None, dir_name = None , folder_id = None ):
    time_str = "%4d%02d%02d"%( time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday )
    dir_list, file_list = None,None

    if root:
        file_root = f"auto_backup/{gid}/files"
        marker = str(gid)
    else:
        file_root = f"{file_root}/{dir_name}"
        marker = dir_name

    if not os.path.isdir( file_root ):
        os.system(f"mkdir -p {file_root}")

    if  root :
        url = 'http://0.0.0.0:5700/get_group_root_files'
        data = {'group_id':int(gid) } 
        res = requests.post( url=url, data=data )
        reply_msg = json.loads( res.content )
        file_list = reply_msg['data']['files']
        dir_list = reply_msg['data']['folders']
    else:
        url = 'http://0.0.0.0:5700/get_group_files_by_folder'
        data = { 'group_id':int(gid) ,'folder_id': folder_id } 
        res = requests.post( url=url, data=data )
        reply_msg = json.loads( res.content )
        file_list = reply_msg['data']['files']
        try:
            dir_list = reply_msg['data']['folders']
        except:
            dir_list = []

    # load file_id_list
    file_marker = f"{file_root}/../bot_file_id_list_{marker}" 
    if not os.path.isfile( file_marker ):
        os.system(f"touch {file_marker}" )
    file_id_list = [ x.strip() for x in open( file_marker ).readlines() ]

    for f in file_list:
        if f['file_id'] not in file_id_list:
            if f['file_size'] > 1024*1024*100 :
                print( f"Size too big: {file_root}/{f['file_name']}" )
                continue
            try:
                url = 'http://0.0.0.0:5700/get_group_file_url'
                data = {'group_id':int(gid),'file_id': f['file_id'], 'busid':f['busid'] } 
                res = requests.post( url=url, data=data )
                url = json.loads( res.content )['data']['url']

                response = requests.get(url)
                if response.status_code == 200:
                    with open(f"{file_root}/{f['file_name']}", 'wb') as ofp:
                        ofp.write(response.content)
                    print( f"Saved {file_root}/{f['file_name']}" )
            except:
                pass
            if os.path.isfile( f"{file_root}/{f['file_name']}" ):
                file_id_list.append( f['file_id'] )
            else:
                print(f"##### Download file failed. {f['file_name']}")

        else:
            pass

    with open(file_marker,'w') as ofp: 
        for _ in file_id_list:
            ofp.write(f"{_}\n")

    if dir_list:
        for d in dir_list:
            print(d)
            folder_id = d['folder_id']
            folder_name = d['folder_name']
            # remove space
            folder_name = "".join( folder_name.split() )
            backup_files(gid, root = False, file_root = file_root, dir_name = folder_name, folder_id = folder_id )

    # dir_list = reply_msg['data']['folders']
    # backup_files( gid, file_root = None, dir_name = None , folder_id = None )

def backupall():
    time_str = ""
    time_str = "%4d%02d%02d"%( time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday )

    all_group = list()
    res =  analysis.get_group_list() 

    for tmp in res['data']:
        all_group.append( tmp['group_id'] )

    for gid in all_group:
        if gid == 144744787:
            continue
            backup_member(gid)
            backup_files(gid)
        if gid == 528343595:
            continue
            backup_files(gid)
        if gid == 414927948:
            backup_member(gid)
            backup_files(gid)

backupall()


