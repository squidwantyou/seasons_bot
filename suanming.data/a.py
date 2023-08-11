import sys,os
for line in open(sys.argv[1]):
    if len(line)!=2:
        print(line,end='')
