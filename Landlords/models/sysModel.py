# -*- coding: utf8 -*-
__version__ = '1.0.0'
__author__ = 'Aeolus(QQ:251920948)'

from firefly.dbentrust.dbpool import dbpool                         	#引入DBUtil在Firefly封装的模块 
from firefly.dbentrust.memclient import mclient 						#引入memcache在Firefly封装的模块
from firefly.dbentrust.memobject import MemObject
from MySQLdb.cursors import DictCursor
import json,sys,os,re,time												#载入一些基础的模块

def getConfig():
	return json.load(open('config.json', 'r'))

def getVersion():
	print 'This sysModel version is: %s\nAuthor is: %s' % (__version__, __author__)

class MysqlObject(object):
	"""
		MysqlObject数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现
		获取连接对象：conn = MysqlObject.getConn()
		释放连接对象;conn.close()或del conn
	"""
	#连接池对象
	__pool = None
	_errorCode = 0
	_errorMsg = []
	def __init__(self):
		"""
		数据库构造函数，从连接池中取出连接，并生成操作游标
		"""
		self.dbConfig = getConfig().get('db')
		self._conn = MysqlObject.__getConn(self)
		self._cursor = MysqlObject.__getCursor(self)

	@staticmethod
	def __getConn(self):
		"""
		@summary: 静态方法，从连接池中取出连接，配置从config中读取
		@return 多库的_conn
		"""
		__conn = {}
		if MysqlObject.__pool is None:
			try:
				for x in self.dbConfig: # self.dbconfig 目前有4个数据库us,lo,mn,ssc
					mainConfig = self.dbConfig.get(x).get('main')				#主数据库
					dbpool.initPool(host = mainConfig['host'], \
							user = mainConfig['user'], \
							passwd = mainConfig['passwd'], \
							port = mainConfig['port'], \
							db = mainConfig['db'], \
							charset = mainConfig['charset'], \
							cursorclass=DictCursor)#,\ # deleted by wtx 20170109
							#charset = mainConfig['charset']) # deleted by wtx 20170109
					__conn.setdefault(x+'_main', dbpool.connection()) # wtx:dbpool是firefly提供的连接池。

					#wtx@20170123@(1)不需要从数据库(2)下面的原代码中使用mainConfig，也就是主从数据库使用同一个数据库
					queryConfig = self.dbConfig.get(x).get('query')				#从数据库
					dbpool.initPool(host = queryConfig['host'], \
							user = queryConfig['user'], \
							passwd = queryConfig['passwd'], \
							port = queryConfig['port'], \
							db = queryConfig['db'], \
							charset = queryConfig['charset'], \
							cursorclass=DictCursor)#,\ # deleted by wtx 20170109
							#charset = mainConfig['charset']) # deleted by wtx 20170109
					__conn[x+'_query'] = dbpool.connection()

			except Exception, e:
				print e,'[{======Mysql connection error......======}]'
				return {}
			self.__pool = True
		return __conn

	@staticmethod
	def __getCursor(self):
		"""
		@summary: 静态方法，从连接池中取出连接并创建游标
		@return 多库的游标
		"""
		_cursor = {}
		try:
			for x in self._conn:
				_cursor.setdefault(x, self._conn[x].cursor())
		except Exception, e:
			print '[{======cursor create error......======}]'
			return {}
		return _cursor

	def getErrorMsg(self):
		"""
		@summary: 返回数据库错误
		@return string
		"""
		if self._errorCode>=0:
			return ''
		return '错误代码：%d，错误原因：%s，%s' % (self._errorCode, self._errorMsg[0], self._errorMsg[1])

	def checkDbPrefix(self, dbPrefix, sql):
		"""
		@summary: 检查数据库前缀及sql语句
		@return boolean
		"""
		if dbPrefix is None or sql is None:
			self._errorCode = -1999
			self._errorMsg = '参数错误'
			return False
		if dbPrefix+'_query' not in self._cursor:
			self._errorCode = -1998
			self._errorMsg = '数据库前缀不存在'
			return False
		return True

	def getAll(self,dbPrefix,sql,param=None):
		"""
		@summary: 执行查询，并取出所有结果集
		@param dbPrefix:数据库前缀
		@param sql:查询sql，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
		@param param: 可选参数，条件列表值（元组/列表）
		@return: result list/boolean 查询到的结果集, 出错时，MysqlObject._errorCode!=1则表示有错误，MysqlObject._errorCode==1表示空集
		"""
		if self.checkDbPrefix(dbPrefix, sql)==False:
			return False
		try:
			if param is None:
				count = self._cursor[dbPrefix+'_query'].execute(sql)
			else:
				count = self._cursor[dbPrefix+'_query'].execute(sql,param)
			if count>0:
				result = self._cursor[dbPrefix+'_query'].fetchall()
			else:
				self._errorCode = 1
				self._errorMsg = '查询不存在'
				result = False
			return result
		except Exception, e:
			self._errorCode = -1997
			self._errorMsg = '查询出错了：',e
			return False

	def getOne(self,dbPrefix,sql,param=None):
		"""
		@summary: 执行查询，并取出第一条
		@param dbPrefix:数据库前缀
		@param sql:查询sql，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
		@param param: 可选参数，条件列表值（元组/列表）
		@return: result list/boolean 查询到的结果集, 出错时，MysqlObject._errorCode!=1则表示有错误，MysqlObject._errorCode==1表示空集
		"""
		if self.checkDbPrefix(dbPrefix, sql)==False:
			return False
		try:
			if param is None:
				count = self._cursor[dbPrefix+'_query'].execute(sql)
			else:
				count = self._cursor[dbPrefix+'_query'].execute(sql,param)
			if count>0:
				result = self._cursor[dbPrefix+'_query'].fetchone()
			else:
				self._errorCode = 1
				self._errorMsg = '查询不存在'
				result = False

			return dict2list(result)
		except Exception, e:
			self._errorCode = -1997
			self._errorMsg = '查询出错了：',e
			return False
	def getOneDict(self,dbPrefix,sql,param=None):
		"""
                @summary: 执行查询，并取出第一条
                @param dbPrefix:数据库前缀
                @param sql:查询sql，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
                @param param: 可选参数，条件列表值（元组/列表）
                @return: result list/boolean 查询到的结果集, 出错时，MysqlObject._errorCode!=1则表示有错误，MysqlObject._errorCode==1表示空集
                """
		if self.checkDbPrefix(dbPrefix, sql) == False:
			return False
		try:
			if param is None:
				count = self._cursor[dbPrefix + '_query'].execute(sql)
			else:
				count = self._cursor[dbPrefix + '_query'].execute(sql, param)
			if count > 0:
				result = self._cursor[dbPrefix + '_query'].fetchone()
			else:
				self._errorCode = 1
				self._errorMsg = '查询不存在'
				result = False

			return result
		except Exception, e:
			self._errorCode = -1997
			self._errorMsg = '查询出错了：', e
			return False

	def getMany(self,dbPrefix,sql,num,param=None):
		"""
		@summary: 执行查询，并取出num条结果
		@param dbPrefix:数据库前缀
		@param sql:查询sql，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
		@param num:取得的结果条数
		@param param: 可选参数，条件列表值（元组/列表）
		@return: result list/boolean 查询到的结果集
		"""
		if self.checkDbPrefix(dbPrefix, sql)==False:
			return False
		try:
			if param is None:
				count = self._cursor[dbPrefix+'_query'].execute(sql)
			else:
				count = self._cursor[dbPrefix+'_query'].execute(sql,param)
			if count>0:
				result = self._cursor[dbPrefix+'_query'].fetchmany(num)
			else:
				result = False

			return dict2list(result)#wtx:数据库查询类型，这里不确定，但是先修改。
		except Exception, e:
			self._errorCode = -1997
			self._errorMsg = '查询出错了：',e
			return False

	def insertOne(self,dbPrefix,sql,value,returnType=1):
		"""
		@summary: 向数据表插入一条记录
		@param dbPrefix:数据库前缀
		@param sql:要插入的sql格式
		@param value:要插入的记录数据tuple/list
		@param returnType:返回值类型，默认1，返回增加的主键，0则返回主键不是自增的行数
		@return: insertId 受影响的行数
		"""
		if self.checkDbPrefix(dbPrefix, sql)==False:
			return False
		try:
			self._cursor[dbPrefix+'_main'].execute(sql,value)
			if returnType==1:
				return self._cursor[dbPrefix+'_main'].lastrowid
			else:
				return self._cursor[dbPrefix+'_main'].rowcount
		except Exception, e:
			self._errorCode = -1996
			self._errorMsg = '插入数据出错了',e
			return False

	def insertMany(self,dbPrefix,sql,values):
		"""
		@summary: 向数据表插入多条记录
		@param dbPrefix:数据库前缀
		@param sql:要插入的sql格式
		@param values:要插入的记录数据tuple(tuple)/list[list]
		@return: count 受影响的行数
		"""
		if self.checkDbPrefix(dbPrefix, sql)==False:
			return False
		try:
			count = self._cursor[dbPrefix+'_main'].executemany(sql,values)
			return count
		except Exception, e:
			self._errorCode = -1996
			self._errorMsg = '插入数据出错了',e
			return False

	def __getInsertId(self, dbPrefix):
		"""
		@summary: 获取当前连接最后一次插入操作生成的id,如果没有则为０
		@param dbPrefix:数据库前缀
		"""
		try:
			self._cursor[dbPrefix+'_query'].execute("SELECT @@IDENTITY AS id")
			result = self._cursor[dbPrefix+'_query'].fetchall()
			return result[0][0]
		except Exception, e:
			self._errorCode = -19961
			self._errorMsg = '插入数据出错了',e
			return False

	def __query(self,dbPrefix,sql,param=None):
		try:
			if param is None:
				count = self._cursor[dbPrefix+'_main'].execute(sql)
			else:
				count = self._cursor[dbPrefix+'_main'].execute(sql,param)
			return count
		except Exception, e:
			self._errorCode = -1995
			self._errorMsg = '更新数据出错了',e
			return False

	def update(self,dbPrefix,sql,param=None):
		"""
		@summary: 更新数据表记录
		@param dbPrefix:数据库前缀
		@param sql: sql格式及条件，使用(%s,%s)
		@param param: 要更新的  值 tuple/list
		@return: count 受影响的行数
		"""
		if self.checkDbPrefix(dbPrefix, sql)==False:
			return False
		return self.__query(dbPrefix,sql,param)

	def delete(self,dbPrefix,sql,param=None):
		"""
		@summary: 删除数据表记录
		@param dbPrefix:数据库前缀
		@param sql: sql格式及条件，使用(%s,%s)
		@param param: 要删除的条件 值 tuple/list
		@return: count 受影响的行数
		"""
		if self.checkDbPrefix(dbPrefix, sql)==False:
			return False
		return self.__query(dbPrefix,sql,param)

	def begin(self,dbPrefix):
		"""
		@summary: 开启事务
		@param dbPrefix:数据库前缀
		"""
		#print dir(self._cursor[dbPrefix+'_main'])
		#self._conn[dbPrefix+'_main'].autocommit(0)
		return

	def commit(self,dbPrefix):
		"""
		@summary: 结束事务
		@param dbPrefix:数据库前缀
		"""
		self._conn[dbPrefix+'_main'].commit()

	def rollback(self,dbPrefix):
		"""
		@summary: 结束事务
		@param dbPrefix:数据库前缀
		"""
		self._conn[dbPrefix+'_main'].rollback()

	def dispose(self,isEnd=1):
		"""
		@summary: 释放连接池资源
		"""
		if isEnd==1:
			for x in self.dbConfig:
				self.commit(x)
		else:
			for x in self.dbConfig:
				self.rollback(x)
		for x in self.dbConfig:
			self._cursor[x+'_main'].close()
			self._cursor[x+'_query'].close()
			self._conn[x+'_main'].close()
			self._conn[x+'_query'].close()

class MemcacheEx(object):
	def __init__(self, serverName="server_1", hostName='localhost'):
		dbConfig = getConfig().get('memcache')
		dbConfig = dbConfig.get(serverName)
		mclient.connect([dbConfig['host']+':'+dbConfig['port']], hostName)
		self.mclient = mclient

	def set(self,keyName, keyValue):
		return mclient.set(keyName, keyValue)

	def get(self,keyName):
		return mclient.get(keyName)

	def delete(self, keyName):
		return mclient.delete(keyName)

	def get_multi(self, keys):
		return mclient.get_multi(keys)

	def set_multi(self, mapping):
		return mclient.set_multi(mapping)

	def delete_multi(self, keys):
		return mclient.delete_multi(keys)

def showMsg(code, msg):
	rd = {"s":code,"m":msg}
	return json.dumps(rd)+'(end)'

def showDict(dicts):
	return json.dumps(dicts)+'(end)' # wtx:dumps是将dict转化成str格式，loads是将str转化成dict格式

def jsonload(data):
	data = re.sub(r"(,?)(\w+?)\s+?:", r"\1'\2' :", data);
	data = data.replace("'", "\"");
	data = json.loads(data)
	return data

if __name__ == '__main__':
	#memcache
	obj = MemcacheEx('server_1')  #wtx:使用memcache作缓存，但是后面的obj赋值会被覆盖。实际还是没有使用memcache做缓存？
	print obj.set('key1', 'fdsfds')
	print obj.get('key1')
	#mysql
	obj = MysqlObject()
	print obj.getOne('us', ('select * from us_user', []))
	#version
	getVersion()
	#s = MysqlObject()
	#print s.getAll('us', 'select * from us_user')
	#print s.getOne('us', 'select * from us_user')
	#print s.getMany('us', 'select * from us_user',4)
	#print s.insertOne('us', "insert into us_user (user_name, user_pass, pass_rand, balance, funds_key, is_lock) values (%s, %s, %s, %s, %s, %s)", ['ddd33', '1s','2sa',5,'3df',1],1)#参数4默认1，返回新增的主键，为0时返回修改的行数
	#如果是innoDB请commit()
	#s.commit('us')
	#print s.getErrorMsg().decode('UTF-8').encode('gb2312')
	#print s.update('us', 'update us_user set user_name=%s where user_id=%s',['dddd34', 1])
	#s.commit('us')
	#print s.delete('us', 'delete from us_user where user_id=%s',[15])
	#s.commit('us')
	'''开启事务,涉及到几个库就要开启几个前缀'''
	#s.begin('us')
	#s.begin('lo')
	'''执行代码操作,用try执行，捕获异常，如果执行数据库返回值为False，那么就创建异常'''
	#......
	#try:
	#	.....如果出错了，可以自定义错误
	#	raise Exception('err')  #抛出异常
	#	.....如果没有出现异常，则提交
	#	s.commit('us')
	#	s.commit('lo')
	#	return True				#根据需要附上返回值
	#except Exception, e:
	#	......返回自定义错误
	#	s.rollback('us')
	#	s.rollback('lo')

def dict2list(aDict):
	if(isinstance(aDict,dict)):
		return aDict.values()
	else:
		return aDict