#coding:utf8
import time,sys
reload(sys)
sys.setdefaultencoding('utf-8') 
import time

from socket import AF_INET,SOCK_STREAM,socket
import thread
import struct
HOST='localhost'
PORT=10000
BUFSIZE=1024
ADDR=(HOST , PORT)
client = socket(AF_INET,SOCK_STREAM)
client.connect(ADDR)

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
    senddata = data+sendstr
    return senddata

def resolveRecvdata(data):
    head = struct.unpack('!sssss3I',data[:17])
    lenght = head[6]
    data = data[17:17+lenght]
    return data

s1 = time.time()

def start():
    client.sendall(sendData("[1,[1,'ddd33', '18C1BD9C7223FAF46CCCBD2D70942951']]",1))

def send_4():
    time.sleep(4)
    client.sendall(sendData("[1]",4))

start()
thread.start_new_thread(send_4,())

while True:
    message = client.recv(1024)#接收服务器返回的消息
    message = resolveRecvdata(message)#解析消息
    print message.decode('utf-8').encode('gbk')

