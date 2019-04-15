#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File : Db.py
# @Author :hannoch
# -*- encoding:utf-8 -*-
import pymysql
class Db():
	def __init__(self, user='root', password='hannoch', dbname='douban', port=3306, host='localhost'):
		self.host = host
		self.user = user
		self.pwd = password
		self.dbname = dbname
		self.port = port
		
		if self.connect() is False:
			print(self.dbname + "数据库连接异常！\n")
			return None
		print('数据库连接成功！')
	
	def connect(self):
		try:
			conn = pymysql.connect(host=self.host, user=self.user, password=self.pwd, db=self.dbname, port=self.port,
			                       use_unicode=True, charset="utf8")
			self.conn = conn
			self.cursor = conn.cursor()
		except:
			return False
		return True
	
	def IsIdExists(self, id, tablename):
		sql = 'select * from ' + tablename + ' where id=' + str(id)
		self.cursor.execute(sql)
		self.conn.commit()
		result = self.cursor.fetchall()#:接收全部的返回结果行.
		if result is None:
			return False
		return True
	
	def InserInfos(self, dataSet):
		for data in dataSet:
			if (self.IsIdExists(data['id'], 'book_info') == True):
				print('该书籍已经收集过，自动忽略')
				pass
			self.InsertAInfo(data)
	
	# 查询书的信息
	def SelectBookInfo(self, start_num,end_num):
		
		print("读取图书信息第"+ str(start_num) + "到" + str(end_num)+"条")
		# 'select id,book_url from book_info limit 0,10'
		sql = 'select id,book_tag,book_url,book_name from book_info limit ' + str(start_num) +',' + str(end_num)
		#print(sql)
		self.cursor.execute(sql)
		self.conn.commit()
		result = self.cursor.fetchall()# 接收全部的返回结果行.
		if result is None:
			return False
		return result
	
	# 插入书名
	def InsertBookInfo(self, data):
		print(data)
		try:
			sql = (
			"insert into book_info (id,book_name,book_url,book_tag,create_time) values ('%s','%s','%s','%s','%s')" % (
				data['id'], data['book_name'], data['book_url'], data['book_tag'], data['create_time']))
			#print(sql)
			self.cursor.execute(sql)
			self.conn.commit()
		except:
			print('数据库写入出错，操作回滚')
			self.conn.rollback()
			self.conn.commit()
			return
		print('数据库写入成功')
		
	# 插入人的信息
	def InsertPepoleInfo(self, data):
		print(data)
		try:
			sql = (
			"insert into pepole_info (id,book_id,pepole_name,pepole_url,pepole_tag,create_time) values ('%s','%s','%s','%s','%s','%s')" % (
				data['id'], data['book_id'], data['pepole_name'], data['pepole_url'],data['pepole_tag'], data['create_time']))
			print(sql)
			self.cursor.execute(sql)
			self.conn.commit()
		except:
			print('数据库写入出错，操作回滚')
			self.conn.rollback()
			self.conn.commit()
			return
		print('数据库写入成功')
	# 查询人的信息
	def SelectPepoleInfo(self, start_num, end_num):
		
		print("读取人员信息第" + str(start_num) + "到" + str(end_num) + "条")
		# 'select id,book_url from book_info limit 0,10'
		sql = 'select id,pepole_tag,pepole_url,pepole_name from pepole_info limit ' + str(start_num) + ',' + str(end_num)
		# print(sql)
		self.cursor.execute(sql)
		self.conn.commit()
		result = self.cursor.fetchall()  # 接收全部的返回结果行.
		if result is None:
			return False
		return result
	
	# 插入人的信息
	def InsertPepoleTag(self, data):
		print(data)
		try:
			sql = (
			"insert into pepole_tag (id, pepole_id, collect_tag, wish_tag, create_time) values ('%s','%s','%s','%s','%s')" % (
				data['id'], data['pepole_id'], data['collect_tag'], data['wish_tag'], data['create_time']))
			print(sql)
			self.cursor.execute(sql)
			self.conn.commit()
		except:
			print('数据库写入出错，操作回滚')
			self.conn.rollback()
			self.conn.commit()
			return
		print('数据库写入成功')
		