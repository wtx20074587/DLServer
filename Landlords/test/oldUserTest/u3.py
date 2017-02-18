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
                filename='user3.log',
                filemode='w')
# 基本参数
HOST='52.199.191.77'
PORT=843
BUFSIZE=1024
ADDR=(HOST , PORT)
CURRENTUSER = 3
TIMERGAP = 10
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

loginMsg = TEST_USERS[CURRENTUSER] # 登录格式："[1,[6326, 'ddd33', '0B1026A8FA261407426E6CC90D2F0845']]"
heartBeatMsg = "[2]"
dealMsg = "[4,[]]" # 发牌格式："[4,[]]"
heartMsg = "[2]" # 保持心跳格式： "[2]"
joinGameMsg = "[2,[5,1]]" # 请求游戏队列格式： "[2,[5,1]]"
quitGameMsg = "[2,[7,1]]" # 退出游戏队列： "[2,[7,1]]"
qdzMsg = "[2,[1,3]]" # 抢地主格式："[2,[1,"+ point +"]]"
unqdzMsg = "[2,[2]]" # 不抢地主给： "[2,[2]]"
#pukeMsg = "[2,[3,s5]]" # 用户出牌格式： "[2,[3, "+ str +"]]"
unpukeMsg = "[2,[4]]" # 用户不出牌格式： "[2,[4]]"

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
    data = data[17:17+lenght]
    data = data.split("(end)")[0]
    return data

s1 = time.time()
def send(data, num):
    client.sendall(sendData(data,num))

def sendHeartBeat():
    print 'sendHeart'
    send(heartBeatMsg, TIMER)
    global timer
    timer = threading.Timer(TIMERGAP,sendHeartBeat)
    timer.start()

def login():
    send(loginMsg,LOGIN)

def joinGame(): #登录之后，请求
    send(joinGameMsg, HANDLE)

def qdz(): # 抢地主
    print 'qdz'
    send(qdzMsg, HANDLE)

def unqdz(): # 不抢地主
    print 'unqdz'
    send(unqdzMsg, HANDLE)

def startHeart(): #开始心跳
    print "start heart beat"
    #timer.start()

def stopHeart(): #停止心跳
    print "stop heart beat"
    #timer.stop()

def deal(): #请求发牌
    send(dealMsg,DEAL)

def puke(aPuke): # 用户出牌
    '''
    :param aPuke:这是一个字符串
    :return: ！！！！！这个非常重要！！！！！
    pukeMsg 一定是一个能被json转换成python对象的str类型。比如：传递python的list类型，需要先转换成str，然后服务器接收之后，再将str转化成list对象。
    '''
    #pukeMsg = "[2,[3,'"+ str(aPuke) +"']]" #wtx:这种方式是错误的！正确的方法见下面
    pukeMsg = [2,[3,str(aPuke)]]
    pukeMsg = json.dumps(pukeMsg)
    print "puke, pukeMsg=",pukeMsg
    send(pukeMsg,HANDLE)

def unpuke(): # 用户跳过出牌：不出
    print 'unpuke'
    send(unpukeMsg,HANDLE)

def quitGame():
    send(quitGameMsg,HANDLE)

def start():
    #1.用户登录
    login()
    #2.用户登录之后，开启线程：保持心跳
    #timer = threading.Timer(1,sendHeartBeat)
    #timer.start()
    sendHeartBeat()
    #3.发送“准备”好信息
    joinGame()
    #4.开启线程，用于接收返回的信息
    cycleThread = threading.Thread(target=startCycle)
    cycleThread.start()

def startCycle():
    print 'thread name=',threading.current_thread().name
    while True:
        message = client.recv(1024)#接收服务器返回的消息
        message = resolveRecvdata(message)#解析消息，此时返回的message对象是string类型
        message = eval(message) #将message对象由string类型转化成dict类型
        print message
        logging.debug(u'message = %s', message)

        if message['s'] > 0:
            autoStart(message)

def autoStart(message):
    currentpuke = []
    currentUser = ''
    amIDzUser = False
    try:
        print 'puking, c=',message['c']
        if message['c'] == 1000 : #1000 ：表示服务器向玩家发牌
            f_p = message['f_p']
            s_p = message['s_p']
            t_p = message['t_p']
            # 1.先把当前用户的牌取出来，看是否含有s5
            if isinstance(f_p, list):
                currentpuke = f_p #取出当前用户的牌，和当前用户的"用户名"
                currentUser = 'f_p'
            if isinstance(s_p, list):
                currentpuke = s_p
                currentUser = 's_p'
            if isinstance(t_p, list):
                currentpuke = t_p
                currentUser = 't_p'
            # 2.如果含有s5，当前用户就是地主；否则不是地主。之后：地主响应出牌 非地主：收到别人出牌信息后，响应不出牌
            if 's5' in currentpuke:
                amIDzUser = True
                qdz() #只让摸到红桃5的人抢地主
            else:
                amIDzUser = False
                unqdz()#其他人都不抢地主
            print 'CURRENTUSER=',currentUser
        elif message['c'] == 2000:#系统分配带有s5的用户首先响应抢地主：那么：（1）当前已经收到牌了，所以认为包含s5的就是地主（2）当前用户（系统后台写pid，client端写p）
            sysUser = message['p']
            print 'sysUser=',sysUser,'currentUser=',currentUser
            if amIDzUser == True:
                qdz()
            elif amIDzUser == False:
                unqdz()
        elif message['c'] == 2002:
            theLast3Pukes = message['p']
            print '最后的3张牌',theLast3Pukes
        elif message['c'] == 2003:#抢地主成功，更新地主牌
            currentpuke = message['p']
            print '9999999999999999 currentp=',currentpuke
            #然后先出一张牌，让游戏进入循环：不然不会收到2011数据
            puke(currentpuke[0])
            currentpuke.remove(currentpuke[0])
        elif message['c'] == 2011:#收到出牌的提醒
            #1.首先判断是不是自己出牌
            print 'message[NEXT]=',message['next'],'currentUser=',currentUser
            if message['next'] == currentUser:
                if amIDzUser == True:
                    if len(currentpuke) > 0:  # we have more than 1 puke
                        puke(currentpuke[0])
                        currentpuke.remove(currentpuke[0])
                else:
                    unpuke()
    except:
        print 'wtx error'


start() #运行后直接自动开始

'''
#开启新线程，用于发送不同的命令：登录，抢地主，出牌，不出牌等等
    def userCommand():
        print 'thread name=', threading.current_thread().name
        while True:
            cmd = raw_input("请输入命令：\n 1-start() \n 2-joinGame() \n 3-qdz() \n 4-unqdz() \n 5-quitGame \n")
            if (cmd == '1'):
                print "start"
                start()
            elif (cmd == '2'):
                print "joinGame"
                joinGame()
            elif (cmd == '3'):
                print "QDZ"
                qdz()
            elif (cmd == '4'):
                print "unQDZ"
                unqdz()
            elif (cmd == '5'):
                print 'quitGame'
                quitGame()
#pukeThread = threading.Thread(target=userCommand)
#pukeThread.start()
'''