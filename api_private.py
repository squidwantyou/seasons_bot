import requests
import analysis 
import groupgame

def keyword(message,uid,gid = None):
    message = Message(message)
    groupgame.forprivate(message,uid)

