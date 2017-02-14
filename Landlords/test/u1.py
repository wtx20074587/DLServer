#coding:utf8

import time,threading,random,json

from socket import AF_INET,SOCK_STREAM,socket
from thread import start_new
import threading
import struct,sys
HOST='52.199.191.77'
PORT=843
BUFSIZE=1024
ADDR=(HOST , PORT)
# 指令类型
LOGIN = 1 #登录
TIMER = 2 #心跳
HANDLE = 3 #抢地主，强退等
DEAL = 4 #请求发牌

#用于测试
CURRENTUSER = 0
enqueueMsg = "[2,[5,1]]"
qdzMsg = "[2,[1,3]]"
unQdzMsg = "[2,[2]]"


#新建socket连接
client = socket(AF_INET,SOCK_STREAM)
client.connect(ADDR)

TEST_USERS = [
"[1,[3, 'aaaaa1', '123456']]",
"[1,[4, 'aaaaa2', '123456']]",
"[1,[5,'aaaaa3','123456']]",
"[1,[6,'aaaaa4','123456']]",
"[1,[7,'aaaaa5','123456']]",
"[1,[8,'aaaaa6','123456']]"
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
    print lenght
    data = data[17:17+lenght]
    data = data.split("(end)")[0]
    return data

s1 = time.time()
def send(data, num):
    client.sendall(sendData(data,num))

def start():
    #1.随机选取一个用户，然后将该用户登录
    loginMsg = TEST_USERS[CURRENTUSER] #wtx：其实没区别，只用第一个用户登录，测试抢地主和不抢地主
    send(loginMsg, LOGIN)
    #2.用户登录之后，保持心跳
    timer = threading.Timer(1,sendHeartBeat)
    timer.start()

    #qiangDiZhu = "[2,[5,1]]"  # wtx:抢地主的数据格式为："[2,[1,"+ point +"]]"
    #send(qiangDiZhu, HANDLE)  # LOGIN就是对应的commandId：登录专用

def sendHeartBeat():
    heartBeatMsg = "[2]"  # 用于保持心跳的数据格式
    send(heartBeatMsg, TIMER)
    global timer
    timer = threading.Timer(5,sendHeartBeat)
    timer.start()

start()
#for i in range(10):
#    start_new(start,())
def cmd():
    while True:
        command = raw_input('输入命令：1-enQueue 2-QDZ 3-UnQDZ')
        if( cmd == '1'):
            enQueue()
        elif(cmd == '2'):
            qdz()
        elif(cmd == '3'):
            unQdz()

def enQueue():
    send(enqueueMsg, HANDLE)
def qdz():
    send(qdzMsg, HANDLE)
def unQdz():
    send(unQdzMsg, HANDLE)

newThread = threading.Thread(target=cmd)
newThread.start()


while True:
    message = client.recv(1024)#接收服务器返回的消息
    message = resolveRecvdata(message)#解析消息，此时返回的message对象是string类型
    message = eval(message) #将message对象由string类型转化成dict类型
    print message

