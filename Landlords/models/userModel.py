# -*- coding: utf8 -*-
from sysModel import MysqlObject,MemcacheEx,__version__,getConfig,showDict					#引入mysql, memcache, 系统模块版本号
from firefly.server.globalobject import GlobalObject
import random,hashlib,time,datetime
from gameMainModel import shufflingLicensing,checkPukeType,sortPuke,pukeData
import threading
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

WTX_DEBUG = True

memcache = MemcacheEx('server_1')
'''heartList = memcache.get('heartList')				#心跳的字典 格式{PID:心跳应答的时间}
if heartList==None:
	heartList = {}'''


def initCache():
	mysqlObj = MysqlObject()
	'''初始化缓存 后期用redis优化
	wtx:1.第一次初始化时会清空所有数据？
	'''
	mysqlObj.delete('lo','delete from lo_logincache')
	mysqlObj.delete('mn','delete from mn_heart')
	mysqlObj.delete('mn','delete from mn_gamequeue')
	mysqlObj.delete('mn','delete from mn_room')

def getNextUser(dz_user,timer_pid, room_id, u, nowUser, fen):
	'''处理下一个响应PID的用户'''

	mysqlObj = MysqlObject()
	#首先获取timer_pid的用户，并计算出dz_user数量然后进行轮回
	dz_user = dz_user.split(',')
	u_num = len(dz_user)
	returnData = {'s':1, 'c':2000,'n_u':nowUser,'f':fen}
	if u_num==1:
		return
	else:
		str_timer_pid = str(timer_pid)
		dqwz = dz_user.index(str_timer_pid)
		nextUser = dz_user[(dqwz+1) % u_num]
		nextUser = int(nextUser)
		weizhi = u.index(nextUser)
		if weizhi==0:
			returnData['p'] = 'f_u'
		if weizhi==1:
			returnData['p'] = 's_u'
		if weizhi==2:
			returnData['p'] = 't_u'
		mysqlObj.update('mn', 'update mn_room set timer=%s,timer_pid=%s where room_id=%s', [int(time.time()),nextUser,room_id])
		print 'GET NEXT USER,returnData=',returnData
		GlobalObject().netfactory.pushObject(3,showDict(returnData),u)

def QDZ(pid,fen):
	'''抢地主方法'''
	mysqlObj = MysqlObject()
	if fen<1 or fen>3:
		return {'s':-1,'m':'分数数错误'}

	isInGame = mysqlObj.getOneDict('mn','select room_id,dizhu_pid,timer_pid,multiple,dz_user,f_u,s_u,t_u from mn_room where f_u=%s or s_u=%s or t_u=%s', [pid,pid,pid])

	if isInGame==False or isInGame['multiple']>=6 or isInGame['timer_pid']!=pid or isInGame['dizhu_pid']==pid or str(pid) not in isInGame['dz_user']:
		return {'s':-1,'m':'不该您抢地主'}
	else:
		if isInGame['multiple']==2:
			if fen<2:
				return {'s':-2,'m':'不能低于2分'}
		if isInGame['multiple']==4:
			if fen<3:
				return {'s':-2,'m':'不能低于3分'}
		multiple = 2*fen
		#修改数据库
		mysqlObj.update('mn', 'update mn_room set multiple=%s,dizhu_pid=%s,timer=%s where room_id=%s', [multiple, pid,int(time.time()),isInGame['room_id']])
		#如果倍数不等于6，就开始下一个用户判断否则直接发送开始游戏信息
		u = [int(isInGame['f_u']),int(isInGame['s_u']),int(isInGame['t_u'])]
		weizhi = u.index(pid)
		if weizhi==0:
			nowUser = 'f_u'
		if weizhi==1:
			nowUser = 's_u'
		if weizhi==2:
			nowUser = 't_u'
		if multiple!=6:
			getNextUser(isInGame['dz_user'], isInGame['timer_pid'], isInGame['room_id'], u, nowUser, fen)
		else:
			beginGame(isInGame['room_id'])
			#直接开始游戏啦
			'''returnData = {'s':1, 'c':2000}
			if u.index(pid)==0:
				returnData['p'] = 'f_u'
			elif u.index(pid)==1:
				returnData['p'] = 's_u'
			elif u.index(pid)==2:
				returnData['p'] = 't_u'
			GlobalObject().netfactory.pushObject(3,showDict(returnData),u)'''
		return {'s':1}

def beginGame(room_id):

	print 'WTX BEGIN GAME =',room_id

	mysqlObj = MysqlObject()
	isInGame = mysqlObj.getOneDict('mn','select room_id,d_z,dizhu_pid,f_u,s_u,t_u,f_p,s_p,t_p from mn_room where room_id=%s and spend=2', [room_id])

	if isInGame==False or isInGame['room_id']<1:
		return False
	#读取地主牌
	d_z = isInGame['d_z'].split(',')
	u = [int(isInGame['f_u']),int(isInGame['s_u']),int(isInGame['t_u'])]
	if u.index(isInGame['dizhu_pid'])==0:
		f_p = isInGame['f_p']+','+isInGame['d_z']
		returnData = {'s':1, 'c':2002, 'd_z':isInGame['d_z'].split(','),'dz_u':'f_u'}
		GlobalObject().netfactory.pushObject(3,showDict({'s':1,'c':2003,'p':f_p.split(',')}),[isInGame['dizhu_pid']])
		mysqlObj.update('mn', 'update mn_room set f_p=%s,timer=%s,timer_pid=%s,dz_pid=%s,spend=3 where room_id=%s', [f_p, int(time.time()),isInGame['dizhu_pid'],isInGame['dizhu_pid'],room_id])
	elif u.index(isInGame['dizhu_pid'])==1:
		s_p = isInGame['s_p']+','+isInGame['d_z']
		returnData = {'s':1, 'c':2002, 'd_z':isInGame['d_z'].split(','),'dz_u':'s_u'}
		GlobalObject().netfactory.pushObject(3,showDict({'s':1,'c':2003,'p':s_p.split(',')}),[isInGame['dizhu_pid']])
		mysqlObj.update('mn', 'update mn_room set s_p=%s,timer=%s,timer_pid=%s,dz_pid=%s,spend=3 where room_id=%s', [s_p, int(time.time()),isInGame['dizhu_pid'],isInGame['dizhu_pid'],room_id])
	elif u.index(isInGame['dizhu_pid'])==2:
		t_p = isInGame['t_p']+','+isInGame['d_z']
		returnData = {'s':1, 'c':2002, 'd_z':isInGame['d_z'].split(','),'dz_u':'t_u'}
		GlobalObject().netfactory.pushObject(3,showDict({'s':1,'c':2003,'p':t_p.split(',')}),[isInGame['dizhu_pid']])
		mysqlObj.update('mn', 'update mn_room set t_p=%s,timer=%s,timer_pid=%s,dz_pid=%s,spend=3 where room_id=%s', [t_p, int(time.time()),isInGame['dizhu_pid'],isInGame['dizhu_pid'],room_id])
	#分别向客户端发送地主牌数据以及新的牌长度,先单独发更新牌的数据
	print 'WTX BEGIN GAME returnData =',returnData
	GlobalObject().netfactory.pushObject(3,showDict(returnData),u)

def removeGame(room_id):
	'''重新发牌'''	
	mysqlObj = MysqlObject()
	isInGame = mysqlObj.getOneDict('mn','select room_id,dizhu_pid,timer_pid,multiple,dz_user,f_u,s_u,t_u from mn_room where room_id=%s', [room_id])

	#if(type(isInGame)=='dict'): #deleted by wtx 20170215
		#isInGame = isInGame.values() #deleted by wtx 20170215

	u = [int(isInGame['f_u']), int(isInGame['s_u']),int(isInGame['t_u'])]
	pukeList = shufflingLicensing()
	#发送信息
	#得到timer_pid
	returnData = {'s':1, 'c':2000}
	if 's5' in pukeList[0]:
		timer_pid = isInGame['f_u']
		returnData['p'] = 'f_u'
	elif 's5' in pukeList[1]:
		timer_pid = isInGame['s_u']
		returnData['p'] = 's_u'
	elif 's5' in pukeList[2]:
		timer_pid = isInGame['t_u']
		returnData['p'] = 't_u'
	else:
		timer_pid = isInGame['f_u']
		returnData['p'] = 't_u'
	dz_user = str(isInGame['f_u'])+','+str(isInGame['s_u'])+','+str(isInGame['t_u'])
	mysqlObj.update('mn', 'update mn_room set f_p=%s,s_p=%s,t_p=%s,d_z=%s,timer=%s,timer_pid=%s, dz_user=%s where room_id=%s',[','.join(pukeList[0]), ','.join(pukeList[1]),','.join(pukeList[2]),','.join(pukeList[3]), int(time.time()),timer_pid,dz_user,room_id])
	removePuke_1 = {'s':1, 'c':2001, 'f_p':pukeList[0],'s_p':17,'t_p':17,'d_z':3}#重新发牌
	removePuke_2 = {'s':1, 'c':2001, 'f_p':17,'s_p':pukeList[1],'t_p':17,'d_z':3}#重新发牌
	removePuke_3 = {'s':1, 'c':2001, 'f_p':17,'s_p':17,'t_p':pukeList[2],'d_z':3}#重新发牌
	GlobalObject().netfactory.pushObject(3,showDict(removePuke_1),[u[0]])
	GlobalObject().netfactory.pushObject(3,showDict(removePuke_2),[u[1]])
	GlobalObject().netfactory.pushObject(3,showDict(removePuke_3),[u[2]])
	#分别发timer数据
	GlobalObject().netfactory.pushObject(3,showDict(returnData),u)
def unQDZ(pid):
	'''不抢地主'''
	mysqlObj = MysqlObject()
	isInGame = mysqlObj.getOneDict('mn','select room_id,dizhu_pid,timer_pid,multiple,dz_user,f_u,s_u,t_u from mn_room where f_u=%s or s_u=%s or t_u=%s and spend=2', [pid,pid,pid])
	if isInGame==False or isInGame['timer_pid']!=pid or isInGame['dizhu_pid']==pid or str(pid) not in isInGame['dz_user']:
		return {'s':-1,'m':'不该您抢地主'}
	#判断三种情况，一种是，都不抢，一种是只剩下一个人了，一种是大于1
	dz_user = isInGame['dz_user'].split(',')
	for x in range(0,len(dz_user)):
		dz_user[x] = int(dz_user[x])
	dz_key = dz_user.index(pid)
	dz_user.remove(dz_user[dz_key])
	num = len(dz_user)
	for x in range(0,len(dz_user)):
		dz_user[x] = str(dz_user[x])
	u_dz_user = ','.join(dz_user)
	mysqlObj.update('mn', 'update mn_room set timer=%s, dz_user=%s where room_id=%s',[int(time.time()),u_dz_user,isInGame['room_id']])
	u = [int(isInGame['f_u']), int(isInGame['s_u']),int(isInGame['t_u'])]
	weizhi = u.index(pid)
	if weizhi==0:
		nowUser = 'f_u'
	if weizhi==1:
		nowUser = 's_u'
	if weizhi==2:
		nowUser = 't_u'
	GlobalObject().netfactory.pushObject(3,showDict({'s':1, 'c':2004,'n_u':nowUser}),u)#不抢地主数据
	if num==0:
		removeGame(isInGame['room_id'])
	elif num==1 and isInGame['dizhu_pid']!=None and isInGame['dizhu_pid']!='':
		#直接开始游戏啦
		beginGame(isInGame['room_id'])
	else:
		#getNextUser(dz_user,timer_pid, room_id, u, nowUser, fen):
		getNextUser(isInGame['dz_user'], isInGame['timer_pid'], isInGame['room_id'], u,nowUser,0)
	return {'s':1}


def countValue(pukeList):
	'''取重复值'''
	if type(pukeList)!=type([]) or len(pukeList)<1:
		return False
	cf,nf,pd = [],[],{}
	for x in pukeList:
		cf.append(pukeData[x])
	nf = sorted(cf)
	for x in nf:
		pd[x] = cf.count(x)
	sortP = sorted(pd.items(), key=lambda d:d[0])
	return sortP

def game_settle(room_id, u, leavepid=0):
	loserPidList,winnerPidList = [],[]
	mysqlObj = MysqlObject()
	data = mysqlObj.getOne('mn', 'select f_p,s_p,t_p,dz_pid,money_type,multiple,f_u,s_u,t_u from mn_room where room_id=%s', [room_id])
	if data==False:
		return {'s':-3,'m':'该游戏已结束'}
	#得到底价
	dj = int(data[4])
	if dj==1:
		d_money = 1
	elif dj==2:
		d_money = 2
	elif dj==3:
		d_money = 5
	else:
		d_money = 10

	loseMoney = int(data[5]) * d_money#输的money
	ct = 0
	hasPuke_1 = len(data[0].split(','))
	hasPuke_2 = len(data[1].split(','))
	hasPuke_3 = len(data[2].split(','))
	if hasPuke_1==17 and data[6]!=data[3]:
		ct +=1
	if hasPuke_2==17 and data[7]!=data[3]:
		ct +=1
	if hasPuke_3==17 and data[8]!=data[3]:
		ct +=1
	if ct>=2:
		loseMoney = loseMoney*2
	ymd = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	winner,userList,loser = [],[],[]
	#判断是否leavepid为空
	if leavepid==0:
		#正常结束，先判断是那个牌出完了
		if data[0]=='':
			userindex = 0
		elif data[1]=='':
			userindex = 1
		elif data[2]=='':
			userindex = 2
		else:
			return {'s':-3,'m':'该游戏未结束'}
		#获取胜利者PID
		winnerPid = u[userindex]
		#判断是不是地主
		if winnerPid==int(data[3]):
			#地主获胜了,农民输
			#先赔钱，再删除数据库，发送结束游戏指令
			winnerPidList = [u[userindex]]
			loserPidList = u[:]
			loserPidList.remove(loserPidList[userindex])
			#del loserPidList[userindex]
			winMoney = loseMoney*2
			losMoney = loseMoney
		else:
			#农民获胜了，地主输
			winnerPidList = u[:]
			winnerPidList.remove(int(data[3]))
			loserPidList = [int(data[3])]
			winMoney = loseMoney
			losMoney = loseMoney*2
		for x in winnerPidList:
			#获得user_id
			winner_userid = mysqlObj.getOne('lo', 'select user_id from lo_logincache where pid=%s',[x])
			winner.append(winner_userid[0])
			userList.append(winner_userid[0])
			#获得用户money
			winnerMoney = mysqlObj.getOne('ssc', 'select money from mn_user where user_id=%s',[winner_userid[0]])
			#写入log日志
			mysqlObj.insertOne('lo', 'insert into lo_rfloat (user_id,r_status,action_type,money,after_money,add_time,add_ymd,note) values (%s,%s,%s,%s,%s,%s,%s,%s)', [winner_userid[0], 1,4,winMoney,winnerMoney[0],int(time.time()),ymd,('斗地主获胜获得奖金'+str(winMoney)+'元').encode('utf-8') ])
			mysqlObj.commit('lo')
			#修改用户金钱
			mysqlObj.update('ssc', 'update mn_user set money=money+%s where user_id=%s',[winMoney,winner_userid[0]])
			mysqlObj.commit('ssc')
		for x in loserPidList:
			loser_userid = mysqlObj.getOne('lo', 'select user_id from lo_logincache where pid=%s',[x])
			loser.append(loser_userid[0])
			userList.append(loser_userid[0])
			#获得用户money
			loserMoney = mysqlObj.getOne('ssc', 'select money from mn_user where user_id=%s',[loser_userid[0]])
			#写入log日志
			mysqlObj.insertOne('lo', 'insert into lo_rfloat (user_id,r_status,action_type,money,after_money,add_time,add_ymd,note) values (%s,%s,%s,%s,%s,%s,%s,%s)', [loser_userid[0], 2,3,losMoney,loserMoney[0],int(time.time()),ymd,('斗地主输掉了'+str(losMoney)+'元奖金').encode('utf-8') ])
			mysqlObj.commit('lo')
			#修改用户金钱
			mysqlObj.update('ssc', 'update mn_user set money=money-%s where user_id=%s',[losMoney,loser_userid[0]])
			mysqlObj.commit('ssc')
		#写入游戏记录表
		gamer_list = ','.join(str(i) for i in userList)
		winner = ','.join(str(i) for i in winner)
		loser = ','.join(str(i) for i in loser)
		winnerID = ','.join(str(i) for i in winnerPidList)
		loserID = ','.join(str(i) for i in loserPidList)
		multiple = int(data[5])
		upset = d_money
		mysqlObj.insertOne('lo', 'insert into lo_gamelog (gamer_list,winner,loser,multiple,upset,add_time,add_ymd) values (%s,%s,%s,%s,%s,%s,%s)',[gamer_list,winner,loser,multiple,upset,int(time.time()),ymd])
	else:
		#判断是不是地主
		if data[3]==None:
			dz_pid = leavepid
		else:
			dz_pid = int(data[3])
		print u'退出的地主PID：',dz_pid
		if leavepid==dz_pid:
			print u'dizhu '
			#是地主,赔两家
			winnerPidList = u[:]
			winnerPidList.remove(int(leavepid))
			loserPidList = [int(leavepid)]
			winMoney = loseMoney
			losMoney = loseMoney*2
			for x in winnerPidList:
				#获得user_id
				winner_userid = mysqlObj.getOne('lo', 'select user_id from lo_logincache where pid=%s',[x])
				if winner_userid!=False:
					winner.append(winner_userid[0])
					userList.append(winner_userid[0])
					#获得用户money
					winnerMoney = mysqlObj.getOne('ssc', 'select money from mn_user where user_id=%s',[winner_userid[0]])
					#写入log日志
					mysqlObj.insertOne('lo', 'insert into lo_rfloat (user_id,r_status,action_type,money,after_money,add_time,add_ymd,note) values (%s,%s,%s,%s,%s,%s,%s,%s)', [winner_userid[0], 1,4,winMoney,winnerMoney[0],int(time.time()),ymd,('斗地主获胜获得奖金'+str(winMoney)+'元').encode('utf-8')])
					mysqlObj.commit('lo')
					#修改用户金钱
					mysqlObj.update('ssc', 'update mn_user set money=money+%s where user_id=%s',[winMoney,winner_userid[0]])
					mysqlObj.commit('ssc')
			for x in loserPidList:
				loser_userid = mysqlObj.getOne('lo', 'select user_id from lo_logincache where pid=%s',[x])
				if loser_userid!=False:
					loser.append(loser_userid[0])
					userList.append(loser_userid[0])
					#获得用户money
					loserMoney = mysqlObj.getOne('ssc', 'select money from mn_user where user_id=%s',[loser_userid[0]])
					#写入log日志
					mysqlObj.insertOne('lo', 'insert into lo_rfloat (user_id,r_status,action_type,money,after_money,add_time,add_ymd,note) values (%s,%s,%s,%s,%s,%s,%s,%s)', [loser_userid[0], 2,3,losMoney,loserMoney[0],int(time.time()),ymd,('斗地主逃跑输掉了'+str(losMoney)+'元奖金').encode('utf-8') ])
					mysqlObj.commit('lo')
					#修改用户金钱
					mysqlObj.update('ssc', 'update mn_user set money=money-%s where user_id=%s',[losMoney,loser_userid[0]])
					mysqlObj.commit('ssc')
			#写入游戏记录表
			gamer_list = ','.join(str(i) for i in userList)
			winner = ','.join(str(i) for i in winner)
			loser = ','.join(str(i) for i in loser)
			winnerID = ','.join(str(i) for i in winnerPidList)
			loserID = ','.join(str(i) for i in loserPidList)
			multiple = int(data[5])
			upset = d_money
			mysqlObj.insertOne('lo', 'insert into lo_gamelog (gamer_list,winner,loser,multiple,upset,add_time,add_ymd) values (%s,%s,%s,%s,%s,%s,%s)',[gamer_list,winner,loser,multiple,upset,int(time.time()),ymd])
		else:
			#配3家，其中2家给地主
			print u'nongmin '
			winnerDZPidList = [dz_pid]
			winnerPidList = u[:]
			if dz_pid!=int(leavepid):
				winnerPidList.remove(dz_pid)
				winnerPidList.remove(int(leavepid))
			else:
				winnerPidList.remove(dz_pid)
			loserPidList = [int(leavepid)]
			winDZMoney = loseMoney*2
			winMoney = loseMoney
			losMoney = loseMoney*3
			for x in winnerDZPidList:
				#获得user_id
				winner_userid = mysqlObj.getOne('lo', 'select user_id from lo_logincache where pid=%s',[x])
				winner.append(winner_userid[0])
				userList.append(winner_userid[0])
				#获得用户money
				winnerMoney = mysqlObj.getOne('ssc', 'select money from mn_user where user_id=%s',[winner_userid[0]])
				#写入log日志
				mysqlObj.insertOne('lo', 'insert into lo_rfloat (user_id,r_status,action_type,money,after_money,add_time,add_ymd,note) values (%s,%s,%s,%s,%s,%s,%s,%s)', [winner_userid[0], 1,4,winDZMoney,winnerMoney[0],int(time.time()),ymd,('斗地主获胜获得奖金'+str(winDZMoney)+'元').encode('utf-8') ])
				mysqlObj.commit('lo')
				#修改用户金钱
				mysqlObj.update('ssc', 'update mn_user set money=money+%s where user_id=%s',[winDZMoney,winner_userid[0]])
				mysqlObj.commit('ssc')
			for x in winnerPidList:
				#获得user_id
				winner_userid = mysqlObj.getOne('lo', 'select user_id from lo_logincache where pid=%s',[x])
				winner.append(winner_userid[0])
				userList.append(winner_userid[0])
				#获得用户money
				winnerMoney = mysqlObj.getOne('ssc', 'select money from mn_user where user_id=%s',[winner_userid[0]])
				#写入log日志
				mysqlObj.insertOne('lo', 'insert into lo_rfloat (user_id,r_status,action_type,money,after_money,add_time,add_ymd,note) values (%s,%s,%s,%s,%s,%s,%s,%s)', [winner_userid[0], 1,4,winMoney,winnerMoney[0],int(time.time()),ymd,('斗地主获胜获得奖金'+str(winMoney)+'元').encode('utf-8') ])
				mysqlObj.commit('lo')
				#修改用户金钱
				mysqlObj.update('ssc', 'update mn_user set money=money+%s where user_id=%s',[winMoney,winner_userid[0]])
				mysqlObj.commit('ssc')
			for x in loserPidList:
				loser_userid = mysqlObj.getOne('lo', 'select user_id from lo_logincache where pid=%s',[x])
				loser.append(loser_userid[0])
				userList.append(loser_userid[0])
				#获得用户money
				loserMoney = mysqlObj.getOne('ssc', 'select money from mn_user where user_id=%s',[loser_userid[0]])
				#写入log日志
				mysqlObj.insertOne('lo', 'insert into lo_rfloat (user_id,r_status,action_type,money,after_money,add_time,add_ymd,note) values (%s,%s,%s,%s,%s,%s,%s,%s)', [loser_userid[0], 2,3,losMoney,loserMoney[0],int(time.time()),ymd,('斗地主逃跑输掉了'+str(losMoney)+'元奖金').encode('utf-8') ])
				mysqlObj.commit('lo')
				#修改用户金钱
				mysqlObj.update('ssc', 'update mn_user set money=money-%s where user_id=%s',[losMoney,loser_userid[0]])
				mysqlObj.commit('ssc')
			#写入游戏记录表
			gamer_list = ','.join(str(i) for i in userList)
			winner = ','.join(str(i) for i in winner)
			loser = ','.join(str(i) for i in loser)
			winnerID = ','.join(str(i) for i in winnerPidList)+','+str(winnerDZPidList[0])
			loserID = ','.join(str(i) for i in loserPidList)
			multiple = int(data[5])
			upset = d_money
			mysqlObj.insertOne('lo', 'insert into lo_gamelog (gamer_list,winner,loser,multiple,upset,add_time,add_ymd) values (%s,%s,%s,%s,%s,%s,%s)',[gamer_list,winner,loser,multiple,upset,int(time.time()),ymd])
	winnerID = winnerID.split(',')
	loserID = loserID.split(',')
	winS,losS = [],[]
	for x in winnerID:
		try:
			if u.index(int(x))==0:
				winS.append('f_u')
		except Exception, e:
			continue
		try:
			if u.index(int(x))==1:
				winS.append('s_u')
		except Exception, e:
			continue
		try:
			if u.index(int(x))==2:
				winS.append('t_u')
		except Exception, e:
			continue
	for x in loserID:
		try:
			if u.index(int(x))==0:
				losS.append('f_u')
		except Exception, e:
			continue
		try:
			if u.index(int(x))==1:
				losS.append('s_u')
		except Exception, e:
			continue
		try:
			if u.index(int(x))==2:
				losS.append('t_u')
		except Exception, e:
			continue
	mysqlObj.delete('mn', 'delete from mn_room where room_id=%s',[room_id])
	endDict = {'s':1,'m':'游戏已结束','c':2012,'w':winS,'l':losS,'d':upset,'losemoney':losMoney,'winmoney':winMoney}
	GlobalObject().netfactory.pushObject(3,showDict(endDict),u)
	return endDict	

def outPuke(pid, puke,userPrefix):
	'''出牌方法'''
	mysqlObj = MysqlObject()
	data = mysqlObj.getOne('mn', 'select '+userPrefix+'p,f_u,s_u,t_u,room_id,now_pid from mn_room where spend=3 and timer_pid=%s', [pid])
	if data[0]=='':
		return {'s':-3,'m':'该游戏已结束'}
	db_puke = data[0].split(',')
	if len(db_puke)<len(puke):
		return {'s':-4,'m':'数据出现错误，用户被强制退出登录，并扣除金钱处罚'}
	#print len(db_puke)
	isFind = 0
	#print puke
	upd_puke = []
	for x in range(0,len(db_puke)):
		for y in puke:
			if db_puke[x]==y:
				db_puke[x] = ''

	for x in db_puke:
		if x != '':
			upd_puke.append(x) 
	up_puke = ','.join(upd_puke)#修改牌组信息，数据库移除牌组数据
	u = [int(data[1]), int(data[2]), int(data[3])]
	#数据移到下一个用户,更新timer和timer_pid
	try:
		nowU = u.index(int(pid))
		if nowU==0:
			nowUser = 'f_u'
			nextUser = 's_u'
			nextPid = u[1]
		elif nowU==1:
			nowUser = 's_u'
			nextUser = 't_u'
			nextPid = u[2]
		else:
			nowUser = 't_u'
			nextUser = 'f_u'
			nextPid = u[0]
	except Exception, e:
		return {'s':-4,'m':'数据出现错误，用户被强制退出登录，并扣除金钱处罚'}

	max_puke = unicode(','.join(puke))
	#数据移到下一个用户,更新timer和timer_pid,和数据牌组数据
	mysqlObj.update('mn', 'update mn_room set timer=%s,timer_pid=%s,'+userPrefix+'p=%s,puke_type=%s,max_puke=%s,now_pid=%s where room_id=%s', [int(time.time()), nextPid,up_puke,checkPukeType(puke),max_puke,pid,data[4]])
	pukeType = checkPukeType(puke)
	if pukeType==3 or pukeType==6:
		mysqlObj.update('mn', 'update mn_room set multiple=multiple*2 where room_id=%s', [data[4]])
	
	#判断是否报警或为空
	if len(upd_puke)<=2 and len(upd_puke)!=0:
		#抱警
		bjDict = {'s':1,'m':'还剩'+str(len(upd_puke))+'张牌了','n':nowUser,'c':2010,'mp3':'clock.mp3'}#报警
		#GlobalObject().netfactory.pushObject(3,showDict(bjDict),u)
	elif len(upd_puke)==0:
		#游戏结束
		return game_settle(data[4],u)
	dataC = countValue(puke)
	print dataC
	if pukeType==1:
		if dataC[0][0]==1:
			music = '3.mp3'
		if dataC[0][0]==2:
			music = '4.mp3'
		if dataC[0][0]==3:
			music = '5.mp3'
		if dataC[0][0]==4:
			music = '6.mp3'
		if dataC[0][0]==5:
			music = '7.mp3'
		if dataC[0][0]==6:
			music = '8.mp3'
		if dataC[0][0]==7:
			music = '9.mp3'
		if dataC[0][0]==8:
			music = '10.mp3'
		if dataC[0][0]==9:
			music = '11.mp3'
		if dataC[0][0]==10:
			music = '12.mp3'
		if dataC[0][0]==11:
			music = '13.mp3'
		if dataC[0][0]==12:
			music = '14.mp3'
		if dataC[0][0]==13:
			music = '15.mp3'
		if dataC[0][0]==14:
			music = '16.mp3'
		if dataC[0][0]==15:
			music = '17.mp3'
	elif pukeType==2:
		if dataC[0][0]==1:
			music = 'dui3.mp3'
		if dataC[0][0]==2:
			music = 'dui4.mp3'
		if dataC[0][0]==3:
			music = 'dui5.mp3'
		if dataC[0][0]==4:
			music = 'dui6.mp3'
		if dataC[0][0]==5:
			music = 'dui7.mp3'
		if dataC[0][0]==6:
			music = 'dui8.mp3'
		if dataC[0][0]==7:
			music = 'dui9.mp3'
		if dataC[0][0]==8:
			music = 'dui10.mp3'
		if dataC[0][0]==9:
			music = 'dui11.mp3'
		if dataC[0][0]==10:
			music = 'dui12.mp3'
		if dataC[0][0]==11:
			music = 'dui13.mp3'
		if dataC[0][0]==12:
			music = 'dui14.mp3'
		if dataC[0][0]==13:
			music = 'dui15.mp3'
	if pukeType==3:
		music = 'wangzha.mp3'
	if pukeType==6:
		music = 'zhadan.mp3'
	if data[5]==None or data[5]=='' or data[5]==False:
		if pukeType==4:
			music = 'give.mp3'
		elif pukeType==5:
			music = 'sandaiyi.mp3'
		elif pukeType==7:
			music = 'shunzi.mp3'
		elif pukeType==8:
			music = 'liandui.mp3'
		elif pukeType==9:
			music = 'give.mp3'
		elif pukeType==10:
			music = 'sidaier.mp3'
		elif pukeType==11:
			music = 'sidaier.mp3'
		elif pukeType==12:
			music = 'sandaiyidui.mp3'
		elif pukeType==13:
			music = 'feiji.mp3'
		elif pukeType==14:
			music = 'feiji.mp3'
	else:
		music = 'dani'+str(random.randint(1,3))+'.mp3'
	#推送数据
	showDicts = {'s':1,'p':puke,'n':nowUser, 'c':2011,'next':nextUser, 'mp3':music}
	GlobalObject().netfactory.pushObject(3,showDict(showDicts),u)
	#发送报警数据
	if len(upd_puke)<=2 and len(upd_puke)!=0:
		GlobalObject().netfactory.pushObject(3,showDict(bjDict),u)
	return {'s':1,'m':'出牌成功'}


def showPuke(pid, puke,pukeData):
	'''
	:param pid: 当前用户pid
	:param puke: 当前用户 所出的牌
	:param pukeData: 当前的牌堆数据，已经出过的牌会从牌堆清除
	:return:
	'''
	puke = puke.split(',')
	if len(puke)>0:
		puke = list(set(puke))
	else:
		return {'s':-1,'m':'非法数据'}
	for x in puke:
		if x not in pukeData:
			#如果不在牌组中
			return {'s':-1,'m':'非法数据'}
	#判断是否在他自己的牌中，并且是否该他出牌，并且是否大于最大牌数，并且最大的牌的用户是否是他本身
	#首先梳理逻辑，判断是否在他的牌中
	mysqlObj = MysqlObject()
	data = mysqlObj.getOne('mn', 'select * from mn_room where spend=3 and timer_pid=%s', [pid])

	if data==False or data==None or data[0]=='':
		return {'s':-1,'m':u'游戏不存在'}

	if int(data[1])==pid:
		#用户1
		user_key=4
		userPrefix = 'f_'
	elif int(data[2])==pid:
		#用户2
		user_key=5
		userPrefix = 's_'
	elif int(data[3])==pid:
		#用户3
		user_key=6
		userPrefix = 't_'
	for x in puke:
		if x not in data[user_key]:
			return {'s':-2,'m':'您没有此牌'}
	#判断牌是否合法并返回牌类型
	pukeType = checkPukeType(puke)
	if pukeType==False or pukeType==0:
		return {'s':-2,'m':u'出牌不合法，请重出'}
	#开始判断是否与数据库中的牌型同步
	if pukeType!=int(data[13]) and int(data[13])>0 and pukeType!=3 and pukeType!=6:
		return {'s':-2,'m':u'牌型不符'}
	if int(data[13])==0:#可以出任意合法的牌
		return outPuke(pid,puke,userPrefix)
	#判断当前最大牌是否是他本人
	if data[17]==None:
		now_pid = 0
	else:
		now_pid = int(data[17])
	if pid==now_pid:
		#如果是最大的牌是自己，可以出任意合法的牌
		return outPuke(pid,puke,userPrefix)
	#判断是否有最大牌，如果有，就需要比较两个牌组的大小，否则直接成功
	if data[13]!=0:
		if data[14]!=None and data[14]!='':
			max_puke = data[14].split(',')
			if len(max_puke)>0:
				#比较大小
				if data[13]==1:#单牌
					if pukeType!=1 and pukeType!=3 and pukeType!=6:
						return {'s':-2,'m':u'您出的牌未大过上家'}
					if pukeType==3 or pukeType==6:
						#肯定大于，那么就直接成功了
						return outPuke(pid,puke,userPrefix)
					else:
						#比对两个牌的大小
						if pukeData[puke[0]]>pukeData[max_puke[0]]:
							return outPuke(pid,puke,userPrefix)
						else:
							return {'s':-2,'m':u'您出的牌未大过上家'}
				if data[13]==2:#对子
					if pukeType!=2 and pukeType!=3 and pukeType!=6:
						return {'s':-2,'m':u'您出的牌未大过上家'}
					if pukeType==3 or pukeType==6:
						#肯定大于，那么就直接成功了
						return outPuke(pid,puke,userPrefix)
					else:
						#比对两个牌的大小
						if pukeData[puke[0]]>pukeData[max_puke[0]]:
							return outPuke(pid,puke,userPrefix)
						else:
							return {'s':-2,'m':u'您出的牌未大过上家'}
				if data[13]==3:#王炸
					return {'s':-2,'m':u'您出的牌未大过上家'}
				if data[13]==4:#三不带
					if pukeType!=4 and pukeType!=3 and pukeType!=6:
						return {'s':-2,'m':u'您出的牌未大过上家'}
					if pukeType==3 or pukeType==6:
						#肯定大于，那么就直接成功了
						return outPuke(pid,puke,userPrefix)
					else:
						#比对两个牌的大小
						if pukeData[puke[0]]>pukeData[max_puke[0]]:
							return outPuke(pid,puke,userPrefix)
						else:
							return {'s':-2,'m':u'您出的牌未大过上家'}
				if data[13]==5:#三带一
					if pukeType!=5 and pukeType!=3 and pukeType!=6:
						return {'s':-2,'m':u'您出的牌未大过上家'}
					if pukeType==3 or pukeType==6:
						#肯定大于，那么就直接成功了
						return outPuke(pid,puke,userPrefix)
					else:
						#判断3个那个牌的大小
						p1,p2 = countValue(max_puke),countValue(puke)
						for x in p1:
							if x[1]==3:
								p1_k = x[0]
						for x in p2:
							if x[1]==3:
								p2_k = x[0]
						if p2_k>p1_k:
							return outPuke(pid,puke,userPrefix)
						else:
							return {'s':-2,'m':u'您出的牌未大过上家'}
				if data[13]==6:#炸弹
					if pukeType!=6 and pukeType!=3:
						return {'s':-2,'m':u'您出的牌未大过上家'}
					if pukeData[puke[0]]>pukeData[max_puke[0]] or pukeType==3:
						return outPuke(pid,puke,userPrefix)
					else:
						return {'s':-2,'m':u'您出的牌未大过上家'}
				if data[13]==7:#顺子
					if pukeType!=7 and pukeType!=3 and pukeType!=6:
						return {'s':-2,'m':u'您出的牌未大过上家'}
					if pukeType==3 or pukeType==6:
						#肯定大于，那么就直接成功了
						return outPuke(pid,puke,userPrefix)
					else:
						p1,p2 = countValue(max_puke),countValue(puke)
						if len(p1)!=len(p2):
							return {'s':-2,'m':u'出牌不合法'}
						for x in p1:
							p1_k = x[0]
						for x in p2:
							p2_k = x[0]
						if p2_k>p1_k:
							return outPuke(pid,puke,userPrefix)
						else:
							return {'s':-2,'m':u'您出的牌未大过上家'}
				if data[13]==8:#连对
					if pukeType!=8 and pukeType!=3 and pukeType!=6:
						return {'s':-2,'m':u'您出的牌未大过上家'}
					if pukeType==3 or pukeType==6:
						#肯定大于，那么就直接成功了
						return outPuke(pid,puke,userPrefix)
					else:
						p1,p2 = countValue(max_puke),countValue(puke)
						if len(p1)!=len(p2):
							return {'s':-2,'m':u'出牌不合法'}
						for x in p1:
							p1_k = x[0]
						for x in p2:
							p2_k = x[0]
						if p2_k>p1_k:
							return outPuke(pid,puke,userPrefix)
						else:
							return {'s':-2,'m':u'您出的牌未大过上家'}
				if data[13]==9:#四带1
					if pukeType!=9 and pukeType!=3 and pukeType!=6:
						return {'s':-2,'m':u'您出的牌未大过上家'}
					if pukeType==3 or pukeType==6:
						#肯定大于，那么就直接成功了
						return outPuke(pid,puke,userPrefix)
					else:
						p1,p2 = countValue(max_puke),countValue(puke)
						for x in p1:
							if x[1]==4:
								p1_k = x[0]
						for x in p2:
							if x[1]==4:
								p2_k = x[0]
						if p2_k>p1_k:
							return outPuke(pid,puke,userPrefix)
						else:
							return {'s':-2,'m':u'您出的牌未大过上家'}
				if data[13]==10:#四带对
					if pukeType!=10 and pukeType!=3 and pukeType!=6:
						return {'s':-2,'m':u'您出的牌未大过上家'}
					if pukeType==3 or pukeType==6:
						#肯定大于，那么就直接成功了
						return outPuke(pid,puke,userPrefix)
					else:
						p1,p2 = countValue(max_puke),countValue(puke)
						for x in p1:
							if x[1]==4:
								p1_k = x[0]
						for x in p2:
							if x[1]==4:
								p2_k = x[0]
						if p2_k>p1_k:
							return outPuke(pid,puke,userPrefix)
						else:
							return {'s':-2,'m':u'您出的牌未大过上家'}
				if data[13]==11:#四带2
					if pukeType!=11 and pukeType!=3 and pukeType!=6:
						return {'s':-2,'m':u'您出的牌未大过上家'}
					if pukeType==3 or pukeType==6:
						#肯定大于，那么就直接成功了
						return outPuke(pid,puke,userPrefix)
					else:
						p1,p2 = countValue(max_puke),countValue(puke)
						for x in p1:
							if x[1]==4:
								p1_k = x[0]
						for x in p2:
							if x[1]==4:
								p2_k = x[0]
						if p2_k>p1_k:
							return outPuke(pid,puke,userPrefix)
						else:
							return {'s':-2,'m':u'您出的牌未大过上家'}
				if data[13]==12:#三带二
					if pukeType!=12 and pukeType!=3 and pukeType!=6:
						return {'s':-2,'m':u'您出的牌未大过上家'}
					if pukeType==3 or pukeType==6:
						#肯定大于，那么就直接成功了
						return outPuke(pid,puke,userPrefix)
					else:
						p1,p2 = countValue(max_puke),countValue(puke)
						for x in p1:
							if x[1]==3:
								p1_k = x[0]
						for x in p2:
							if x[1]==3:
								p2_k = x[0]
						if p2_k>p1_k:
							return outPuke(pid,puke,userPrefix)
						else:
							return {'s':-2,'m':u'您出的牌未大过上家'}
				if data[13]==13:#飞机1
					if pukeType!=13 and pukeType!=3 and pukeType!=6:
						return {'s':-2,'m':u'您出的牌未大过上家'}
					if pukeType==3 or pukeType==6:
						#肯定大于，那么就直接成功了
						return outPuke(pid,puke,userPrefix)
					else:
						p1,p2 = countValue(max_puke),countValue(puke)
						if len(p1)!=len(p2):
							return {'s':-2,'m':u'出牌不合法'}
						for x in p1:
							if x[1]==3:
								p1_k = x[0]
						for x in p2:
							if x[1]==3:
								p2_k = x[0]
						if p2_k>p1_k:
							return outPuke(pid,puke,userPrefix)
						else:
							return {'s':-2,'m':u'您出的牌未大过上家'}
				if data[13]==14:#飞机2,带单的飞机
					if pukeType!=14 and pukeType!=3 and pukeType!=6:
						return {'s':-2,'m':u'您出的牌未大过上家'}
					if pukeType==3 or pukeType==6:
						#肯定大于，那么就直接成功了
						return outPuke(pid,puke,userPrefix)
					else:
						p1,p2 = countValue(max_puke),countValue(puke)
						if len(p1)!=len(p2):
							return {'s':-2,'m':u'出牌不合法'}
						for x in p1:
							if x[1]==3:
								p1_k = x[0]
						for x in p2:
							if x[1]==3:
								p2_k = x[0]
						if p2_k>p1_k:
							return outPuke(pid,puke,userPrefix)
						else:
							return {'s':-2,'m':u'您出的牌未大过上家'}
	return {'s':1,'m':''}

def mustPuke(pid):
	'''必须出'''
	pid = int(pid)
	mysqlObj = MysqlObject()
	data = mysqlObj.getOne('mn', 'select f_u,s_u,t_u,f_p,s_p,t_p,room_id,puke_type,now_pid from mn_room where spend=3 and timer_pid=%s and now_pid is null', [pid])
	if data==False or data==None or data[0]=='':
		return {'s':-1,'m':u'游戏不存在'}
	if pid==int(data[0]):
		puke = data[3].split(',')
	if pid==int(data[1]):
		puke = data[4].split(',')
	if pid==int(data[2]):
		puke = data[5].split(',')
	if len(puke)<1:
		return {'s':-1,'m':u'游戏已结束'}
	puke = sortPuke(puke)
	showpuke = showPuke(pid,puke[0],pukeData)
	return showpuke


def unOutPuke(pid):
	'''不出'''
	pid = int(pid)
	mysqlObj = MysqlObject()
	#判断用户位置
	data = mysqlObj.getOne('mn', 'select f_u,s_u,t_u,room_id,puke_type,now_pid from mn_room where spend=3 and timer_pid=%s', [pid])
	if data==False or data==None or data[0]=='':
		return {'s':-1,'m':u'游戏不存在'}
	if data[4]==0 or data[4]==None:
		return {'s':-2,'m':u'您必须出牌'}
	if data[5]==None:
		return {'s':-2,'m':u'您必须出牌'}
	if int(data[0])==pid:
		nowUser = 'f_u'
		nextUser = int(data[1])
		nextU = 's_u'
	if int(data[1])==pid:
		nowUser = 's_u'
		nextUser = int(data[2])
		nextU = 't_u'
	if int(data[2])==pid:
		nowUser = 't_u'
		nextUser = int(data[0])
		nextU = 'f_u'
	u = [data[0],data[1],data[2]]
	if nextUser==int(data[5]):
		mysqlObj.update('mn', 'update mn_room set timer=%s,timer_pid=%s,puke_type=0,now_pid=null,max_puke=null where room_id=%s', [int(time.time()), nextUser,data[3]])
	else:
		mysqlObj.update('mn', 'update mn_room set timer=%s,timer_pid=%s where room_id=%s', [int(time.time()), nextUser,data[3]])

	unOutDict = {'s':1,'c':2013, 'p':nowUser}
	GlobalObject().netfactory.pushObject(3,showDict(unOutDict),u)
	nextDict = {'s':1,'p':'','n':nowUser, 'c':2011,'next':nextU, 'mp3':'NO'+str(random.randint(1,4))+'.mp3'}
	GlobalObject().netfactory.pushObject(3,showDict(nextDict),u)
	return {'s':1,'m':''}


def getUserInfo(pid):
	'''拉取用户信息和资金'''
	mysqlObj = MysqlObject()
	user_id = mysqlObj.getOne('lo', 'select user_id from lo_logincache where pid=%s', [pid])
	if user_id==False:
		return {'s':-1,'m':'用户未登录'}
	else:
		user_info = mysqlObj.getOne('ssc', 'select user_id,user_name,money,qq from mn_user where user_id=%s and is_lock=1', [user_id[0]])
		if user_id==False:
			return {'s':-1,'m':'用户不存在或已被锁定'}
		user_info = list(user_info)
		return {'s':1,'data':user_info}



def loginCache(pid,user_id,user_name):
	mysqlObj = MysqlObject()
	'''写入用户信息memcache'''
	isLogin = mysqlObj.getOne('lo', 'select count(pid) as a from lo_logincache where user_id=%s',[user_id])
	if isLogin==False or isLogin[0]<1:
		#写入
		mysqlObj.insertOne('lo', 'insert into lo_logincache (pid,user_id,user_name) values (%s,%s,%s)',[pid,user_id,user_name])
		return True
	else:
		#报错，并断开连接
		return False

def joinQueue(pid,room_type):
	mysqlObj = MysqlObject()
	isjoinQueue = mysqlObj.getOne('mn', 'select * from mn_gamequeue where pid=%s',[pid])
	if isjoinQueue==False or isjoinQueue[0]<1:
		isInGame = mysqlObj.getOne('mn','select count(id) as a from mn_room where f_u=%s or s_u=%s or t_u=%s', [pid])
		if isInGame==False or isInGame[0]<1:
			mysqlObj.insertOne('mn', 'insert into mn_gamequeue (pid,room_type) values (%s,%s)',[pid,room_type])
			return {'s':1,'m':''}	#flash操作号1001
		else:
			return {'s':-1,'m':'您已经在游戏队列中了'}
	else:
		return {'s':-1,'m':'您已经在游戏队列中了'}

def outQueue(pid):
	'''离开游戏队列'''
	mysqlObj = MysqlObject()
	isjoinQueue = mysqlObj.getOne('mn', 'select count(pid) as a from mn_gamequeue where pid=%s', [pid])
	if isjoinQueue==False or isjoinQueue[0]<1:
		return False
	isjoinQueue = mysqlObj.delete('mn', 'delete from mn_gamequeue where pid=%s', [pid])
	return True

def delLoginCache(pid):
	mysqlObj = MysqlObject()
	mysqlObj.delete('lo','delete from lo_logincache where pid=%s',[pid])
	mysqlObj.delete('mn','delete from mn_gamequeue where pid=%s',[pid])

def randomStr():
	strRand = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789&#%^*'
	randList = []
	for x in range(0,8):
		randList.append(random.choice(strRand))
	return ''.join(randList)

def setHeart(pid):
	mysqlObj = MysqlObject()
	isPid = mysqlObj.getOne('mn', 'select count(pid) as a from mn_heart where pid=%s',[pid])
	if isPid==False or isPid[0]<1:
		#写入心跳
		u = mysqlObj.insertOne('mn', 'insert into mn_heart (pid, heart_time) values (%s,%s)', [pid, int(time.time())])
	else:
		#更新心跳
		u = mysqlObj.update('mn', 'UPDATE mn_heart SET heart_time=%s WHERE pid=%s', [int(time.time()), pid])
	if u==False:
		return {'s':-1,'m':'更新心跳出错，连接断开'}

def removeHeart(pid):
	mysqlObj = MysqlObject()
	mysqlObj.delete('mn', 'delete from mn_heart where pid=%s',[pid])

def checkRoom(pid):
	mysqlObj = MysqlObject()
	isRoom = mysqlObj.getOne('mn', 'select room_id,f_u,t_u,s_u from mn_room where f_u=%s or s_u=%s or t_u=%s', [pid,pid,pid])
	if isRoom==False or isRoom[0]==None or isRoom[0]=='':
		#没有进入房间
		return {'s':1}
	else:
		#在房间中存在,就要开始结算游戏，然后执行扣款加款
		return game_settle(isRoom[0], [int(isRoom[1]),int(isRoom[2]),int(isRoom[3])],pid)

def checkLogin(pid):
	mysqlObj = MysqlObject()
	isLogin = mysqlObj.getOne('mn', 'select count(pid) as a from mn_heart where pid=%s',[pid])
	if isLogin==False or isLogin[0]<1:
		returnData = False
	else:
		returnData = True
	return returnData

def sysMsg(text):
	return {'t':'系统消息：','c':text}

def userTalk(user_name, text):
	return {'t':user_name+'：','c':text}

def heartCheck():
	mysqlObj = MysqlObject()
	'''心跳检测的方法, 每10秒一次  返回需移除的PID list'''
	nowUnixTime = int(time.time())
	timeoutList = mysqlObj.getMany('mn', 'select pid from mn_heart where %s-heart_time>=30'[nowUnixTime], 500)#3次应答失败
	if len(timeoutList)>0:
		for x in timeoutList:
			mysqlObj.delete('mn', 'delete from mn_heart where pid=%s', [x[0]])
	return

def userLogin(userData):
	'''用户登录的方法'''
	if userData.has_key('user_id')==False or userData['user_id']=='':
		return {'status':-2999, 'msg':'用户ID错误'}
	if userData.has_key('user_name')==False or userData['user_name']=='':
		return {'status':-2998, 'msg':'用户名错误'}

	if userData.has_key('user_key')==False or userData['user_key']=='':
		return {'status':-2997, 'msg':'用户密钥错误'}
	#读取全局配置key
	sunnyKey = getConfig().get('other')['authenticationKey']
	#组建密钥

	#wtx-start@20170209@001@（1）暂时不了解加密，因此将该部分忽略掉。 （2）那么用户注册时的userKey也需要做相应的改动
	#userKey = hashlib.md5(str(userData['user_id'])+userData['user_name']+sunnyKey.upper()).hexdigest().upper() #wtx:没看出密钥用途？
	userKey = str(userData['user_key'])
	#wtx-end@20170209@001

	if str(userData['user_key'])!=str(userKey):
		return {'status':-2996, 'msg':'用户信息错误，请重新登录'}
	else:
		return {'status':1, 'msg':'验证成功'}
	#wtx-end@20170125@002@


def regUser(userData):
	'''用户注册方法'''

	mysqlObj = MysqlObject()
	if userData.has_key('user_name')==False or userData['user_name']=='':
		return {'status':-1999, 'msg':'请输入用户名'}
	if userData.has_key('user_pass')==False or userData['user_pass']=='':
		return {'status':-1998, 'msg':'请输入用户密码'}

	if userData.has_key('nick_name')==False:
		userData['nick_name'] = ''
	if userData.has_key('email')==False:
		userData['email'] = ''
	if userData.has_key('phone')==False:
		userData['phone'] = ''
	if userData.has_key('qq')==False:
		userData['qq'] = ''
	if userData.has_key('q_one')==False:
		userData['q_one'] = ''
	if userData.has_key('a_one')==False:
		userData['a_one'] = ''
	if userData.has_key('q_two')==False:
		userData['q_two'] = ''
	if userData.has_key('a_two')==False:
		userData['a_two'] = ''
	if userData.has_key('credentials')==False:
		userData['credentials'] = ''
	if userData.has_key('add_ip')==False:
		userData['add_ip'] = ''
	#检测用户名是否合法
	if len(userData['user_name'])<6 or len(userData['user_name'])>16:
		return {'status':-1997, 'msg':'用户名长度在6~16位之间'}
	if len(userData['user_pass'])<6 or len(userData['user_pass'])>16:
		return {'status':-1996, 'msg':'密码长度在6~16位之间'}
	#开始进行数据检测，检测重复等
	isUserName = mysqlObj.getOne('us', 'select count(*) from us_user where user_name=%s',[userData['user_name']])

	if isUserName!=None and isUserName[0]>0:
		return {'status':-1995, 'msg':'用户名已存在'}

	if userData['nick_name']!='':
		isNiceName = mysqlObj.getOne('us', 'select count(*) from us_userbase where nick_name=%s',[userData['nick_name']])

		if isNiceName!=None and isNiceName[0]>0:
			return {'status':-1995, 'msg':'用户昵称已存在'}
		userList.append(userData['nick_name']) #wtx:为什么这里添加list？
	if userData['email']!='':
		isEmail = mysqlObj.getOne('us', 'select count(*) from us_userbase where email=%s',[userData['email']])

		if isEmail!=None and isEmail[0]>0:
			return {'status':-1995, 'msg':'用户邮箱已存在'}
	if userData['phone']!='':
		isPhone = mysqlObj.getOne('us', 'select count(*) from us_userbase where phone=%s',[userData['phone']])

		if isPhone!=None and isPhone[0]>0:
			return {'status':-1994, 'msg':'用户手机已存在'}
	if userData['qq']!='':
		isQQ = mysqlObj.getOne('us', 'select count(*) from us_userbase where qq=%s',[userData['phone']])

		if isQQ!=None and isQQ[0]>0:
			return {'status':-1993, 'msg':'用户QQ已存在'}
	#组建密码
	pass_rand = randomStr()

	#wtx-start@20170209@002@不加密密码，用于测试
	password = hashlib.md5(str(userData['user_pass']) + pass_rand).hexdigest().upper()
	password = str(userData['user_pass']) #wtx：不加密密码，为了方便测试
	funds_key = hashlib.md5('0' + pass_rand).hexdigest().upper()
	funds_key = pass_rand #wtx:不加密资金key
	#wtx-end@20170209@002@不加密密码，用于测试

	userList = [userData['user_name'], password, pass_rand, 0, funds_key, 1]	
	#开启事务
	try:
		mysqlObj.begin('us')
		returnAdd = mysqlObj.insertOne('us', \
			'INSERT INTO us_user (user_name, user_pass, pass_rand, balance, funds_key, is_lock) VALUES (%s, %s, %s, %s, %s, %s)',userList)
		if returnAdd==False:
			raise Exception('写入用户表错误',-1992)
		userBaseList = [returnAdd, userData['nick_name'], userData['email'], userData['phone'], userData['qq'], 
						userData['q_one'], userData['a_one'], userData['q_two'], userData['a_two'], userData['credentials'], \
						'', int(time.time()), datetime.datetime.now().strftime('%Y-%m-%d'), userData['add_ip']]
		returnAddBase = mysqlObj.insertOne('us', \
			'INSERT INTO us_userbase (user_id, nick_name, email, phone, qq, q_one, a_one, q_two, a_two, credentials, credentials_img, add_time, add_ymd, add_ip) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s)',userBaseList,0)
		if returnAddBase==False:
			raise Exception('写入用户表基础表错误',-1991)
			mysqlObj.getErrorMsg()
		mysqlObj.commit('us')										#提交事务
	except Exception, e:
		return {'status':e[1], 'msg':'创建用户失败'}
		mysqlObj.rollback('us')									#回滚事务
	return {'status':1, 'msg':'创建用户成功'}
	


if __name__ == '__main__':
	'''
	1.wtx:为了测试服务器，需要先添加几个临时的测试用户
	'''
	print memcache.get('heartList')
	for i in range(0,9,1):
		# wtx1:注册3个用户
		userData = {
			'user_name': 'aaaaa' + str(i),
			'user_pass':'123456'
		}
		print regUser(userData)
		# wtx2：将3个注册好的用户登录
		userData = {
			'user_name': 'aaaaa' + str(i),
			'user_id': str(i),
			'user_key':'C9855A3C3AF6149772659CBA9D33D4A3'
		}
		print userLogin(userData)

	# print heartCheck()

def addTest():
	print memcache.get('heartList')
	for i in range(0, 9, 1):
		# wtx1:注册几个用户
		userData = {
			'user_name': 'aaaaa' + str(i),
			'user_pass': '123456'
		}
		print userData
		print regUser(userData)
		# wtx2：将3个注册好的用户登录
		userData = {
			'user_name': 'aaaaa' + str(i),
			'user_id': str(i),
			'user_key': 'C9855A3C3AF6149772659CBA9D33D4A3'
		}
		# print userLogin(userData) #wtx:只注册用户，不登录