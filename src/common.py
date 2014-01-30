import sys
import random
import time
import operator
import glob
import os
import hashlib
sys.path.append('/usr/local/lib/python3.3/dist-packages/python_graph_core-1.8.2-py3.3.egg')
from pygraph.classes.digraph import digraph

random.seed(1001)

def strToMD5(mystr):
    return hashlib.md5(mystr.encode('utf-8')).hexdigest()

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap

def getRepLength(list):
    """How many times the first element occurs"""
    i = 1
    while i < len(list):
        if list[i] == list[0]: 
            i += 1
        else: break
    return i

def getRepFirst(list, i):
    """Where does the first element like list[i] occur in the sequence of repeated elements"""
    el = list[i]
    while i >= 0:
        if list[i] != el:
            break 
        i-=1
    return i + 1

#print (getRepLength([1,2,3,3,3, 4,5,6,6][6:])) 
INFINITY = 2**30