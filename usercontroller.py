#!/usr/bin/env python
#coding:utf-8
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import re
import numpy as np

#定义端口号
define("port", default=8000, help="run on the given port", type=int)

#定义的全局变量
people_name=[]          #保存所有参与抽奖的人员
people_reward1_name=[]  #抽中一等奖的人员名单
people_reward2_name=[]  #抽中二等奖的人员名单
people_reward3_name=[]  #抽中三等奖的人员名单
falg=0   #每次只显示抽奖人数的一部分，不能全部显示出来,一等奖一名，二等奖两名，三等奖三名
people_reward1=0        #一等奖中奖人数
people_reward2=0        #二等奖中奖人数
people_reward3=0        #三等奖中奖人数
flag1 = ""            #一等奖是否一次性抽完,yes:一次性抽完；no：分批次抽完
flag2 = ""            #二等奖是否一次性抽完,yes:一次性抽完；no：分批次抽完
flag3 = ""            #三等奖是否一次性抽完,yes:一次性抽完；no：分批次抽完


def fun1(peoplestr):
  #字符串处理函数，主要将文件内容（名字）存放到列表中
  pattern=r','
  result=re.split(pattern,peoplestr)
  return result


class IndexHandler(tornado.web.RequestHandler):
  #渲染主页面
  def get(self):
    self.render("index.html")

class infoHandler(tornado.web.RequestHandler): #信息处理与提取
  def post(self):
    num_1 = self.get_argument("num1")
    num_2 = self.get_argument("num2")
    num_3 = self.get_argument("num3")
    flg1 = self.get_argument("panduan1")
    flg2 = self.get_argument("panduan2")
    flg3 = self.get_argument("panduan3")
    global people_reward1, people_reward2, people_reward3, flag1, flag2, flag3
    people_reward1 = int(num_1)
    people_reward2 = int(num_2)
    people_reward3 = int(num_3)
    flag1 = flg1
    flag2 = flg2
    flag3 = flg3
    print(flag1)       #显示为yes
    print(type(flag1)) #显示为str
    num = int(num_1)+int(num_2)+int(num_3)#一共有多少人中奖
    print(num)
    file = self.request.files #文件信息提取
    print(file)
    print(type(file))  #<class 'dict'>
    for inputname in file:
      http_file = file[inputname]
      print(http_file)
      people=http_file[0]['body']
    #  people.decode('ascii')
    print(people)
    print(type(people)) #  <class 'bytes'>

    people_str = people.decode(encoding='utf-8')
    print("people1",people_str,type(people_str)) #  <class 'str'>

    results = fun1(people_str)
    print(results)
    global people_name  #  保存所有参与抽奖的人员
    people_name = results

    hight = len(results)-1
    print(hight)
    ary1 = set()
    #  根据中奖总人数将所有中奖人员一次性全部抽出，放在集合之中
    # （因为前提是所有中奖人员没有重复，所以抽一次和抽三次结果是一样的）
    while len(ary1) < num:
      a = np.random.random_integers(low=0, high=hight, size=1)
      ary1.add(a[0])
    #  ary = random.sample(range(0, hight), num)
    #  将集合转成列表
    ary=list(ary1)
    print(ary)
    people_1 = []   #  存放一等奖中奖名单
    people_3 = []   #  存放二等奖中奖名单
    people_2 = []   #  存放三等奖中奖名单
    for i in ary[0:int(num_1)]:
      people_1.append(results[i])
    for j in ary[int(num_1):int(num_1)+int(num_2)]:
      people_2.append(results[j])
    for k in ary[int(num_1)+int(num_2):int(num_1)+int(num_2)+int(num_3)]:
      people_3.append(results[k])
    global people_reward1_name
    people_reward1_name=people_1
    global people_reward2_name
    people_reward2_name=people_2
    global  people_reward3_name
    people_reward3_name=people_3
    self.render("user.html", num1=num_1, people1="  ?  ", num2=num_2, people2="  ?  ", num3=num_3, people3="  ?  ", people_in=people)
    #global falg
    #self.render("user.html", num1=num_1, people1=people_1[falg:falg+1], num2=num_2, people2=people_2[falg:falg+2], num3=num_3, people3=people_3[falg:falg+3], people_in=people)
    #falg = falg + 1

class ChoujiangHandler(tornado.web.RequestHandler):
  def post(self):
    global falg, flag1, flag2, flag3
    global people_reward1_name, people_reward2_name, people_reward3_name
    global people_reward1, people_reward2, people_reward3

    if flag1=="yes" and flag2=="yes" and flag3=="yes":
      self.render("user.html", num1=people_reward1, people1=people_reward1_name, num2=people_reward2,
                  people2=people_reward2_name, num3=people_reward3,
                  people3=people_reward3_name, people_in=people_name)

    if flag1=="yes" and flag2=="yes" and flag3=="no":
        if falg+3 <= people_reward3:
          self.render("user.html", num1=people_reward1, people1=people_reward1_name, num2=people_reward2,
                    people2=people_reward2_name, num3=people_reward3,
                    people3=people_reward3_name[falg:falg+3], people_in=people_name)
          falg=falg+3
        else:
          self.render("user.html", num1=people_reward1, people1=people_reward1_name, num2=people_reward2,
                      people2=people_reward2_name, num3=people_reward3,
                      people3=people_reward3_name[falg:], people_in=people_name)

    if flag1=="yes" and flag2=="no" and flag3=="no":
        if falg*3+3 <= people_reward3 and falg*2+2 <= people_reward2:
          self.render("user.html", num1=people_reward1, people1=people_reward1_name, num2=people_reward2,
                    people2=people_reward2_name[falg*2:falg*2+2], num3=people_reward3,
                    people3=people_reward3_name[falg*3:falg*3+3], people_in=people_name)
          falg=falg+1
        if falg*3+3 > people_reward3 and falg*2+2 <= people_reward2:
          self.render("user.html", num1=people_reward1, people1=people_reward1_name, num2=people_reward2,
                    people2=people_reward2_name[falg*2:falg*2+2], num3=people_reward3,
                    people3=people_reward3_name[falg*3:], people_in=people_name)
          falg=falg+1
        if falg*3+3 > people_reward3 and falg*2+2 > people_reward2:
          self.render("user.html", num1=people_reward1, people1=people_reward1_name, num2=people_reward2,
                    people2=people_reward2_name[falg*2:], num3=people_reward3,
                    people3=people_reward3_name[falg*3:], people_in=people_name)
          falg=falg+1
        if falg*3+3 <= people_reward3 and falg*2+2 > people_reward2:
          self.render("user.html", num1=people_reward1, people1=people_reward1_name, num2=people_reward2,
                    people2=people_reward2_name[falg*2:], num3=people_reward3,
                    people3=people_reward3_name[falg*3:falg*3+3], people_in=people_name)
          falg=falg+1

    if flag1=="no" and flag2=="no" and flag3=="no":
        if falg*3+3 <= people_reward3 and falg*2+2 <= people_reward2:
          self.render("user.html", num1=people_reward1, people1=people_reward1_name[falg:falg+1], num2=people_reward2,
                    people2=people_reward2_name[falg*2:falg*2+2], num3=people_reward3,
                    people3=people_reward3_name[falg*3:falg*3+3], people_in=people_name)
          falg=falg+1
        if falg*3+3 > people_reward3 and falg*2+2 <= people_reward2:
          self.render("user.html", num1=people_reward1, people1=people_reward1_name[falg:falg+1], num2=people_reward2,
                    people2=people_reward2_name[falg*2:falg*2+2], num3=people_reward3,
                    people3=people_reward3_name[falg*3:], people_in=people_name)
          falg=falg+1
        if falg*3+3 > people_reward3 and falg*2+2 > people_reward2:
          self.render("user.html", num1=people_reward1, people1=people_reward1_name[falg:falg+1], num2=people_reward2,
                    people2=people_reward2_name[falg*2:], num3=people_reward3,
                    people3=people_reward3_name[falg*3:], people_in=people_name)
          falg=falg+1
        if falg*3+3 <= people_reward3 and falg*2+2 > people_reward2:
          self.render("user.html", num1=people_reward1, people1=people_reward1_name[falg:falg+1], num2=people_reward2,
                    people2=people_reward2_name[falg*2:], num3=people_reward3,
                    people3=people_reward3_name[falg*3:falg*3+3], people_in=people_name)
          falg=falg+1


handlers = [
  (r"/", IndexHandler),
  (r"/info", infoHandler),
  (r"/choujiang",ChoujiangHandler),
]
template_path = os.path.join(os.path.dirname(__file__),"template")
if __name__ == "__main__":
  tornado.options.parse_command_line()
  app = tornado.web.Application(handlers, template_path)
  http_server = tornado.httpserver.HTTPServer(app)
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()