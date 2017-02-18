#coding:utf8
import sys,os,time,json,re,random
from firefly.server.globalobject import netserviceHandle,GlobalObject
from models.sysModel import showMsg,jsonload, MemcacheEx,showDict
from models.userModel import checkLogin,joinQueue,outQueue,getUserInfo,QDZ,unQDZ,showPuke,unOutPuke
from models.gameMainModel import pukeData

@netserviceHandle
def console_3(_conn,data):
	'''工作控制台，所有任务从这里分发'''
	_sessionno = _conn.transport.sessionno
	isLogin = checkLogin(_sessionno)
	if isLogin==False:
		return showMsg(-1, '您还未登录')
	#try:


	print 'before, type=',type(data)
	data = jsonload(data) #部分数据可能会导致json转换不通过
	print 'after, type=',type(data),'data=',data

	if data[0]!=2: #wtx:因此，客户端定义的DEAL=4，不是合法操作。可以删除。
		return showMsg(-1, '请求非法')
	else:
		if data[1][0]==1:
			#抢地主
			isOK = QDZ(_sessionno,int(data[1][1]))
			if isOK['s']==1:
				return showMsg(1, '')
			else:
				if isOK['s']==-1:
					return showDict({'s':-1, 'm':isOK['m'],'c':2005}) #wtx:只有抢地主错误，才会返回带m的信息
				else:
					return showDict({'s':-1, 'm':isOK['m'],'c':2006})
		elif data[1][0]==2:
			#不抢地主
			isOK = unQDZ(_sessionno)
			if isOK['s']==1:
				return showMsg(1, '')
			else:
				return showDict({'s':-1, 'm':isOK['m'],'c':2007})
		elif data[1][0]==3:
			#出牌
			isOK = showPuke(_sessionno, data[1][1],pukeData)
			if isOK['s']==1:
				return showMsg(1, '')
			else:
				if isOK['s']==-1:
					return showDict({'s':-1, 'm':isOK['m'],'c':2008})
				else:
					return showDict({'s':-1, 'm':isOK['m'],'c':2009})
		elif data[1][0]==4:
			#不出
			isOK = unOutPuke(_sessionno)
			if isOK['s']==1:
				return showMsg(1, '')
			else:
				if isOK['s']==-1:
					return showDict({'s':-1, 'm':isOK['m'],'c':2014})
				elif isOK['s']==-2:
					return showDict({'s':-1, 'm':isOK['m'],'c':2015})
				elif isOK['s']==-3:
					return showDict({'s':-1, 'm':isOK['m'],'c':2016})
				elif isOK['s']==-4:
					return showDict({'s':-1, 'm':isOK['m'],'c':2017})
		elif data[1][0]==5:
			#加入游戏队列
			if int(data[1][1]) not in [1,2,3,4]:#5种房间类型
				return showMsg(-1, '房间错误，请刷新浏览器')
			isJoin = joinQueue(_sessionno,data[1][1])
			print 'WTX isJoin=',isJoin
			if isJoin['s']==-1:
				return showMsg(isJoin['s'], isJoin['m'])
			else:
				return showDict({'s':1,'c':1001})
		elif data[1][0]==6:
			#取用户信息
			isGet = getUserInfo(_sessionno)
			if isGet['s']!=1:
				return showMsg(isGet['s'], isGet['m'])
			else:
				return showDict({'s':1,'c':1001,'d':isGet['data']})
		elif data[1][0]==7:
			#离开游戏队列
			isLeaveQueue = outQueue(_sessionno)
			if isLeaveQueue==True:
				return showDict({'s':1,'c':1002})	#flash操作号1002，flash返回大厅
			else:
				return showMsg(-1, '您不在队列中')
	'''except Exception, e:
		print Exception,e
		return showMsg(-1, '请求非法')'''
	return showMsg(1, '')

