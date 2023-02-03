#!/usr/bin/env python
import analysis
import sys
import time

uid = int(sys.argv[1])
gid = int(sys.argv[2])
waittime = int(sys.argv[3])
text = sys.argv[4] 

time.sleep(waittime)

analysis.send_msg( text, uid=uid,gid = gid )



