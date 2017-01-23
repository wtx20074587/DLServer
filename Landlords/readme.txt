#coding:utf8
该项目是一个半完整的项目，需要继续完善。该项目的说明文档见：doc/firefly整理.pdf

一、目录结构（使用tree命令生成）及文件作用说明
Landlords/
├── 127.0.0.1-3306.sql #创建测试数据库和表的sql文件
├── app
│   ├── __init__.py
│   ├── cross.py
│   ├── gate
│   │   ├── __init__.py
│   │   ├── initapp.py
│   ├── gateServer.py
│   ├── net
│   │   ├── __init__.py
│   │   ├── initapp.py
│   │   └── plub
│   │       ├── __init__.py
│   │       ├── console.py
│   │       ├── login.py
│   │       ├── methodcallback.py
│   │       ├── setheart.py
│   ├── netServer.py
│   ├── timer
│   │   ├── __init__.py
│   │   ├── initapp.py
│   │   └── plub
│   │       ├── __init__.py
│   │       ├── service.py
│   ├── timerServer.py
├── appmain.py
├── config.json # firefly启动时，各种配置属性都取自该文件。例如："db"属性设置数据库的登录密码，当在服务器电脑上安装mysql时，设置的mysql密码就需要配置到这里，不然就不能登录mysql
├── database
│   ├── Land-main.sql
│   └── user_data.sql
├── doc
│   ├── Database.pdb  # PowerDesigner是用来帮助用户定义数据库（库，表）的软件（http://www.cr173.com/soft/23650.html）。
│   ├── Database.pdm
│   ├── firefly整理.pdf   #该项目的主要说明文档
│   └── 斗地主通信接口文档.docx  #server与client之间，通信变量的说明。
├── filecache
│   └── room.json
├── models
│   ├── __init__.py
│   ├── gameMainModel.py
│   ├── sysModel.py
│   ├── userModel.py
├── readme.txt
├── service
│   └── room.py
├── startmaster.py
├── tool
│   ├── __init__.py
│   ├── 1.py
│   ├── 2.py
│   ├── 3.py
│   ├── clienttest.py
│   ├── t.py
│   └── t1.py
└── 牌面大小比对.json  #单张牌的大小（数值越大，牌越大）。例如："h8": 6 — 红桃8，大小为6 ；"fQ": 10 — 梅花Q，大小为10；"P2": 14 — 小王，大小为14
