#coding:utf8
import sys,os
from firefly.server.globalobject import netserviceHandle,GlobalObject
from models.sysModel import showMsg
from models.userModel import addTest

@netserviceHandle
def reg_666(_conn,data): # wtx：666是自己定义的，临时用于注册测试用户的接口
	'''心跳请求接口'''
	addTest()
	return showMsg(1, '注册测试用户成功')