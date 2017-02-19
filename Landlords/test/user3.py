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
                filename='u3.log',
                filemode='w')
# 基本参数
HOST='13.113.30.58'
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
    cycleThread.join()

def startCycle():
    print 'thread name=',threading.current_thread().name
    while True:
        message = client.recv(1024)#接收服务器返回的消息
        message = resolveRecvdata(message)#解析消息，此时返回的message对象是string类型
        message = eval(message) #将message对象由string类型转化成dict类型
        #print message
        #logging.debug(u'message = %s', message)
        if message['s'] > 0:
            autoStart(message)


def autoStart(message):
    currentpuke = []
    currentUser = ''
    amIDzUser = False
    theLast3pukes = ''
    errormsg = 'There is an error here.'

    s = message['s']
    if s == 1:#Correct Status
        try:
            c = message['c']
            if c==1001:#(1)用户请求加入游戏队列之后：加入游戏队列成功 —— ps：相当于点击“准备”，之后返回该信息，说明准备成功(2)其他情况：该信号有重叠
                logging.debug('加入游戏队列成功'+message)
                if message['d'] != False:
                    logging.debug('获取用户信息成功'+message['d'])
            elif c == 1002:#用户离开游戏队列 —— ps：相当于点击 “取消准备”，之后返回该信息，说明退出成功
                logging.debug('离开游戏队列成功'+message)
            elif c == 1000:
                #1.系统发牌成功，先将各自的牌（或数量）取出来
                f_p = message['f_p'] #如果当前用户就是f_p,那么f_p就是系统发给他牌，相应的：s_p,t_p就是另外2个用户的牌的数量了。d就是地主牌的数量
                s_p = message['s_p']
                t_p = message['t_p']
                d = message['d']
                if isinstance(f_p,list):
                    currentpuke = f_p
                    currentUser = 'f_p'
                if isinstance(s_p,list):
                    currentpuke = s_p
                    currentUser = 's_p'
                if isinstance(t_p,list):
                    currentpuke = t_p
                    currentUser = 't_p'

                print 'currentpuke=',currentpuke,'currentUser=',currentUser
                #2.首先提前判断下自己会不会“优先”抢地主：
                if 's5' in currentpuke:
                    amIDzUser = True
                    print '\n\n 哈哈哈 我是地主  \n\n'
                else:
                    print '我不是地主'
            elif c == 2000: #系统开启抢地主
                #{'s':1, 'c':2000, 'p':XXX}
                whichOneShouldRespond = message['p']
                if whichOneShouldRespond == currentUser: # 1.PS:此时才是真正的开始抢地主哦。
                    amIDzUser = True
                #2.（1）优先抢地主用户设置倒计时30s，然后决定是否抢地主，30s后，默认不抢地主（2）非优先抢地主用户也会收到该信息，“观看”优先抢地主用户抢地主
                print '谁先抢地主呢？！！user=',whichOneShouldRespond,'currentUser=',currentUser
                if whichOneShouldRespond == False: #这里不确定，如果没人抢地主，没有'p'字段
                    logging.debug("没人抢地主"+message)
                #3.开始抢地主
                if amIDzUser == True:
                    print ' \n\n   我是地主，抢起来！！！！  \n\n'
                    qdz()
                else:
                    print ' \n\n   我不是地主，不抢   \n\n'
                    unqdz()

            elif c == 2001: #没人抢地主，重新发牌
                #{'s':1, 'c':2001, 'f_p':pukeList[0],'s_p':17,'t_p':17,'d_z':3}
                #1.重新发牌，做个动画吧
                currentpuke = message[currentUser] #取出当前用户的牌。其他用户的牌就不取出来了。
                logging.debug("没人抢地主，重新发牌.,message="+message)
            elif c == 2002:
                #{'s':1, 'c':2002, 'd_z':isInGame['d_z'].split(','),'dz_u':'XXXX'} #该用户会收到自己的信息
                theLast3pukes = message['d_z'] # 如果当前用户不是地主，那么只会看到最后的3张地主牌
                print '3张地主牌是：',theLast3pukes,'地主用户是：',message['dz_u']
                #1.如果是地主用户，此时可以开始了么？
                logging.debug("选出地主来啦：地主是"+message['dz_u']+" ,message="+message)
            elif c == 2003: #只有地主用户才能收到2003的消息：
                #{'s':1,'c':2003,'p':t_p.split(',')}
                currentpuke = message['p'] # 该用户是地主，最后的3张地主牌，已经混合了原来的17张牌。共计20张牌给地主。
                print "我就是地主，地主就是我，我的牌是：",currentpuke
                print "\n\n先出一张牌！\n\n"
                if len(currentpuke)>0:
                    onepuke = currentpuke[0]
                    puke(onepuke)
                    currentpuke.remove(currentpuke[0])

            elif c == 2004: #用户x不抢地主
                # {'s': 1, 'c': 2004, 'n_u': nowUser}
                nowUser = message['n_u']
                print '用户：'+nowUser+' 就是不NOOOO去抢地主！\n\n'

            elif c == 2010:#报警数据，某个用户的牌剩余不到2张
                #{'s':1,'m':'还剩'+str(len(upd_puke))+'张牌了','n':nowUser,'c':2010,'mp3':'clock.mp3'}
                warningMsg = message['m']
                nowUser = message['n']
                print 'User:'+nowUser+'  '+warningMsg
                logging.debug("我快出完啦!!,message="+message)

            elif c == 2011:#用户的出牌数据
                #{'s':1,'p':puke,'n':nowUser, 'c':2011,'next':nextUser, 'mp3':music}
                #{'s':1,'p':'','n':nowUser, 'c':2011,'next':nextU, 'mp3':'NO'+str(random.randint(1,4))+'.mp3'}
                nowUser = message['n']
                p = message['p']
                nextUser = message['next']
                music = message['mp3']
                print "用户："+nowUser+" 出牌："+p+", 下一个出牌用户是："+nextUser+", 播放对应的音乐："+music
                print "当前用户是：",currentUser
                logging.debug("用户："+nowUser+" 出牌："+p+", 下一个出牌用户是："+nextUser+", 播放对应的音乐："+music +" message="+message)
                #1.判断是不是自己出牌：
                if nextUser == currentUser:
                    #(1)如果自己是地主，出一张牌
                    if amIDzUser == True:
                        # def pukeOne()
                        if currentpuke!=None and len(currentpuke)>0:
                            onePuke = currentpuke[0]
                            puke(onePuke)
                            currentpuke.remove(currentpuke[0])
                    #（2）自己不是地主，所以就不出牌了
                    else :
                        unpuke()
                #2.如果没轮到自己出牌，就看别人出吧
            elif c == 2012: #一盘结束，计算最终的结果，返回给用户
                #PS:默认的初始化用户好像都没钱！
                #{'s':1,'m':'游戏已结束','c':2012,'w':winS,'l':losS,'d':upset,'losemoney':losMoney,'winmoney':winMoney}
                winners = message['w']
                losers = message['l']
                loseMoney = message['losemoney']
                winMoney = message['winmoney']
                upset = message['d']
                print '游戏结束啦！ 赢的用户是：'+winners +"赢了："+winMoney+" 输了用户是："+losers+"输了："+loseMoney
                logging.debug( '游戏结束啦！ 赢的用户是：'+winners +"赢了："+winMoney+" 输了用户是："+losers+"输了："+loseMoney+'message='+message)

            elif c == 2013:#某个用户不出牌
                #unOutDict = {'s':1,'c':2013, 'p':nowUser}
                nowUser = message['p']
                print "用户："+nowUser+"发话了，我就是不要!"

            elif c== 2016:#游戏结束
                m = message['m']
                print "游戏结束啦！！m=",m
                logging.debug("游戏结束啦！message="+message)
        except:
            logging.debug('errormsg')
    elif s != 1:#Wrong Status
        try:
            c = message['c']
            if c==2005 or c == 2006:
                logging.debug("抢地主失败,message="+message)
                print '抢地主失败'
            elif c == 2007:
                logging.debug("不抢地主失败,message="+message)
                print '不抢地主失败'
            elif c == 2008 or c == 2009:
                logging.debug("出牌失败,message="+message)
                print '出牌失败'
            elif c == 2014 or c == 2015 or c == 2016 or c == 2017:
                logging.debug("不出牌失败,message="+message)
                print '不出牌失败'
        except:
            logging.debug('errormsg')



start() #运行后直接自动开始

