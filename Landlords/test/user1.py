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
                filename='user1.log',
                filemode='w')
# 基本参数
HOST='52.199.191.77'
PORT=843
BUFSIZE=1024
ADDR=(HOST , PORT)
CURRENTUSER = 1
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
    theLast3pukes = ''
    errormsg = 'There is an error here.'
    '''
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
    '''
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

                #2.首先提前判断下自己会不会“优先”抢地主：
                if 's5' in currentpuke:
                    amIDzUser = True
            elif c == 2000: #系统开启抢地主
                #{'s':1, 'c':2000, 'p':XXX}
                whichOneShouldRespond = message['p']
                if whichOneShouldRespond == currentUser: # 1.PS:此时才是真正的开始抢地主哦。
                    amIDzUser = True
                #2.（1）优先抢地主用户设置倒计时30s，然后决定是否抢地主，30s后，默认不抢地主（2）非优先抢地主用户也会收到该信息，“观看”优先抢地主用户抢地主

                if whichOneShouldRespond == False: #这里不确定，如果没人抢地主，没有'p'字段
                    logging.debug("没人抢地主"+message)
                #3.开始抢地主
                if amIDzUser == True:
                    qdz()
                else:
                    unqdz()

            elif c == 2001: #没人抢地主，重新发牌
                #{'s':1, 'c':2001, 'f_p':pukeList[0],'s_p':17,'t_p':17,'d_z':3}
                #1.重新发牌，做个动画吧
                currentpuke = message[currentUser] #取出当前用户的牌。其他用户的牌就不取出来了。

            elif c == 2002:
                #{'s':1, 'c':2002, 'd_z':isInGame['d_z'].split(','),'dz_u':'XXXX'} #该用户会收到自己的信息
                if amIDzUser == True:
                    currentpuke = message['d_z'] # 如果该用户是地主，那么最后的3张地主牌，已经混合了原来的17张牌。共计20张牌给地主。
                else:
                    theLast3pukes = message['d_z'] # 如果当前用户不是地主，那么只会看到最后的3张地主牌
                #1.如果是地主用户，此时可以开始了么？

            elif c ==



            '''
						case 2002://是抢地主完成，并获取地主用户的牌数d_z地主牌，dz_u:地主。
							GameView.getInstance().poker.onShow(o.d_z);
							if(GameView.getInstance().user.postion != o.dz_u)//排除地主是自己。是自己执行2003里面的方法
							{
								if(GameView.getInstance().enemy_1.postion == o.dz_u)
								{
									GameView.getInstance().enemy_1.pokerContainer.addPoker(3);
									GameView.getInstance().RoleShow();
									GameView.getInstance().roleList[0].gotoAndStop(1);
									GameView.getInstance().roleList[1].gotoAndStop(2);
									GameView.getInstance().roleList[2].gotoAndStop(2);
								}
								else
								{
									GameView.getInstance().enemy_2.pokerContainer.addPoker(3);
									GameView.getInstance().RoleShow();
									GameView.getInstance().roleList[0].gotoAndStop(2);
									GameView.getInstance().roleList[1].gotoAndStop(1);
									GameView.getInstance().roleList[2].gotoAndStop(2);
								}
							}
							//游戏开始
							GameView.getInstance().clock.start(o.dz_u, 30);
							break;
						case 2003://更新当前地主用户的牌组（获取地主牌后的牌组，只要自己是地主时候才收到此消息）
							GameView.getInstance().user.initialize(o.p, null);
							//更新角色图标
							GameView.getInstance().RoleShow();
							GameView.getInstance().roleList[0].gotoAndStop(2);
							GameView.getInstance().roleList[1].gotoAndStop(2);
							GameView.getInstance().roleList[2].gotoAndStop(1);
							GameView.getInstance().clock.start(GameView.getInstance().user.postion, 30);
							GameView.getInstance().updateHandle(GameView.getInstance().user.postion, 2);
							break;
						case 2004://不抢地主(非系统时间到了弃权，是用户自主弃权)
							GameView.getInstance().updateHandle(o.n_u, 3, o.f);
							break;
						case 2010://报警
							trace(o.m);
							arr = o.mp3.split(".");
							SoundEngine.getInstance().playSound(arr[0]);
							switch(o.m)
							{
								case "还剩2张牌了":
									break;
								case "还剩1张牌了":
									break;
							}
							break;
						case 2011://推送数据，告诉客户端该下一个用户出牌了，如果p=''，则表示上家是不出，n=上家，next=该出牌的下家
							if(o.p)//更新牌
							{
								GameView.getInstance().updateChupai(o.n, o.p);
								GameView.getInstance().chupai(o.p);
								//播放mp3
								arr = o.mp3.split(".");
								SoundEngine.getInstance().playSound(arr[0]);
							}//计时器跳入下一个玩家
							GameView.getInstance().clock.start(o.next, 30);
							GameView.getInstance().updateHandle(o.next, 2);
							//播放mp3
							arr = o.mp3.split(".");
							SoundEngine.getInstance().playSound(arr[0]);
							break;
						case 2012://游戏结束了,w=胜利者list数组，l=失败者list数组，d=底价，losemoney=输的金额，winmoney=赢的money
							GameStage.getInstance().gameLayer.addChild(GameEndView.getInstance());

							break;
						case 2013://用户放弃了，p=放弃出牌的用户
							trace(o.p + "放弃出牌");
							break;
						case 2016://游戏结束，返回大厅
							trace("游戏结束");
							GameStage.getInstance().firstLayer.removeChild(GameView.getInstance().res);
							GameStage.getInstance().firstLayer.addChild(HallView.getInstance().res);
							break;
            '''





        except:
            logging.debug('errormsg')
    elif s != 1:#Wrong Status
        try:
            c = message['c']
            if c==2005 or c == 2006:
                logging.debug("抢地主失败"+message)
            elif c == 2007:
                logging.debug("不抢地主失败"+message)
            elif c == 2008 or c == 2009:
                logging.debug("出牌失败"+message)
            elif c == 2014 or c == 2015 or c == 2016 or c == 2017:
                logging.debug("不出牌失败"+message)
        except:
            logging.debug('errormsg')



start() #运行后直接自动开始

