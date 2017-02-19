#coding:utf8
import multiprocessing

def hello():
    print "num_cpu=",str(multiprocessing.cpu_count())

hello()