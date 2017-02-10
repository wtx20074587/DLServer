#coding:utf8
import sys,os
from firefly.server.globalobject import netserviceHandle,GlobalObject
from models.sysModel import showMsg
from models.userModel import setHeart,checkLogin
count = 0
@netserviceHandle
def heart_2(_conn,data):
	'''心跳请求接口'''
	isLogin = checkLogin(_conn.transport.sessionno)

	print "wtx isLogin=",isLogin

	if isLogin==False:
		return showMsg(-1, '您还未登录')

	else:
		print "wtx 用户已经登录了！开始心跳一次",++count

	setHeart(_conn.transport.sessionno)
	return showMsg(1, '')