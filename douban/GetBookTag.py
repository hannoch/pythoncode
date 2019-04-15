#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File : GetBookTag.py
# @Author :hannoch

import requests
import re
import time
import random,uuid

from bs4 import BeautifulSoup
from DBOperator import Db
import UserAgent

# 浏览器登录后得到的cookie，也就是刚才复制的字符串
cookie_str = r'll="118201"; bid=W7SayxGrHR0; _vwo_uuid_v2=D765E04ECA20563C6075E728873152889|2b2ff9ddfcf94c055d69b1ebbaf403fd; gr_user_id=7d770b11-ea67-40af-9098-87fc4da5c7f9; __yadk_uid=Riuk30a6EzqqgIz6cdlxkmBaRodPDlEU; push_noty_num=0; push_doumail_num=0; __utmv=30149280.19468; douban-profile-remind=1; ct=y; ps=y; viewed="26745556_1202226_4913064_30376507_30482656"; __utmc=30149280; __utmz=30149280.1554965362.12.6.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; ap_v=0,6.0; __utma=30149280.1873647356.1547038431.1554965362.1554985646.13; dbcl2="194682440:cXWPVgTKt4k"; ck=nAfX; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1554986251%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%3Fsource%3Dbook%22%5D; _pk_id.100001.8cb4=eb76370d08f764a6.1554728851.8.1554986251.1554965382.; _pk_ses.100001.8cb4=*; __utmt=1; __utmb=30149280.4.10.1554985646'
cookies = {}
for line in cookie_str.split(';'):
	key, value = line.split('=', 1)
	cookies[key] = value
# 设置请求头
headers = {ll="118201"; bid=W7SayxGrHR0; _vwo_uuid_v2=D765E04ECA20563C6075E728873152889|2b2ff9ddfcf94c055d69b1ebbaf403fd; gr_user_id=7d770b11-ea67-40af-9098-87fc4da5c7f9; __yadk_uid=Riuk30a6EzqqgIz6cdlxkmBaRodPDlEU; push_noty_num=0; push_doumail_num=0; __utmv=30149280.19468; douban-profile-remind=1; ct=y; ps=y; viewed="26745556_1202226_4913064_30376507_30482656"; __utmc=30149280; __utmz=30149280.1554965362.12.6.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; ap_v=0,6.0; __utma=30149280.1873647356.1547038431.1554965362.1554985646.13; dbcl2="194682440:cXWPVgTKt4k"; ck=nAfX; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1554986251%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%3Fsource%3Dbook%22%5D; _pk_id.100001.8cb4=eb76370d08f764a6.1554728851.8.1554986251.1554965382.; _pk_ses.100001.8cb4=*; __utmt=1; __utmb=30149280.4.10.1554985646
	'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}

Headers = {
	'User-Agent':random.choice(UserAgent.list)
	}
#https://book.douban.com/people/169923003/collect  xy读过的书(31)
#https://book.douban.com/people/169923003/wish  xy想读的书(759)

db = Db()
def GetPepoleInfo():
	pepole_list = db.SelectPepoleInfo(501,1500)
	for item in pepole_list:
		#print(item[1])
		#读过的书
		collect_url = "https://book.douban.com/people/{book_tag}/collect/".format(book_tag=item[1])
		print(collect_url)
		# 想读的书
		wish_url = "https://book.douban.com/people/{book_tag}/wish/".format(book_tag=item[1])
		print(wish_url)
		time.sleep(10 + random.random())
		rp = requests.get(collect_url, headers=headers, cookies=cookies)
		rp2 = requests.get(wish_url, headers=headers, cookies=cookies)
		
		rp.Encoding = 'utf-8'
		soup = BeautifulSoup(rp.text, 'html.parser')
		rp2.Encoding = 'utf-8'
		soup2 = BeautifulSoup(rp2.text, 'html.parser')
		print(soup)
		# 所有标签
		li_collect = soup.findAll(attrs={"class": "clearfix"})
		#li_collect = soup.findAll('li')
		li_wish = soup2.findAll('li')
		print(li_collect)
		print(li_wish)
		#tag_total = soup.findAll(attrs={"class": "clearfix"})
		temp_collect = str(li_collect)
		temp_wish = str(li_wish)
		#print(temp_collect)
		STR3 = r'mode=grid" title="(.*?)">'
		total_collect = re.findall(STR3, temp_collect, re.S | re.M)
		total_wish = re.findall(STR3, temp_wish, re.S | re.M)
		collect_tag = ";".join(total_collect)
		wish_tag = ";".join(total_wish)
		# if(not total_collect is None )or (not total_wish is None):
		# 	#print(total_num)
		# 	collect_tag = ";".join(total_collect)
		# 	wish_tag = ";".join(total_wish)
		#
		# else:
		# 	collect_tag = ""
		# 	wish_tag = ""
		now_time = time.strftime('%Y-%m-%d %H:%M:%S')
		data = {
			'id': uuid.uuid1(),
			'pepole_id': item[0],
			'collect_tag':collect_tag,
			'wish_tag': wish_tag,
			'create_time': now_time,
		}
		# 每页评论链接
		db.InsertPepoleTag(data)
		
		
		

if __name__ == '__main__':
	GetPepoleInfo()