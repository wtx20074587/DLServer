# -*- coding: utf8 -*-
import socket, sys
import struct
from thread import start_new

reload(sys)
sys.setdefaultencoding('utf8')
wtxdebug = True


def sendData(sendstr, commandId):
    '''定义协议头
    sendstr —— 发送的数据
    commandId —— 服务器接收信息的端口
    '''
    HEAD_0 = chr(0)
    HEAD_1 = chr(0)
    HEAD_2 = chr(0)
    HEAD_3 = chr(0)
    ProtoVersion = chr(0)  # char类型，1个字节。
    ServerVersion = 0
    sendstr = sendstr  # 这是发送的消息
    data = struct.pack('!sssss3I', HEAD_0, HEAD_1, HEAD_2, \
                       HEAD_3, ProtoVersion, ServerVersion, \
                       len(sendstr) + 4, commandId)  # 注意头部：s是1个字节；I是4个字节。共计：count=5*1+3*4=17个字节。
    senddata = data + sendstr

    return senddata


def resolveRecvdata(data):
    '''解析数据，根据定义的协议头解析服务器返回的数据
    '''
    head = struct.unpack('!sssss3I', data[:17])
    lenght = head[6]  # 由于前5个字段都是char类型，即前5个都是1个字节。因此从第6个字节开始，是int类型。取出长度。
    message = data[17:17 + lenght]
    message = message.split('|<2s|')[0]

    return message


def signIn(connection):
    print 'We will sign in'
    data = "[1,[3, 'cccccc', '123456']]"
    connection.sendall(sendData(data, 1))  # 向服务器发消息
    print 'Loding...wait for a later.'


def sendMessage(connection, returnLogin):
    '''发送消息
    '''
    while 1:
        if (wtxdebug):
            print 'wtx sendMessage'
        data = raw_input()
        if data == '':
            continue
        length = len(data)
        if length > 80:
            length = 80
        line = length * '-'
        data += '\\r\\n' + line

        print "data ="
        print data
        try:
            # print returnLogin
            data = "[" + str(returnLogin['user_id']) + ",'" + str(returnLogin['user_name']) + "','" + str(
                returnLogin['userkey']) + "', '" + data + "']"
        except Exception, e:
            print u"登陆签名错误，用户退出"
            return

        connection.sendall(sendData(data, 2))  # 向服务器发送消息，注意10001，对接server.py
        print line


def checkMessage(connection):
    '''接收检查消息
    '''
    messageData = ''
    while 1:
        message = connection.recv(1024)  # 接收服务器返回的消息(阻塞读到1024个字节时超时)
        message = resolveRecvdata(message)  # 解析消息
        return message


def receiveMessage(connection):
    '''接收消息
    '''
    while 1:
        message = connection.recv(1024)  # 接收服务器返回的消息(读到1024个字节时阻塞)
        message = resolveRecvdata(message)  # 解析消息
        message = str(message)
        if message != '':
            try:
                message = eval(message)
                if message['status'] != 1:
                    print u'系统错误，错误代码：' + str(message['status']) + u'\n错误原因：' + unicode(message['msg'].decode("gbk"))
                    return
                else:
                    print unicode(message['msg'].decode("gbk"))  # 输出消息
            except Exception, e:
                print u'系统错误，返回值数据格式错误，你可以自定义一个错误代码，方便自己查看，其余的错误可以看返回值Status'
                return

                # print message


class ChatServer:
    '''
    1.__init__ : 新建一个传递聊天内容的socket连接
    2.run : 使用self.srvsock对象，连接2个方法：sendMessage和receiveMessage，进行聊天信息的传递。
    '''

    def __init__(self, port, returnLogin):
        self.port = port;
        self.returnLogin = returnLogin
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.connect(('52.199.191.77', port))  # localhost也是服务器端地址，部署之后，就需要修改了。

    def run(self):
        start_new(sendMessage, (self.srvsock, self.returnLogin,))  ## wtx 这里的sendMessage和receiveMessage
        start_new(receiveMessage, (self.srvsock,))  ## wtx 使用的都是同一个self.srvsock，是在生成ChatServer对象时新生成的。


class LoginServer:
    '''
    1.__init__ : 新建一个socket连接，进行登录信息的验证，连接端口：见config.json文件中的，LoginServer的端口号。
    2. run : 注意run方法中的signIn和checkMessage方法。其中：
        signIn方法会登录LoginServer，然后返回一些信息。（说是返回，但是方法调用上是自己请求的）
        checkMessage就是接受同一个socket连接返回的信息，检查是否已经登录。
        当验证登录成功之后，开启聊天服务器。

        关于ChatServer：
        （1）
    '''

    def __init__(self, port):
        self.port = port;
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # wtx socket编程，需要继续看下。这里相当于新建一个连接。
        self.srvsock.connect(('52.199.191.77', port))  # 服务器部署之后，就要是远程的网址，最好使用系统变量定义这个接口。

    def run(self):
        if (wtxdebug):
            print 'wtx LoginServer : run'
        signIn(self.srvsock)  # self.srvsock是一个新连接，将这个连接作为参数传给signin。
        returnLogin = checkMessage(self.srvsock)  ## wtx注意：这里调用signIn之后，self.srvsock相当于“桥梁”
        print 'returnLogin'
        print returnLogin

        returnLogin = str(returnLogin)

        if returnLogin == '':
            print u'系统错误，返回值为空，你可以自定义一个错误代码，方便自己查看，其余的错误可以看返回值Status'
            return self.run()  # 由于python尾递归的关系，这个方法肯定是不行的，不过flash用其他方法即可
        try:
            returnLogin = eval(returnLogin)
        except Exception, e:
            print u'系统错误，返回值数据格式错误，你可以自定义一个错误代码，方便自己查看，其余的错误可以看返回值Status'
            return self.run()
        if returnLogin['status'] != 1:
            print u'系统错误，错误代码：' + str(returnLogin['status']) + u'\n错误原因：' + unicode(returnLogin['msg'].decode("gbk"))
            return self.run()
        else:
            print u'欢迎回来，亲爱的：%s\r\n' % unicode(str(returnLogin['user_name']).decode("gbk"))
            # 运行聊天窗口
            chatServer = ChatServer(11000, returnLogin).run()  # ChatServer的port为1000。注意config.json中。端口号也是客户端需要牢记的!


if __name__ == '__main__':
    loginServer = LoginServer(10000).run()  # 一开始由于端口被占用，因此使用了数值更大的端口（在原端口名称前面+1），端口也是客户端需要牢记的！！
    while 1:
        pass