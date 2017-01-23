#coding:utf8
import os,sys,time
main_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(main_root)
from models.userModel import *


print "脚本名：".decode('utf8').encode('gbk'), sys.argv[0]
for i in range(1, len(sys.argv)):
    print "参数".decode('utf8').encode('gbk'), i, sys.argv[i]
while 1:
	print 1
	time.sleep(1)
