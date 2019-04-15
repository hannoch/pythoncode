目录结构

douban

├── DBOperator.py  操作数据

├── GetBookTag.py  个人用户书的标签

├── GetBookUrl.py  每本书的地址

├── GetPeople.py   每本书对应所有的评论用户

├── __init__.py    空包

└── UserAgent.py   浏览器头


# 

# 所需环境
`python3.x`

`pip install requirements.txt`

# 本程序的流程
流程就是，随便一本书---用户评论---用户想读的书--得到想读和在读的标签
脚本执行先后顺序：

1、首先要得到每本书对应的地址 `python3 GetBookUrl.py`  

2、再得到每本书对应所有的评论用户 `python3  GetPeople.py `

3、最后得到用户的标签 `python3  GetBookTag.py`


ps：三个脚本可独立运行，需要替换每个脚本里的cookies 

# 顺序流程
![获取cookies](https://github.com/hannoch/pythoncode/blob/master/douban/images/douban_1.png)
![书的标签](https://github.com/hannoch/pythoncode/blob/master/douban/images/douban_2.png)
![标签下的书](https://github.com/hannoch/pythoncode/blob/master/douban/images/douban_3.png)
![书的短评](https://github.com/hannoch/pythoncode/blob/master/douban/images/douban_4.png)
![用户主页](https://github.com/hannoch/pythoncode/blob/master/douban/images/douban_5.png)
![用户定义的标签](https://github.com/hannoch/pythoncode/blob/master/douban/images/douban_6.png)

# 数据库存储如下：
![书信息表](https://github.com/hannoch/pythoncode/blob/master/douban/images/douban_8.png)
![人信息表](https://github.com/hannoch/pythoncode/blob/master/douban/images/douban_9.png)
![最后的标签](https://github.com/hannoch/pythoncode/blob/master/douban/images/douban_10.png)
