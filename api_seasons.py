import requests
import function as fc
from analysis import *

def conduct(message,uid,gid = None):
    message = Message(message)
    for cq in message.cqs:
        if cq.type == 'forward':
            pass

