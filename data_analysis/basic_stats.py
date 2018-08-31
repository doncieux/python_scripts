#/usr/bin/python -w

import sys
from statistics import *

data=[]
for l in sys.stdin.readlines():
    data.append(float(l))
print("max min mean")
print(str(max(data))+" "+str(min(data))+" "+str(mean(data)))
