#coding:utf8
import socket,os
from firefly.server.globalobject import GlobalObject

#GlobalObject().root.service._runstyle=2#多线程方式

cross_data = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy> 
	<allow-access-from domain="*" to-ports="*" />
</cross-domain-policy>'''
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#s=socket.socket()
#s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#s.setsockopt(socket.SOL_SOCKET,SO_LINGER,pack('ii',0,0))
s.bind(('0.0.0.0',843))   #注意，bind函数的参数只有一个，是（host,port）的元组
s.listen(1000)

while True:
	try:
		client,ipaddr=s.accept()
		print "Got a connect from %s"  %str(ipaddr)
		data=client.recv(1024)
		#print "receive data:%s" %data
		client.send(cross_data)
		client.close()
	except Exception, e:
		continue