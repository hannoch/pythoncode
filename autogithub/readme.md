# python模拟自动登录github，设置邮箱提醒

---

[TOC]


 
Python模拟Github登陆，详情请查看源码点链接进入Python-Spiders文集，模拟Github登陆可以分为五个操作步骤，步骤如下：

 - 模拟Github登陆步骤：
>   1、请求头：self.headers，请求url；
>   2、设置session，保存登陆信息cookies，生成github_cookie文件；
>   3、POST表单提交，请求数据格式post_data；
>   4、authenticity_token获取；
>   5、在个人中心验证判断是否登陆成功，输出个人中心信息即登陆成功。

# 一、获取请求头

① 在浏览器中敲入`https://github.com/login`，同时右击页面查看检查，如下图所示：
![image.png](https://upload-images.jianshu.io/upload_images/5451635-e8ff62bd4adf600b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Python模拟Github登陆

② 点击红框内login进入如下图所示：
![image.png](https://upload-images.jianshu.io/upload_images/5451635-1d6cf69fbf90c3d4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Python模拟Github登陆

③ 源码中对应部分：
```python
# 设置请求头
self.headers = {
    'Referer': 'https://github.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Host': 'github.com'
}
```
# 二、保存登陆信息cookies

① 设置session

② 保存登陆信息cookies，生成github_cookie文件，用cookies保存的信息加载个人设置，验证是否模拟登录成功

③ 源码中对应部分：
```python
# 设置session
self.session = requests.session()
# 生成github_cookie文件
self.session.cookies = cookielib.LWPCookieJar(filename='github_cookie')
```
# 三、POST表单提交

① POST表单提交字段获取，如下图所示：
![image.png](https://upload-images.jianshu.io/upload_images/5451635-556184c41d604c6f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Python模拟Github登陆

② 源码中对应部分：
```python
    #登陆时表单提交参数
    Form Data:
         commit:Sign in
         utf8:?
         authenticity_token:yyZprIm4aghZ0u7r25ymZjisfTjGdUAdDowD9fKHM0oUvHD1WjUHbn2sW0Cz1VglZWdGno543jod2M8+jwLv6w==
         login:*****
         password:******
```
# 四、authenticity_token获取

① 在浏览器中敲入https://github.com/login，获取网页文本文件

② 源码中对应部分：
```python
# 获取authenticity_token
  def get_token(self):
        response = self.session.get(self.loginUrl, headers=self.headers)
        html = etree.HTML(response.text)
        authenticity_token = html.xpath('//div/input[2]/@value')
        print(authenticity_token)
        return authenticity_token
```
# 五、在个人中心验证判断是否登陆成功

在个人中心验证判断是否登陆成功，输出个人中心信息即登陆成功，如下图：
![image.png](https://upload-images.jianshu.io/upload_images/5451635-71096fae5438ea33.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Python模拟Github登陆

即模拟GitHub模拟登陆成功。
# 六、使用QQ邮箱发送邮件提醒
这里用到了Python的两个包来发送邮件： smtplib 和 email 。
Python 的 email 模块里包含了许多实用的邮件格式设置函数，可以用来创建邮件“包裹”。使用的 MIMEText 对象，为底层的 MIME（Multipurpose InternetMailExtensions，多用途互联网邮件扩展类型）协议传输创建了一封空邮件，最后通过高层的SMTP 协议发送出去。 MIMEText 对象 msg 包括收发邮箱地址、邮件正文和主题，Python 通过它就可以创建一封格式正确的邮件。smtplib 模块用来设置服务器连接的相关信息。

要想通过QQ邮箱来发送邮件，需要开启QQ邮箱的设置-账户里SMTP服务，接下来会通过发送短信验证来获得授权码，有了授权码后就可以在代码里添加了。
![image.png](https://upload-images.jianshu.io/upload_images/5451635-afebd0926b2f3d43.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我新建了一个senemil.py文件用于测试

```python

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
```

网易邮箱接受到了QQ邮箱发送的邮件，如下图：
![image.png](https://upload-images.jianshu.io/upload_images/5451635-3c0a6f634f9aadc6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

整合了全部代码之后。
![image.png](https://upload-images.jianshu.io/upload_images/5451635-2255d314669e18f4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)







