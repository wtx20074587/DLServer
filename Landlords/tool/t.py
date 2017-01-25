#coding:utf8

import time,threading

from socket import AF_INET,SOCK_STREAM,socket
from thread import start_new
import struct,sys
HOST='52.199.191.77'
PORT=10000
BUFSIZE=1024
ADDR=(HOST , PORT)
client = socket(AF_INET,SOCK_STREAM)
client.connect(ADDR)

def sendData(sendstr,commandId):
    HEAD_0 = chr(0)
    HEAD_1 = chr(0)
    HEAD_2 = chr(0)
    HEAD_3 = chr(0)
    ProtoVersion = chr(0)
    ServerVersion = 0
    sendstr = sendstr
    data = struct.pack('!sssss3I',HEAD_0,HEAD_1,HEAD_2,\
                       HEAD_3,ProtoVersion,ServerVersion,\
                       len(sendstr)+4,commandId)
    senddata = data+sendstr #wtx：最终的打包方式，打包头+数据
    return senddata

def resolveRecvdata(data):
    head = struct.unpack('!sssss3I',data[:17])
    lenght = head[6]
    data = data[17:17+lenght]
    return data

s1 = time.time()
def send(data, num):
    client.sendall(sendData(data,num))

def start():
    send('as', 1)
start()
#for i in range(10):
#    start_new(start,())
while True:
    message = client.recv(1024)#接收服务器返回的消息
    message = resolveRecvdata(message)#解析消息
    print message.decode('utf-8').encode('gbk')
