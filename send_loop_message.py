#!/usr/bin/env python
import analysis
import sys
import time

uid = int(sys.argv[1])
gid = int(sys.argv[2])
delay = int(sys.argv[3])
ntime = int(sys.argv[4])
interval = int(sys.argv[5])
text = sys.argv[6] 

time.sleep(delay)

for i in range(int(ntime)-1) :
    analysis.send_msg( text, uid=uid,gid = gid )
    time.sleep(interval)

analysis.send_msg( text, uid=uid,gid = gid )




