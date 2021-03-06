#coding:utf8
from firefly.server.globalobject import rootserviceHandle,GlobalObject
import time
from models.sysModel import MysqlObject,showDict
from models.gameMainModel import gameMatching,shufflingLicensing,sortPuke
@rootserviceHandle
def timerconnection_1000():
	print '*'*5,u'心跳定时服务器连接成功','*'*5
	time.sleep(1)
	removeHeart()

@rootserviceHandle
def timerconnection_999():
	print '*'*5,u'房间定时服务器连接成功','*'*5
	time.sleep(1)
	createroom()

@rootserviceHandle
def timerconnection_998():
	print '*'*5,u'抢地主定时服务器连接成功','*'*5
	time.sleep(1)
	seizeTimer()

@rootserviceHandle
def timerconnection_997():
	print '*'*5,u'游戏定时服务器连接成功','*'*5
	time.sleep(1)
	gameTimer()

def removeHeart():
	'''心跳定时器'''
	mysqlObj = MysqlObject()
	while True:
		time.sleep(10)
		nowTime = int(time.time())
		isTimeOut = mysqlObj.getAll('mn', 'select pid from mn_heart where heart_time<%s',[nowTime-60])
		if isTimeOut==False or len(isTimeOut)<1:
			continue
		else:
			for x in isTimeOut:
				GlobalObject().root.callChild('net','clearclient_200',x)

def createroom():
	'''创建房间定时器
	TODO:
	1.目前的房间创建是自动选择已经准备的用户，但是需要实现：（1）用户自定义房间，然后其他用户选择该房间，进入之后再开始抢地主
	2.将所有的数据库返回的list转化成dict
	'''
	mysqlObj = MysqlObject()
	room_type=[1,2,3,4]
	while True:
		isInGame = 0
		time.sleep(1)
		for x in room_type:
			userList = mysqlObj.getAll('mn', 'select pid from mn_gamequeue where room_type=%s',[x])
			if userList==False:
				continue
			isroom = gameMatching(list(userList))
			if isroom['status']!=1:
				continue
			#删除玩家的队列缓存
			pidList = isroom['matchList']
			#判断玩家是否在游戏中
			for y in pidList:
				isgame = mysqlObj.getOne('mn', 'select count(*) as a from mn_room where f_u=%s or s_u=%s or t_u=%s',[y['pid'],y['pid'],y['pid']])
				if isgame==False or isgame[0]<1:
					continue
				else:
					mysqlObj.delete('mn', 'delete from mn_gamequeue where pid =%s',[y['pid']])
					isInGame = 1
			if isInGame==1:
				continue
			mysqlObj.delete('mn', 'delete from mn_gamequeue where pid in (%s, %s, %s)',[pidList[0]['pid'],pidList[1]['pid'],pidList[2]['pid']])
			#创建牌组，并生成房间
			pukeList = shufflingLicensing()
			#写入数据库中
			roomUserList = []
			for y in pidList:
				roomUserList.append(y['pid'])
			room_id = mysqlObj.insertOne('mn', 'insert into mn_room (f_u,s_u,t_u,f_p,s_p,t_p,d_z,timer,timer_pid, multiple,puke_type,dz_user,spend,money_type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',\
				[roomUserList[0],roomUserList[1],roomUserList[2],','.join(pukeList[0]),','.join(pukeList[1]),','.join(pukeList[2]),','.join(pukeList[3]), int(time.time()),0, 1,0,str(roomUserList[0])+','+str(roomUserList[1])+','+str(roomUserList[2]), 1,x])	#写入房间完毕
			for y in range(0, len(pidList)):
				returnData = {}
				#向各玩家发牌
				returnData['s'] = 1 
				returnData['c'] = 1000 #指令号1000
				if y==0:
					returnData['f_p'] = pukeList[0]		#first	1 :如果当前用户是first用户，将first用户的牌直接给他。
				else:
					returnData['f_p'] = len(pukeList[0]) # 当前用户不是first用户，将first用户的牌的数量告诉他
				if y==1:
					returnData['s_p'] = pukeList[1]		#second	2
				else:
					returnData['s_p'] = len(pukeList[1])
				if y==2:
					returnData['t_p'] = pukeList[2]		#theard	3
				else:
					returnData['t_p'] = len(pukeList[2])
				returnData['d']	=len(pukeList[3])	#地主牌
				#读取用户数据

				#调用发牌异步方法
				GlobalObject().root.callChild('net','sendpuke_201',[pidList[y]['pid']],showDict(returnData))
			#初始化抢地主
			returnData = {'s':1, 'c':2000} #wtx:当收到2000信息时，告知用户可以抢地主了
			if 's5' in ','.join(pukeList[0]):
				nextUser = roomUserList[0] #wtx:如果该用户首先抢地主，那么更新timer_pid为当前用户（即该用户开启倒计时30s）
				returnData['p'] = 'f_u'
			elif 's5' in ','.join(pukeList[1]):
				nextUser = roomUserList[1]
				returnData['p'] = 's_u'
			elif 's5' in ','.join(pukeList[2]):
				nextUser = roomUserList[2]
				returnData['p'] = 't_u'
			else:
				nextUser = roomUserList[0]
				returnData['p'] = 'f_u'
			mysqlObj.update('mn', 'update mn_room set timer=%s,timer_pid=%s,spend=2 where room_id=%s', [int(time.time()),nextUser,room_id]) #更新房间状态：抢地主状态
			GlobalObject().root.callChild('net','dzpid_202',[roomUserList[0],roomUserList[1],roomUserList[2]],showDict(returnData))

def getNextUser(dz_user,timer_pid, room_id, u):
	'''处理下一个响应PID的用户'''
	print 'wtx qdzing??'
	mysqlObj = MysqlObject()
	#首先获取timer_pid的用户，并计算出dz_user数量然后进行轮回
	dz_user_l = dz_user
	dz_user = dz_user.split(',')
	u_num = len(dz_user)
	returnData = {'s':1, 'c':2000}
	if u_num==0:
		return
	else:
		for x in range(0,len(dz_user)):
			dz_user[x] = int(dz_user[x])
		dqwz = dz_user.index(timer_pid)
		nowweizhi = u.index(timer_pid)
		if nowweizhi==0:
			returnData['n_u'] = 'f_u'
		elif nowweizhi==1:
			returnData['n_u'] = 's_u'
		elif nowweizhi==2:
			returnData['n_u'] = 't_u'
		returnData['f'] = 0
		nextUser = dz_user[(dqwz+1) % u_num]
		del dz_user[dqwz]
		for x in range(0,len(dz_user)):
			dz_user[x] = str(dz_user[x])
		u_dz_user = ','.join(dz_user)
		if len(dz_user)>0:
			weizhi = u.index(nextUser)
			if weizhi==0:
				returnData['p'] = 'f_u'
			if weizhi==1:
				returnData['p'] = 's_u'
			if weizhi==2:
				returnData['p'] = 't_u'
		mysqlObj.update('mn', 'update mn_room set timer=%s,timer_pid=%s,dz_user=%s where room_id=%s', [int(time.time()),nextUser,u_dz_user,room_id])
		GlobalObject().root.callChild('net','dzpid_202',u,showDict(returnData))
		if len(dz_user)==0:
			#mysqlObj.update('mn', 'update mn_room set timer=%s,timer_pid=%s,dz_user=%s where room_id=%s', [int(time.time()),0,dz_user_l,room_id])
			#mysqlObj.update('mn', 'update mn_room set timer=%s where room_id=%s', [int(time.time()),room_id])
			GlobalObject().root.callChild('net','removegame_203',room_id)

def seizeTimer():
	'''抢地主倒计时'''
	mysqlObj = MysqlObject()
	while True:
		time.sleep(2)
		#业务逻辑思路是，查询数据库所有状态为2的房间，读出time值，然后根据PID来进行确定到底该谁抢地主
		roomList = mysqlObj.getAll('mn', 'select room_id,dz_user from mn_room where spend=2 and timer<%s',[int(time.time())-30])
		if roomList==False or roomList[0]=='':
			continue
		for x in roomList:
			if x['dz_user']=='':
				#全部放弃了
				continue
			else:
				roomInfo = mysqlObj.getOneDict('mn', 'select f_u,s_u,t_u,timer_pid,dz_pid from mn_room where room_id=%s', [int(x['room_id'])])
				if roomInfo==False or roomInfo['f_u']=='':
					continue
				if roomInfo['timer_pid']==roomInfo['dz_pid']:
					#轮到他自己抢地主，就开始进行游戏了，分发地主牌并响应地主的倒计时,由客户请求触发
					continue
				else:
					getNextUser(x['dz_user'], int(roomInfo['timer_pid']), x['room_id'],[int(roomInfo['f_u']),int(roomInfo['s_u']),int(roomInfo['t_u'])])
					continue

def gameTimer():
	'''游戏倒计时'''
	mysqlObj = MysqlObject()
	while True:
		time.sleep(2)
		#业务逻辑思路是，查询数据库所有状态为2的房间，读出time值，然后根据PID来进行确定到底该谁抢地主
		roomList = mysqlObj.getAll('mn', 'select room_id,timer_pid,now_pid from mn_room where spend=3 and timer<%s',[int(time.time())-30])
		print 'wtx roomList=',roomList,'type=',type(roomList)

		if roomList==False or roomList[0]=='': #getAll返回tuple
			continue
		for x in roomList:
			#x是dict:{'timer_pid': 1L, 'now_pid': 0L, 'room_id': 503L}
			if x['now_pid']!=None:
				now_pid=int(x['now_pid'])
			if x['now_pid']==None:
				GlobalObject().root.callChild('net','nextmustpuke_205',int(x['timer_pid']))
			else:
				if int(x['timer_pid'])==now_pid:
					#清空pid
					mysqlObj.update('mn','update mn_room set now_pid=null,puke_type=0,max_puke=null where room_id=%s',[x['room_id']])
					print '*'*5,11111,'*'*5
					GlobalObject().root.callChild('net','nextmustpuke_205',int(x['timer_pid']))
					continue
				GlobalObject().root.callChild('net','nextoutpuke_204',int(x['timer_pid']))
