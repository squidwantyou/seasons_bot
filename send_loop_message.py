#!/usr/bin/env python
import analysis
import sys
import time

uid = int(sys.argv[1])
gid = int(sys.argv[2])
ntime = int(sys.argv[3])
interval = int(sys.argv[4])
text = sys.argv[5] 

for i in range(int(ntime)-1) :
    analysis.send_msg( text, uid=uid,gid = gid )
    time.sleep(interval)

analysis.send_msg( text, uid=uid,gid = gid )




