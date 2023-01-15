#!/usr/bin/env python
import sys,os
import random as rd
import requests
import json

gid = 144744787

url = 'http://0.0.0.0:5700/get_msg'
data = {'message_id':-1776849735} 
# res = requests.post( url=url, data=data )
# print( json.loads( res.content ) )

m = sys.argv[1]
data = {'group_id': gid  , 'message':m} 
url = 'http://0.0.0.0:5700/send_group_msg'
requests.post( url=url, data=data )



