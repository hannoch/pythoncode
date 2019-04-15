#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File : GetPepole.py
# @Author :hannoch

import sys,io
import requests
import re
import time
import random,uuid

from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from DBOperator import Db
import UserAgent

# 浏览器登录后得到的cookie，也就是刚才复制的字符串
cookie_str = r'll="118201"; bid=W7SayxGrHR0; _vwo_uuid_v2=D765E04ECA20563C6075E728873152889|2b2ff9ddfcf94c055d69b1ebbaf403fd; gr_user_id=7d770b11-ea67-40af-9098-87fc4da5c7f9; __yadk_uid=Riuk30a6EzqqgIz6cdlxkmBaRodPDlEU; push_noty_num=0; push_doumail_num=0; __utmv=30149280.19468; douban-profile-remind=1; ct=y; ps=y; viewed="26745556_1202226_4913064_30376507_30482656"; __utmc=30149280; ap_v=0,6.0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1554957972%2C%22https%3A%2F%2Faccounts.douban.com%2Fsafety%2Funlock_sms%2Fresetpassword%3Fconfirmation%3D1519de69fbdf1fda%26alias%3D%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.1873647356.1547038431.1554954542.1554957973.11; __utmz=30149280.1554957973.11.5.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/safety/unlock_sms/resetpassword; __utmt=1; dbcl2="194682440:dHPPWmAiTTw"; ck=Mi10; _pk_id.100001.8cb4=eb76370d08f764a6.1554728851.6.1554958043.1554949515.; __utmb=30149280.9.10.1554957973'
# 把cookie字符串处理成字典，以便接下来使用
cookies = {}
for line in cookie_str.split(';'):
	key, value = line.split('=', 1)
	cookies[key] = value
# 设置请求头
headers = {
	'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}

Headers = {
	'User-Agent':random.choice(UserAgent.list)
	}

db = Db()
def GetPepoleInfo():
	"""
	得到每本总评论数量
	:return:
	"""
	
	book_list = db.SelectBookInfo(51,100)
	for item in book_list:
		#total - comments
		time.sleep(3 + random.random())
		comments_url = "https://book.douban.com/subject/{book_tag}/comments/".format(book_tag = item[1])
		print(comments_url)
		rp = requests.get(comments_url, headers=headers, cookies=cookies)
		
		rp.Encoding='utf-8'
		soup=BeautifulSoup(rp.text,'html.parser')
		#print(soup)
		#全部共几条评论
		comments_total = soup.find(attrs={"id":"total-comments"})
		temp = str(comments_total)
		print(temp)
		STR3 = r'[0-9]\d*'
		total_num = re.findall(STR3, temp, re.S | re.M)
		total_num = "".join(total_num) #全部共 252 条
		#每页评论链接
		total_page = int(total_num) % 20
		
		for page_num in range(1,total_page + 1):
		#每页有２０条评论
			comments_page = "https://book.douban.com/subject/{book_tag}/comments/hot?p={page_num}".format(book_tag = item[1],page_num = page_num)
			#print(comments_page)
			#GetPepoleUrl(id, url)
			GetPepoleUrl(item[0], comments_page)
			
			
			
def GetPepoleUrl(book_id, comments_page):
	'''
	得到用户url和名字
	:param:book_id,comments_page
	:return:
	'''
	#comments_page = "https://book.douban.com/subject/26787813/comments/hot?p=1"
	# print(pepole_list)
	time.sleep(10 + random.random())
	print(comments_page)
	rp2 = requests.get(comments_page, headers=Headers, cookies=cookies)

	rp2.Encoding = 'utf-8'
	soup2 = BeautifulSoup(rp2.text, 'html.parser')
	#print(soup2)
	#搜索所有class': 'comment-info'
	pepole_span = soup2.findAll(attrs={'class': 'comment-info'})
	
	STR = r'<a href="(.*?)">(.*?)</a>'
	STR2 = r'people/(.*?)/'
	result = re.findall(STR, str(pepole_span), re.S | re.M)
	print(result)
	#('https://www.douban.com/people/zitawong/', '夕山')
	for item in result:
		print(item)
		pepole_tag = re.findall(STR2, item[0], re.S | re.M)
		now_time = time.strftime('%Y-%m-%d %H:%M:%S')
		data = {
			'id': uuid.uuid1(),
			'book_id': book_id,
			'pepole_url': item[0],
			'pepole_name': item[1],
			'pepole_tag': "".join(pepole_tag),
			'create_time': now_time,
		}
		db.InsertPepoleInfo(data)
	#
	#print(pepole_span)
	# 全部共几条评论


	
if __name__ == '__main__':
	
	GetPepoleInfo()
