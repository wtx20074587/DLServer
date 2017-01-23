#coding:utf8
import sys,os,time
from firefly.server.globalobject import remoteserviceHandle,GlobalObject
from models.userModel import removeGame,unOutPuke,mustPuke
from models.sysModel import showDict

@remoteserviceHandle("timer")
def clearclient_200(data):
	GlobalObject().netfactory.loseConnection(int(data[0]))

@remoteserviceHandle("timer")
def sendpuke_201(_sessionnoList, data):
	GlobalObject().netfactory.pushObject(3,data,_sessionnoList)

@remoteserviceHandle("timer")
def dzpid_202(_sessionnoList, data):
	GlobalObject().netfactory.pushObject(3,data,_sessionnoList)

@remoteserviceHandle("timer")
def removegame_203(room_id):
	removeGame(room_id)

@remoteserviceHandle("timer")
def nextoutpuke_204(pid):
	unOut = unOutPuke(pid)
	if unOut['s']!=1:
		GlobalObject().netfactory.pushObject(3,showDict(unOut),[pid])

@remoteserviceHandle("timer")
def nextmustpuke_205(pid):
	mustOut = mustPuke(pid)
	if mustOut['s']!=1:
		GlobalObject().netfactory.pushObject(3,showDict(mustOut),[pid])

GlobalObject().remote['timer'].callRemote('timerconnection_1000')
GlobalObject().remote['timer'].callRemote('timerconnection_999')
GlobalObject().remote['timer'].callRemote('timerconnection_998')
GlobalObject().remote['timer'].callRemote('timerconnection_997')