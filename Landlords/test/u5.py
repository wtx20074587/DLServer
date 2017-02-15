#coding:utf8

import time,threading,random,json

from socket import AF_INET,SOCK_STREAM,socket
from thread import start_new
import threading,thread,logging
import struct,sys

# 初始化log工具
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='user_5.log',
                filemode='w')
# 基本参数
HOST='52.199.191.77'
PORT=843
BUFSIZE=1024
ADDR=(HOST , PORT)
CURRENTUSER = 4
# 指令类型
LOGIN = 1 #登录
TIMER = 2 #心跳
HANDLE = 3 #抢地主，强退等
DEAL = 4 #请求发牌

#新建socket连接
client = socket(AF_INET,SOCK_STREAM)
client.connect(ADDR)

TEST_USERS = [
"[1,[2, 'aaaaa0', '123456']]",
"[1,[3, 'aaaaa1', '123456']]",
"[1,[4, 'aaaaa2', '123456']]",
"[1,[5,'aaaaa3','123456']]",
"[1,[6,'aaaaa4','123456']]",
"[1,[7,'aaaaa5','123456']]",
"[1,[8,'aaaaa6','123456']]",
"[1,[9,'aaaaa7','123456']]",
"[1,[10,'aaaaa8','123456']]"
]

def sendData(sendstr,commandId):
    HEAD_0 = chr(127)
    HEAD_1 = chr(12)
    HEAD_2 = chr(24)
    HEAD_3 = chr(22)
    ProtoVersion = chr(65)
    ServerVersion = 1
    sendstr = sendstr
    data = struct.pack('!sssss3I',HEAD_0,HEAD_1,HEAD_2,\
                       HEAD_3,ProtoVersion,ServerVersion,\
                       len(sendstr)+4,commandId)
    senddata = data+sendstr #wtx：最终发送过去的数据是：固定格式的包头+数据本身
    return senddata

def resolveRecvdata(data):
    head = struct.unpack('!sssss3I',data[:17])
    lenght = head[6]
    #logging.debug('resolveRecvdata length= %s', lenght)
    data = data[17:17+lenght]
    data = data.split("(end)")[0]
    return data

s1 = time.time()
def send(data, num):
    client.sendall(sendData(data,num))

def start():
    #1.
    loginMsg = TEST_USERS[CURRENTUSER] #wtx：第1个用户
    send(loginMsg, LOGIN)
    #2.用户登录之后，开启线程：保持心跳
    timer = threading.Timer(1,sendHeartBeat)
    timer.start()
    #3.开启线程，用于接收返回的信息
    cycleThread = threading.Thread(target=startCycle)
    cycleThread.start()


def sendHeartBeat():
    heartBeatMsg = "[2]"  # 用于保持心跳的数据格式
    send(heartBeatMsg, TIMER)
    global timer
    timer = threading.Timer(5,sendHeartBeat)
    timer.start()

#start()

def startCycle():
    print 'thread name=',threading.current_thread().name
    while True:
        message = client.recv(1024)#接收服务器返回的消息
        message = resolveRecvdata(message)#解析消息，此时返回的message对象是string类型
        message = eval(message) #将message对象由string类型转化成dict类型
        print message
        logging.debug(u'message = %s', message)



#wtx-start:20170212:上面的代码实现功能：1.启动登录 2.保持心跳
loginMessage = "" # 登录格式："[1,[6326, 'ddd33', '0B1026A8FA261407426E6CC90D2F0845']]"
dealMsg = "[4,[]]" # 发牌格式："[4,[]]"
heartMsg = "[2]" # 保持心跳格式： "[2]"
joinGameMsg = "[2,[5,1]]" # 请求游戏队列格式： "[2,[5,1]]"
quitGameMsg = "[2,[7,1]]" # 退出游戏队列： "[2,[7,1]]"
qdzMsg = "[2,[1,3]]" # 抢地主格式："[2,[1,"+ point +"]]"
unqdzMsg = "[2,[2]]" # 不抢地主给： "[2,[2]]"
pukeMsg = "[2,[3,s5]]" # 用户出牌格式： "[2,[3, "+ str +"]]"
unpukeMsg = "[2,[4]]" # 用户不出牌格式： "[2,[4]]"


def userCommand():
    print 'thread name=', threading.current_thread().name
    while True:
        cmd = raw_input("请输入命令：\n 1-start() \n 2-joinGame() \n 3-qdz() \n 4-unqdz() \n 5-quitGame \n")
        if( cmd == '1'):
            print "start"
            start()
        elif ( cmd == '2'):
            print "joinGame"
            joinGame()
        elif( cmd == '3'):
            print "QDZ"
            qdz()
        elif(cmd == '4'):
            print "unQDZ"
            unqdz()
        elif(cmd == '5'):
            print 'quitGame'
            quitGame()


def joinGame(): #登录之后，请求
    send(joinGameMsg, HANDLE)

def qdz(): # 抢地主
    send(qdzMsg, HANDLE)

def unqdz(): # 不抢地主
    send(unqdzMsg, HANDLE)

def startHeart(): #开始心跳
    print "start heart beat"
    #timer.start()

def stopHeart(): #停止心跳
    print "stop heart beat"
    #timer.stop()

def deal(): #请求发牌
    send(dealMsg,DEAL)

def puke(): # 用户出牌
    send(pukeMsg,HANDLE)

def unpuke(): # 用户跳过出牌：不出
    send(unpukeMsg,HANDLE)

def quitGame():
    send(quitGameMsg,HANDLE)

#开启新线程，用于发送不同的命令：登录，抢地主，出牌，不出牌等等
pukeThread = threading.Thread(target=userCommand)
pukeThread.start()