#coding:utf8
from app.timer import initapp
from firefly.server.globalobject import GlobalObject
GlobalObject().root.service._runstyle=2#多线程方式启动

initapp.initmain()