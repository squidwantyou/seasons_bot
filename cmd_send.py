#!/usr/bin/env python
import sys,os
import random as rd
import requests
import json
import analysis

gid = 528343595

m = " ".join(sys.argv[1:])
analysis.send_msg( m,uid=0,gid=gid, to_image=False)



