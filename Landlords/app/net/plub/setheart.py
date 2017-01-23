#coding:utf8
import sys,os
from firefly.server.globalobject import netserviceHandle,GlobalObject
from models.sysModel import showMsg
from models.userModel import setHeart,checkLogin

@netserviceHandle
def heart_2(_conn,data):
	'''心跳请求接口'''
	isLogin = checkLogin(_conn.transport.sessionno)
	if isLogin==False:
		return showMsg(-1, '您还未登录')
	setHeart(_conn.transport.sessionno)
	return showMsg(1, '')