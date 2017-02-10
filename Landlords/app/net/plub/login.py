#coding:utf8
import sys,os
from firefly.server.globalobject import netserviceHandle,GlobalObject
from models.sysModel import showMsg,jsonload
from models.userModel import userLogin,setHeart,loginCache,checkLogin,addTest

import random,json
from models.gameMainModel import shufflingLicensing

WTXDEBUG = "WANG TIANXIAO IS DEBUGING"

@netserviceHandle
def login_1(_conn,data):
	isLogin = checkLogin(_conn.transport.sessionno)
	try:
		data = jsonload(data)

		if data[0]!=1:
			return showMsg(-1, '请求非法001')
		else:
			if data[1][0]<1 or data[1][1]=='' or data[1][2]=='': #分别对应了数据库中的：id，用户名，用户的密码。
				return showMsg(-1, '账号数据错误')
			returnData = userLogin({'user_id':data[1][0],'user_name':data[1][1],'user_key':data[1][2]})
			if returnData['status']!=1:
				return showMsg(returnData['status'], returnData['msg'])
			cache = loginCache(_conn.transport.sessionno, data[1][0], data[1][1]) #写入Cache中
			if cache==False:
				return showMsg(-1, '您已经登录，请先下线')
			setHeart(_conn.transport.sessionno)	#更新心跳 #wtx:疑问？：心跳更新的参数是什么类型？？
			return showMsg(returnData['status'], returnData['msg'])
	except Exception, e:
		return showMsg(-1, '请求非法002')
print '='*5,u'登录服务器已启动','='*5


'''@netserviceHandle
def moni_4(_conn,data):
	isLogin = checkLogin(_conn.transport.sessionno)
	if isLogin==False:
		return showMsg(-1, '您还未登录')
	#初始化随机
	randNum = random.randint(0,2)
	#初始化牌组
	pukeList = shufflingLicensing()
	returnData = {}
	returnData['c'] = 1000 #指令号1000
	returnData['p'] = pukeList[0]	#用户扑克
	returnData['l_1'] = len(pukeList[1])	#上家扑克数量
	returnData['l_2'] = len(pukeList[2])	#下家扑克数量
	returnData['d']	=pukeList[3]	#地主牌
	return json.dumps(returnData)'''