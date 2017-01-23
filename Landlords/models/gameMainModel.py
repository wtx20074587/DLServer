# -*- coding: utf8 -*-
from sysModel import MysqlObject,MemcacheEx,__version__,getConfig						#引入mysql, memcache, 系统模块版本号
#from userModel import memcache						
import random,hashlib,time,datetime,os,json
pukeData = {"h8": 6, "f3": 1, "f4": 2, "f5": 3, "f6": 4, "f7": 5, "f8": 6, "h3": 1, "h6": 4, "h7": 5, "h4": 2, "h5": 3, "b4": 2, "b5": 3, "b6": 4, "b7": 5, "b2": 13, "b3": 1, "b8": 6, "b9": 7, "s9": 7, "s8": 6, "fA": 12, "s3": 1, "s2": 13, "s7": 5, "s6": 4, "s5": 3, "s4": 2, "h2": 13, "f9": 7, "P2": 14, "P1": 15, "sQ": 10, "f2": 13, "sK": 11, "sJ": 9, "h9": 7, "sA": 12, "fQ": 10, "hA": 12, "bA": 12, "hQ": 10, "bJ": 9, "bK": 11, "hJ": 9, "hK": 11, "bQ": 10, "fJ": 9, "fK": 11, "f10":8, "s10":8,"b10":8,"h10":8}

'''TimerCache = memcache.get('timeCache')
if TimerCache==None:
	TimerCache = {}'''

#gameZone = []				#游戏空间[[{user_1:0},{user_2:0},{user_3:0}],[{user_1:1},{user_2:1},{user_3:2}]]		
def showUserCount():
	mysqlObj = MysqlObject()
	s = mysqlObj.getOne('mn', 'select count(pid) as a from mn_heart')
	if s==False:
		s=0
	else:
		s=s[0]
	return s

def gameMatching(userList):
	'''随机匹配游戏玩家'''
	if len(userList)<3:
		return {'status':-1999}
	pid_one = random.choice(userList)
	userList.remove(pid_one)
	pid_two = random.choice(userList)
	userList.remove(pid_two)
	pid_three = random.choice(userList)
	matchList = [pid_one, pid_two, pid_three]
	return {'status':1, 'matchList':matchList}

def _puke():
	'''生成扑克牌'''
	s1 = ['s','h','f','b']			#黑桃spade，红桃hearts，梅花flower，方块block
	s2 = ["3","4","5","6","7","8","9","10","J","Q","K","A","2"]
	s3 = ['P1','P2']				#大王，小王
	s4 = [] #s4是返回值，作为最终的牌形
	for x in range(0,52):
		s4.append(s1[x % 4]+s2[x/4]) #分别附加花色(s1)和数字(s2)
	for x in s3:
		s4.append(x) #最终生成牌型。
	return s4

def _wash():
	'''洗牌的方法
	wtx:需要重新设置洗牌算法
	'''
	pukeList = _puke()
	#循环100次随机交换两张牌实现洗牌
	for x in range(0,100):
		rand_one = random.randint(0, 53) #风险：底牌是大小王的概率是多少？
		rand_two = random.randint(0, 53)
		pukeListValue = pukeList[rand_one]
		pukeList[rand_one] = pukeList[rand_two]
		pukeList[rand_two] = pukeListValue
	return pukeList

def shufflingLicensing():
	'''
		洗牌发牌的方法，并整理排序, 这里的思路是先发牌，后排序，因为牌组一共有54张牌，除去三张一共还剩51,3个人，每人17张
		return list [[玩家1的牌,玩家2的牌,玩家3的牌,地主牌],[整理后的玩家1的牌,整理后的玩家2的牌,整理后的玩家3的牌]]
	'''
	(player_one, player_two, player_three) = ([], [], [])
	#(sortPlayer_one, sortPlayer_two, sortPlayer_three) = ({},{},{})
	pukeList = _wash()
	pukeSortList = _puke()
	for x in range(0,17):
		player_one.append(pukeList[0])
		pukeList.remove(pukeList[0])
		player_two.append(pukeList[0])
		pukeList.remove(pukeList[0])
		player_three.append(pukeList[0])
		pukeList.remove(pukeList[0])
	'''for x in player_one:
		sortPlayer_one.setdefault(pukeSortList.index(x), x)
	for x in player_two:
		sortPlayer_two.setdefault(pukeSortList.index(x), x)
	for x in player_three:
		sortPlayer_three.setdefault(pukeSortList.index(x), x)
	sortPlayer_one = sorted(sortPlayer_one.items(), key=lambda d:d[0])
	sortPlayer_two = sorted(sortPlayer_two.items(), key=lambda d:d[0])
	sortPlayer_three = sorted(sortPlayer_three.items(), key=lambda d:d[0])
	sortPlayer_one = [x[1] for x in sortPlayer_one] 
	sortPlayer_two = [x[1] for x in sortPlayer_two] 
	sortPlayer_three = [x[1] for x in sortPlayer_three] '''
	#return [[player_one,player_two,player_three,pukeList], [sortPlayer_one,sortPlayer_two,sortPlayer_three]]
	return [player_one,player_two,player_three,pukeList]

def sortPuke(pukeList):
	'''整理牌的顺序，用于抢地主后的地主整理'''
	pukeSortList = _puke()
	sortPlayer = {}
	for x in pukeList:
		sortPlayer.setdefault(pukeSortList.index(x), x)
	sortPlayer = sorted(sortPlayer.items(), key=lambda d:d[0])
	sortPlayer = [x[1] for x in sortPlayer] 
	return sortPlayer

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

def checkPukeType(pukeList):
	'''牌型判断'''
	#开始进行判断
	pukeLen = len(pukeList)
	#首先判断牌型是否合法
	for x in pukeList:
		if pukeData.has_key(x)==False:
			return False
	#再判断牌组中是否有重复
	pukeLenCheck = sorted(set(pukeList),key=pukeList.index)
	if len(pukeLenCheck)!=pukeLen:
		return False
	#再判断牌组中是否存在已出的牌，即玩家手中不存在的牌，这里的判断放到出牌逻辑，该函数只做牌型判断

	#定义牌型
	c = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,0] #定义各种牌型：单，对，炸，顺子等（共计15种）。
	countList = countValue(pukeList)
	if countList==False:
		return False
	#定义连续字符串
	isLian = '123456789101112'
	if pukeLen<5:
		#先判断小于5的
		if pukeLen==1:
			return c[0]#单
		if pukeLen==2 and len(countList)==1:
			return c[1]#对
		if pukeLen==2 and pukeData[pukeList[0]]>=14 and pukeData[pukeList[1]]>=14:
			return c[2]#王炸
		if pukeLen==3 and len(countList)==1:
			return c[3]#三不带
		if pukeLen==4 and len(countList)==2 and (countList[0][1]==3 or countList[1][1]==3):
			return c[4]#三带一
		if pukeLen==4 and len(countList)==1:
			return c[5]#炸弹
	elif pukeLen>=5:
		#再判断大于等于5的
		if pukeLen==len(countList):
			dl = []
			for x in countList:
				dl.append(str(x[0]))
			dl = ''.join(dl)
			if dl in isLian:
				return c[6]#顺子
		if pukeLen==len(countList)*2 and len(countList)>=3:
			isL,dl = 1,[]
			for x in countList:
				#判断是否连续
				dl.append(str(x[0]))
				if x[1]!=2:
					isL = 0
					break
			dl = ''.join(dl)
			if isL==1 and dl in isLian:
				return c[7]#连对
		if pukeLen==5 and len(countList)==2:#四带1
			for x in countList:
				if x[1]==4:
					return c[8]#四带1
		if pukeLen==6:#四带对或四带2
			if len(countList)==2:
				for x in countList:
					if x[1]==4:
						return c[9]#四带对
			if len(countList)==3:
				for x in countList:
					if x[1]==4:
						return c[10]#四带2
		if pukeLen%5==0 and len(countList)==(pukeLen/5*2):#三带2或飞机1
			if pukeLen==5:
				dt,dd = 0,0	#三张#两张
				for x in countList:
					if x[1]==3:
						dt+=1
					if x[1]==2:
						dd+=1
				if dt==1 and dd==1:
					return c[11]#三带二
			else:#大于5张的
				dl,dt,dd = [],0,0
				for x in countList:
					if x[1]==3:
						dl.append(str(x[0]))
						dt+=1
					if x[1]==2:
						dd+=1
				if dt==pukeLen/5 and dd==pukeLen/5:#第一层判断，判断数量是否正确
					if ''.join(dl) in isLian:#第二层判断，判断是否连续	3-A
						return c[12]#飞机1
		if pukeLen%4==0 and len(countList)==(pukeLen/4*2) and pukeLen>4:
			#飞机二
			dl,dt,ds = [],0,0
			for x in countList:
				if x[1]==3:
					dl.append(str(x[0]))
					dt+=1
				if x[1]==1:
					ds+=1
			if dt==pukeLen/4 and ds==pukeLen/4:
				if ''.join(dl) in isLian:#第二层判断，判断是否连续	3-A
					return c[13]#飞机2,带单的飞机
	return c[14]



def checkPukeSize(pid, pukeList):
	mysqlObj = MysqlObject()
	'''匹配出牌是否合法'''
	#取出房间当前最大的牌面
	maxPuke = mysqlObj.getOne('mn','select max_puke from mn_room where f_u=%s or s_u=%s or t_u=%s', [pid,pid,pid])
	if maxPuke==False:
		return {'s':-1,'m':u'房间不存在'}
	#检查用户是那个位置
	userSort =	mysqlObj.getOne('mn','select f_u,s_u,t_u from mn_room where f_u=%s or s_u=%s or t_u=%s', [pid,pid,pid])
	if userSort==False:
		return {'s':-1,'m':u'房间不存在'}
	if userSort[0]==pid:#位置1
		userPrefix = 'f_'
	elif userSort[1]==pid:#位置2
		userPrefix = 's_'
	elif userSort[2]==pid:#位置3
		userPrefix = 't_'
	#检查用户手中的牌
	userPuke = mysqlObj.getOne('mn','select '+userPrefix+'p,spend from mn_room where '+userPrefix+'u=%s', [pid])
	if userPuke==False:
		return {'s':-1,'m':u'房间不存在'}
	if userPuke[0]=='' and userPuke[1]==1:
		#抢地主阶段不允许出牌
		return {'s':-1,'m':u'非法请求'}
	if userPuke[0]=='' and userPuke[1]==2:
		#游戏已结束
		return {'s':-1,'m':u'非法请求'} 
	#检查牌  
	hasPuke = userPuke[0].split(',')
	for x in pukeList:
		if x not in pukeList:
			return {'s':-1,'m':u'您没有这个牌，请重出'}
	#都通过了，那么我们就可以验证牌型了
	pukeType = checkPukeType(pukeList)
	if pukeType==False or pukeType==0:
		return {'s':-1,'m':u'出牌不合法，请重出'}
	#与数据库牌型比较


'''class gameMain(object):
	def __init__(self, userList):
		self.userList = userList
		self.showUserPuke,self.userPuke = {},{}
		self.timerClass = object

	def run(self):
		global TimerCache
		pukeList = shufflingLicensing()
		#得到牌组之后开始给每个人划分牌组
		for x in range(3):
			self.showUserPuke.setdefault(self.userList[x], pukeList[0][x])
			self.userPuke.setdefault(self.userList[x], pukeList[1][x])
		print u'分开向用户发送未整理前的牌组数据：',self.showUserPuke
		print u'分开向用户发送整理后的牌组数据：',self.userPuke
		#开始抢地主,随机抽选一个
		y = random.randint(0, 2)
		#实例化化Timer
		for x in range(3):
			if y>2:				#如果键值大于2，表示超出下标，则回到起始点
				y=0
			self.timerClass = Timer(self, self.userList[y])
			returnData = self.timerClass.timing()				#执行定时器
			del TimerCache[self.userList[y]]
			if TimerCache=={}:
				memcache.delete('timeCache')
			else:
				memcache.set('timeCache', TimerCache)
			if returnData==-1:
				print self.userList[y],u'超时'
			else:
				return self.userPuke[0]
				print u'获取用户请求:',self.userList[y]
			y+=1
		return self.userPuke


class Timer(object):
	def __init__(self, parent, PID):
		self.parent = parent
		self.PID = PID
	def timing(self, timeout=20):
		global TimerCache
		if self.PID not in TimerCache:
			TimerCache.setdefault(self.PID, 1)
		else:
			TimerCache[self.PID] = 1
		memcache.set('timeCache', TimerCache)
		for x in range(timeout):
			TimerCache = memcache.get('timeCache')
			if self.PID in TimerCache:
				if TimerCache[self.PID]==0:
					return 1
					break
			else:
				return -1
				break
			time.sleep(1)
		return -1'''
if __name__ == '__main__':
	#print showUserCount()
	'''joinGameQueue(1)
	joinGameQueue(4)
	joinGameQueue(5)'''
	#print memcache.get('joinGameList')
	#main = gameMain([1,4,5])
	#main.run()
	'''puke = _puke()
	lastPuke = {}
	for x in puke:
		#print x[-1]
		#print x[:-1]
		if x[:-1]!='P':
			if x[-1]=='3':
				lastPuke[x] = 1
			if x[-1]=='4':
				lastPuke[x] = 2
			if x[-1]=='5':
				lastPuke[x] = 3
			if x[-1]=='6':
				lastPuke[x] = 4
			if x[-1]=='7':
				lastPuke[x] = 5
			if x[-1]=='8':
				lastPuke[x] = 6
			if x[-1]=='9':
				lastPuke[x] = 7
			if x[-1]=='10':
				lastPuke[x] = 8
			if x[-1]=='J':
				lastPuke[x] = 9
			if x[-1]=='Q':
				lastPuke[x] = 10
			if x[-1]=='K':
				lastPuke[x] = 11
			if x[-1]=='A':
				lastPuke[x] = 12
			if x[-1]=='2':
				lastPuke[x] = 13
		else:
			if x[-1]=='1':
				lastPuke[x] = 15
			else:
				lastPuke[x] = 14
	print lastPuke
	f = open('1.json', 'wb+')
	f.write(json.dumps(lastPuke))
	f.close()'''
	#print checkPukeType(['h3','f3','b3','s6','h4','f4','b4','s7']) #双飞，带2个单张