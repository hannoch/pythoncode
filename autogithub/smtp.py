#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-07 19:55:30
# @Author  : HannochTao (hannochtao@163.com)
# @Link    : http://www.imstudy.online
# @Version : $Id$


 
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_mail():
	
	msg_from='790152894@qq.com'  #发送方邮箱
	passwd='meeyzbaeowtbbdgf'    # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
	msg_to='hannochtao@163.com'  #收件人邮箱
	                            
	subject="python邮件测试"     #主题     
	content='''这是我使用python smtplib及email模块发送的邮件'''
	msg = MIMEText(content)
	msg['Subject'] = subject
	msg['From'] = msg_from
	msg['To'] = msg_to
	try:
	    s = smtplib.SMTP_SSL("smtp.qq.com",465)
	    s.login(msg_from, passwd)
	    s.sendmail(msg_from, msg_to, msg.as_string())
	    print ("发送成功")
	except Exception as e:
		print ("Error: 无法发送邮件")
		print(e)
    

if __name__ == '__main__':
	send_mail()
	#meil()