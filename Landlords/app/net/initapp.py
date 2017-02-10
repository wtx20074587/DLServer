#coding:utf8
from firefly.server.globalobject import rootserviceHandle,GlobalObject
from firefly.netconnect.datapack import DataPackProtoc
from models.userModel import removeHeart,checkRoom,delLoginCache,initCache
import time


dataprotocl = DataPackProtoc(127,12,24,22,65,1)#定义协议
GlobalObject().netfactory.setDataProtocl(dataprotocl)

'''连接断开时'''
def doConnectionLost(conn):
	losePid = conn.transport.sessionno
	#然后判断玩家是否在游戏中，如果在游戏，就强行结算游戏 _conn.transport.loseConnection()
	s = checkRoom(losePid)
	if s:
		#if s['s']==1:
		#先清空心跳
		removeHeart(losePid)
		#清除用户缓存
		delLoginCache(losePid)

GlobalObject().netfactory.doConnectionLost = doConnectionLost

def initmain(): #wtx:这里import之后才能启动应用？
	import plub.login
	import plub.setheart
	import plub.console
	import plub.methodcallback
	import plub.registerUser #wtx: 20170210add 用于添加新的接口666。测试通过。
	initCache()	#初始化缓存