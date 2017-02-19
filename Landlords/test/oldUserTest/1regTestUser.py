#coding:utf8

import time,threading,random,json

from socket import AF_INET,SOCK_STREAM,socket
from thread import start_new
import struct,sys
HOST='13.113.30.58'
PORT=843
BUFSIZE=1024
ADDR=(HOST , PORT)
# 指令类型
REG = 666 #wtx定义，请求注册测试用户
#新建socket连接
client = socket(AF_INET,SOCK_STREAM)
client.connect(ADDR)

TEST_USERS = [
"[1,[3, 'aaaaa1', '123456']]",
"[1,[4, 'aaaaa2', '123456']]",
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
    random_number = random.randint(0,len(TEST_USERS)-1) #
    loginMsg =TEST_USERS[random_number] #loginMsg实际没有任何用处，就是一个字符串而已
    send(loginMsg, REG) #REG是wtx定义的，用于注册测试用户的接口。接口测试完成之后，会用于用户注册。

start()
#for i in range(10):
#    start_new(start,())
while True:
    message = client.recv(1024)#接收服务器返回的消息
    message = resolveRecvdata(message)#解析消息，此时返回的message对象是string类型
    message = eval(message) #将message对象由string类型转化成dict类型
    status = message['s'] #状态
    return_msg = message['m'] #返回信息
    print eval("u'%s'" %(return_msg))
