#coding:utf8
import time,sys,json
reload(sys)
sys.setdefaultencoding('utf-8') 
import time

from socket import AF_INET,SOCK_STREAM,socket
import thread
import struct
HOST='52.199.191.77'
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
    listData = data.split('(end)')
    returnData  = []
    for x in listData:
        returnData.append(x[17:])
    #return json.dumps(returnData)
    return returnData

s1 = time.time()

def start():
    client.sendall(sendData("[1,[2,'ddd44', 'D4A8033EE07F6DFB3A9F290752CD5B04']]",1))

def send_4():
    time.sleep(4)
    client.sendall(sendData("[2,[5,1]]",3))

def un_q():
    client.sendall(sendData("[2,[1,2]]",3))
def chu_pai():
    client.sendall(sendData("[2,[3,'h10']]",3))

def send_heart():
    while True:
        time.sleep(30)
        client.sendall(sendData("[1]",2))

start()
thread.start_new_thread(send_4,())
thread.start_new_thread(send_heart,())

while True:
    message = client.recv(1024)#接收服务器返回的消息
    message = resolveRecvdata(message)#解析消息
    for x in message:
        if x!='':
            try:
                x = json.loads(x)
                if x['s']<-1:
                    print unicode(x['m'])
                if x['c']==1000:
                    if x['f_p']!=17:
                        d_z='f_u'
                    if x['s_p']!=17:
                        d_z='s_u'
                    if x['t_p']!=17:
                        d_z='t_u'
                if x['c']==2000:
                    if x['p']==d_z:
                        time.sleep(3)
                        thread.start_new_thread(un_q,())
                if x['c']==2003:
                    thread.start_new_thread(chu_pai,())
            except Exception, e:
                print x
    print message

