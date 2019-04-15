#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File : GetBookUrl.py
# @Author : hannoch

import sys,io
import requests
import re
import time
import random,uuid

from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from DBOperator import Db
import UserAgent

#
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码
# # 登录后才能访问的网页  个人主页
# book_url = 'https://book.douban.com/'
# # 浏览器登录后得到的cookie，也就是刚才复制的字符串
# cookie_str = r'll="118201"; bid=W7SayxGrHR0; _vwo_uuid_v2=D765E04ECA20563C6075E728873152889|2b2ff9ddfcf94c055d69b1ebbaf403fd; gr_user_id=7d770b11-ea67-40af-9098-87fc4da5c7f9; __yadk_uid=2y81glVC7atDZo6MhOoNknyJDMhg0KWL; push_noty_num=0; push_doumail_num=0; __utmv=30149280.19468; douban-profile-remind=1; ct=y; ps=y; __utma=30149280.1873647356.1547038431.1554728852.1554827006.4; __utmc=30149280; __utmz=30149280.1554827006.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; ap_v=0,6.0; __utmt_douban=1; __utmb=30149280.2.10.1554827006; __utma=81379588.1636856418.1554728854.1554728854.1554827007.2; __utmc=81379588; __utmz=81379588.1554827007.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmb=81379588.1.10.1554827007; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1554827007%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=33cd253a-b845-45d2-94aa-9f70476dd21d; gr_cs1_33cd253a-b845-45d2-94aa-9f70476dd21d=user_id%3A0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_33cd253a-b845-45d2-94aa-9f70476dd21d=true; _pk_id.100001.3ac3=86826816f0727505.1554728854.2.1554827010.1554728857.; dbcl2="194682440:iDlm3SCFt2M"'
#
# # 把cookie字符串处理成字典，以便接下来使用
# cookies = {}
# for line in cookie_str.split(';'):
# 	key, value = line.split('=', 1)
# 	cookies[key] = value
# # 设置请求头
# headers = {
# 	'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
# }
#

'''
robots协议
'''
UrlRobots = 'https://book.douban.com/robots.txt'


def GetRobotsTxt(url):
	rp = RobotFileParser()
	rp.set_url(url)
	rp.read()
	print(rp.can_fetch('*', 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'))
	print(rp.can_fetch('*', 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4'))
	print(rp.can_fetch('*', 'https://book.douban.com/tag/%E6%9D%91%E4%B8%8A%E6%98%A5%E6%A0%91?start=40&type=S'))

# GetRobotsTxt(UrlRobots)

'''
爬取标签的5页内容并保存至text.txt
'''
# 参数准备
Headers = {
	'User-Agent':random.choice(UserAgent.list)
	}


def GetOneType(UrlLabel, Headers, Num):
	for i in range(50):
		print('正在抓取' + labels[Num] + '类的第' + str(i) + '页')
		url = UrlLabel + '?start=' + str(i * 20) + '&type=S'
		
		rp = requests.get(url, headers=Headers)
		# 注意目标文件的编码方式要改成utf-8，而不是Unicode，否则否解码失败
		with open("HtmlCode.txt", 'w', encoding='utf-8') as f:
			f.write(rp.text)
		ReEx(Num)
		time.sleep(3 + random.random())


# GetOnepage(Url,Headers)

'''
书名链接并存入数据库
'''
def ReEx(Num):
	FileName = str(labels[Num]) + '.txt'
	with open('HtmlCode.txt', 'r', encoding='utf-8') as file_re:
		content = file_re.read()
		#STR1 = r'class="nbg" .*?title="(.*?)"'
		STR = r'class="nbg" href="(.*?)".*?title="(.*?)"'
		STR2 = r'[0-9]\d*'
		result = re.findall(STR, content, re.S | re.M)
		db = Db()
		for item in result:
			
			book_tag = re.findall(STR2, item[0], re.S | re.M)
			now_time = time.strftime('%Y-%m-%d %H:%M:%S')
			data = {
				'id':uuid.uuid1(),
				'book_url': item[0],
				'book_name':item[1],
				'book_tag': ''.join(book_tag),
				'create_time': now_time,
			}
			db.InsertBookInfo(data)
			
		#
		# # 追加文本'a'而非覆盖文本'w'
		# with open(FileName, 'a', encoding='utf-8') as file_result:
		# 	file_result.write(str(result))
		# # file_result.write('\n')


'''
抓取多个页面
'''
#labels = ['小说', '外国文学', '文学', '随笔', '中国文学', '经典', '日本文学', '散文', '村上春树']
labels = ['诗歌', '童话', '儿童文学', '古典文学', '名著', '王小波', '余华', '杂文', '张爱玲', '当代文学', '钱钟书', '外国名著', '鲁迅', '诗词', ' 茨威格', '杜拉斯', '港台']

def GetAllPages():
	for i in range(len(labels)):
		UrlLabel = 'https://book.douban.com/tag/' + labels[i]
		GetOneType(UrlLabel, Headers, i)
	print('抓取完成')

# def getBookUrl():
# 	# 在发送get请求时带上请求头和cookies
# 	resp = requests.get(book_url, headers=headers, cookies=cookies)
# 	resp.Encoding='utf-8'
# 	soup=BeautifulSoup(resp.text,'html.parser')
# 	#所有的a标签
# 	book_div = soup.findAll('a')
# 	bookUrl = ','.join(str(i) for i in book_div)
# 	STR = r'href="(.*?)".*?title="(.*?)"'
# 	result = re.findall(STR, bookUrl)
# 	return result


if __name__ == '__main__':
	#获取图书链接
	GetAllPages()
