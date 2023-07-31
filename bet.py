#!/usr/bin/env python3
import base64
import sys,os
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patches as mpatches
import matplotlib
import random as rd
import pickle
import numpy as np
from analysis import source_mysql,send_msg
import analysis

class Bet:
    def __init__(self):
        pass

def make_board(ax):
    return

def check_finished(gid):
    try:
        last_puzzle = fetch_last_puzzle(gid)
        if int(last_puzzle[2]) == 1:
            return True
        else:
            return False
    except:
        return True

def report_status(gid,i_d = None):
    return

def finish_puzzle(gid):
    return

def update_puzzle(gid,steps ,path,qq="0",i_d = None):
    return

def make_puzzle(gid, board = None):
    return

def fetch_last_puzzle(gid,i_d = None):
    return 

def statistics(uid,gid):
    return

def pzjqr( message, uid, gid ):
    path = ''
    try:
        path = " ".join(message.text.split()[1:])
    except:
        path = ''

    if path == '':    # no arguments, report 
        if check_finished(gid): # if finished
            path = 'new'
        else:
            report_status(gid)
            return
         
    if path == 'stop': # end current puzzle
        finish_puzzle(gid)
        analysis.send_msg(gid =gid, m ="Thank you for playing.")
        return 



