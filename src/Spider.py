#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import re
import requests
import sys
import traceback
from lxml import etree
from config_reader import config_reader
from datetime import datetime
from datetime import timedelta
import codecs
import csv
import random
from user_agents import agents
import sched
import time

#reload(sys)
#sys.setdefaultencoding("utf-8")

class Weibo:
    #cookie = {"Cookie":"_T_WM=f0dea614db5b50b38845be3a06cd6622; SCF=AjMT0f8E70EN4pon8yufMaIOzQoJegKPOXbBD-PDVxTKbf1hLpdruK144L69rmy7cSVCW3aJWq2X77n1m3T3sQo.; SUB=_2A2530xlBDeRhGeVH6FQT8SnEzTiIHXVVP6cJrDV6PUJbkdAKLVX8kW1NT09ZCCUxPqMlIvfQb4KBknxrMrBP6BuE; SUHB=09P9MkSYWnF8z0; SSOLoginState=1524066577"}
    cookie = {"Cookie":""}
    # Weibo类初始化
    def __init__(self, user_id, filter=0):
        self.user_id = user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.filter = filter  # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
        self.username = ''  # 用户名，如“Dear-迪丽热巴”
        self.weibo_num = 0  # 用户全部微博数
        self.weibo_num2 = 0  # 爬取到的微博数
        self.pr = 0 #用户的pageRank数目

        self.following = 0  # 用户关注数
        self.followers = 0  # 用户粉丝数
        self.weibo_content = []  # 微博内容
        self.publish_time = []  # 微博发布时间
        self.up_num = []  # 微博对应的点赞数
        self.retweet_num = []  # 微博对应的转发数
        self.comment_num = []  # 微博对应的评论数

    # 获取用户昵称
    def get_username(self):
        try:
            url = "https://weibo.cn/%d/info" % (self.user_id)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            username = selector.xpath("//title/text()")[0]
            self.username = username[:-3]
            ##print u"用户名: " + self.username
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

    # 获取用户微博数、关注数、粉丝数
    def get_user_info(self):
        try:
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
                self.user_id, self.filter)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            pattern = r"\d+\.?\d*"

            # 微博数
            str_wb = selector.xpath(
                "//div[@class='tip2']/span[@class='tc']/text()")[0]
            guid = re.findall(pattern, str_wb, re.S | re.M)
            for value in guid:
                num_wb = int(value)
                break
            self.weibo_num = num_wb
            ##print u"微博数: " + str(self.weibo_num)

            # 关注数
            str_gz = selector.xpath("//div[@class='tip2']/a/text()")[0]
            guid = re.findall(pattern, str_gz, re.M)
            self.following = int(guid[0])
            ##print u"关注数: " + str(self.following)

            # 粉丝数
            str_fs = selector.xpath("//div[@class='tip2']/a/text()")[1]
            guid = re.findall(pattern, str_fs, re.M)
            self.followers = int(guid[0])
            ##print u"粉丝数: " + str(self.followers)

        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

    # 获取"长微博"全部文字内容
    def get_long_weibo(self, weibo_link):
        try:
            html = requests.get(weibo_link, cookies=self.cookie).content
            selector = etree.HTML(html)
            info = selector.xpath("//div[@class='c']")[1]
            wb_content = info.xpath("div/span[@class='ctt']")[0].xpath(
                "string(.)").encode(sys.stdout.encoding, "ignore").decode(
                sys.stdout.encoding)
            return wb_content
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()


    # 获取用户微博内容及对应的发布时间、点赞数、转发数、评论数
    def get_weibo_info(self):
        try:
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
                self.user_id, self.filter)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            if selector.xpath("//input[@name='mp']") == []:
                page_num = 1
            else:
                page_num = (int)(selector.xpath(
                    "//input[@name='mp']")[0].attrib["value"])
            pattern = r"\d+\.?\d*"

            #get page infos
            #page_num = 1
            #获取第一条微博信息
            page_num = 1
            for page in range(1, page_num + 1):
                url2 = "https://weibo.cn/u/%d?filter=%d&page=%d" % (
                    self.user_id, self.filter, page)
                html2 = requests.get(url2, cookies=self.cookie).content
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")
                is_empty = info[0].xpath("div/span[@class='ctt']")
                if is_empty:
                    #for i in range(0, len(info) - 2):
                    #len(info)决定了总共的微博数量
                    for i in range(0, 1):
                        # 微博内容
                        str_t = info[i].xpath("div/span[@class='ctt']")
                        weibo_content = str_t[0].xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(
                            sys.stdout.encoding)
                        print 'weibo_content',weibo_content
                        weibo_content = weibo_content[:-1]

                        weibo_id = info[i].xpath("@id")[0][2:]
                        a_link = info[i].xpath("div/span[@class='ctt']/a/@href")
                        if a_link:
                            if a_link[-1] == "/comment/" + weibo_id:
                                weibo_link = "https://weibo.cn" + a_link[-1]
                                wb_content = self.get_long_weibo(weibo_link)
                                if wb_content:
                                    weibo_content = wb_content
                        self.weibo_content.append(weibo_content)
                        ##print u"微博内容：" + weibo_content

                        # 微博发布时间
                        str_time = info[i].xpath("div/span[@class='ct']")
                        str_time = str_time[0].xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(
                            sys.stdout.encoding)
                        publish_time = str_time.split(u'来自')[0]
                        if u"刚刚" in publish_time:
                            publish_time = datetime.now().strftime(
                                '%Y-%m-%d %H:%M')
                        elif u"分钟" in publish_time:
                            minute = publish_time[:publish_time.find(u"分钟")]
                            minute = timedelta(minutes=int(minute))
                            publish_time = (
                                datetime.now() - minute).strftime(
                                "%Y-%m-%d %H:%M")
                        elif u"今天" in publish_time:
                            today = datetime.now().strftime("%Y-%m-%d")
                            time = publish_time[3:]
                            publish_time = today + " " + time
                        elif u"月" in publish_time:
                            year = datetime.now().strftime("%Y")
                            month = publish_time[0:2]
                            day = publish_time[3:5]
                            time = publish_time[7:12]
                            publish_time = (
                                year + "-" + month + "-" + day + " " + time)
                        else:
                            publish_time = publish_time[:16]
                        self.publish_time.append(publish_time)
                        ##print u"微博发布时间：" + publish_time

                        str_footer = info[i].xpath("div")[-1]
                        str_footer = str_footer.xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
                        str_footer = str_footer[str_footer.rfind(u'赞'):]
                        guid = re.findall(pattern, str_footer, re.M)

                        # 点赞数
                        up_num = int(guid[0])
                        self.up_num.append(up_num)
                        ##print u"点赞数: " + str(up_num)

                        # 转发数
                        retweet_num = int(guid[1])
                        self.retweet_num.append(retweet_num)
                        ##print u"转发数: " + str(retweet_num)

                        # 评论数
                        comment_num = int(guid[2])
                        self.comment_num.append(comment_num)
                        ##print u"评论数: " + str(comment_num)

                        self.weibo_num2 += 1

            ## if not self.filter:
            ##     print u"共" + str(self.weibo_num2) + u"条微博"
            ## else:
            ##     print (u"共" + str(self.weibo_num) + u"条微博，其中" +
            ##            str(self.weibo_num2) + u"条为原创微博"
            ##            )
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()



    # 获取用户微博内容及对应的发布时间、点赞数、转发数、评论数
    # 如果已知用户的ID好的weiboID，获取微博的相应的数据
    def get_weibo_infos(self,weiboId):
        try:
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
                self.user_id, self.filter)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            if selector.xpath("//input[@name='mp']") == []:
                page_num = 1
            else:
                page_num = (int)(selector.xpath(
                    "//input[@name='mp']")[0].attrib["value"])
            pattern = r"\d+\.?\d*"

            #获取第一条微博信息
            page_num = 10
            for page in range(1, page_num + 1):
                url2 = "https://weibo.cn/u/%d?filter=%d&page=%d" % (
                    self.user_id, self.filter, page)
                html2 = requests.get(url2, cookies=self.cookie).content
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")

                #links:file:///C:/Users/hasee/Desktop/index.html
                temp_weiboid = "//div[@id='%s']" % (weiboId)
                #temp = selector2.xpath("//div[@id='M_GckPkc10h']")
                temp = selector2.xpath(temp_weiboid)
                if temp:
                    #根据微博ID获得微博全部内容的信息
                    str_temp = temp[0].xpath("div/span[@class='ctt']")
                    weibo_content = str_temp[0].xpath("string(.)").encode(
                        sys.stdout.encoding, "ignore").decode(
                        sys.stdout.encoding)
                    #print weibo_content
                    #获取id的[2:end]
                    weibo_id = temp[0].xpath("@id")[0][2:]
                    a_link = temp[0].xpath("div/a/@href")
                    if a_link:
                        if a_link[-1] == "/comment/" + weibo_id:
                            weibo_link = "https://weibo.cn" + a_link[-1]
                            wb_content = self.get_long_weibo(weibo_link)
                            if wb_content:
                                weibo_content = wb_content
                    self.weibo_content.append(weibo_content)

                    # 微博发布时间
                    str_time = temp[0].xpath("div/span[@class='ct']")
                    str_time = str_time[0].xpath("string(.)").encode(
                        sys.stdout.encoding, "ignore").decode(
                        sys.stdout.encoding)
                    publish_time = str_time.split(u'来自')[0]

                    if u"刚刚" in publish_time:
                        publish_time = datetime.now().strftime(
                            '%Y-%m-%d %H:%M')
                    elif u"分钟" in publish_time:
                        minute = publish_time[:publish_time.find(u"分钟")]
                        minute = timedelta(minutes=int(minute))
                        publish_time = (
                            datetime.now() - minute).strftime(
                            "%Y-%m-%d %H:%M")
                    elif u"今天" in publish_time:
                        today = datetime.now().strftime("%Y-%m-%d")
                        time = publish_time[3:]
                        publish_time = today + " " + time
                    elif u"月" in publish_time:
                        year = datetime.now().strftime("%Y")
                        month = publish_time[0:2]
                        day = publish_time[3:5]
                        time = publish_time[7:12]
                        publish_time = (year + "-" + month + "-" + day + " " + time)
                    else:
                        publish_time = publish_time[:16]
                    self.publish_time.append(publish_time)
                    str_footer = temp[0].xpath("div")[-1]
                    str_footer = str_footer.xpath("string(.)").encode(
                        sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
                    str_footer = str_footer[str_footer.rfind(u'赞'):]
                    guid = re.findall(pattern, str_footer, re.M)

                    # 点赞数
                    up_num = int(guid[0])
                    self.up_num.append(up_num)
                    ##print u"点赞数: " + str(up_num)

                    # 转发数
                    retweet_num = int(guid[1])
                    self.retweet_num.append(retweet_num)
                    ##print u"转发数: " + str(retweet_num)

                    # 评论数
                    comment_num = int(guid[2])
                    self.comment_num.append(comment_num)
                    ##print u"评论数: " + str(comment_num)

        except Exception, e:
            print "Error: ", e
            #traceback.print_exc()

    # 将爬取的信息写入文件
    def write_txt(self):
        try:
            if self.filter:
                result_header = u"\n\n原创微博内容：\n"
            else:
                result_header = u"\n\n微博内容：\n"
            result = (u"用户信息\n用户昵称：" + self.username +
                      u"\n用户id：" + str(self.user_id) +
                      u"\n微博数：" + str(self.weibo_num) +
                      u"\n关注数：" + str(self.following) +
                      u"\n粉丝数：" + str(self.followers) +
                      result_header
                      )
            for i in range(1, self.weibo_num2 + 1):
                text = (str(i) + ":" + self.weibo_content[i - 1] + "\n" +
                        u"发布时间：" + self.publish_time[i - 1] + "\n" +
                        u"点赞数：" + str(self.up_num[i - 1]) +
                        u"	 转发数：" + str(self.retweet_num[i - 1]) +
                        u"	 评论数：" + str(self.comment_num[i - 1]) + "\n\n"
                        )
                result = result + text
            file_dir = os.path.split(os.path.realpath(__file__))[0] + os.sep + "weibo"
            if not os.path.isdir(file_dir):
                os.mkdir(file_dir)
            file_path = file_dir + os.sep + "%d" % self.user_id + ".txt"
            f = open(file_path, "wb")
            f.write(result.encode(sys.stdout.encoding))
            f.close()
            print u"微博写入文件完毕，保存路径:"
            print file_path
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

    # 运行爬虫
    def start(self):
        try:
            self.get_username()
            self.get_user_info()
            self.get_weibo_info()
            #self.write_txt()
            print u"信息抓取完毕"
            print "==========================================================================="
        except Exception, e:
            print "Error: ", e


    # 运行爬虫
    def start_data(self,weiboId):
        try:
            self.get_username()
            self.get_user_info()
            # self.get_weibo_info()
            # self.write_txt()
            # self.get_proper_info()
            self.get_weibo_infos(weiboId)
            #print "==========================================================================="
        except Exception, e:
            print "Error: ", e


def task():
    try:
        filter = 1  # 值为0表示爬取全部微博（原创微博+转发微博），值为1表示只爬取原创微博
        param = config_reader()
        user_ids = param['userids']
        cookie = {"Cookie": ""}
        cookie['Cookie'] = param['cookie']

        #proper_infos = get_proper_info(cookie,user_ids)
        #print proper_infos

        #proper_infos = [['1197191492', 'M_GcGGXEkxM'], ['5127716917', 'M_GctZ0xuOz'], ['1886437464', 'M_GclEqckbg'], ['1337925752', 'M_GcGBvizIY'], ['1864507535', 'M_GcnRV7hhr'], ['2032640064', 'M_GcImKDFdw'], ['5585682587', 'M_GcI62zfbD'], ['3083673764', 'M_GcEcA9bnd']]
        proper_infos = [['1197191492', 'M_GcMn6pFEH']]
        #print proper_infos
        for i in range(len(proper_infos)):
            data = []
            wb = Weibo(int(proper_infos[i][0]), filter)  # 调用Weibo类，创建微博实例wb
            wb.cookie['Cookie'] = param['cookie']
            #wb.start()
            wb.start_data(proper_infos[i][1])
            #这三个参数用于计算pageRank的值，影响因子
            print u"用户名：" + wb.username
            # print u"全部微博数：" + str(wb.weibo_num)
            # print u"关注数：" + str(wb.following)
            # print u"粉丝数：" + str(wb.followers)

            print proper_infos[i]
            now_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            temp = [wb.up_num[0], wb.retweet_num[0], wb.comment_num[0], now_time]
            data.append(temp)
            print temp
            write_data(proper_infos[i][0],data,i)
            #write_data(proper_infos[i][0], data, index)
    except Exception, e:
        print "Error: ", e
        traceback.print_exc()

#get proper userid and weiboid
#return [[userid,weiboid]]
def get_proper_info(cookie, userids):
    print 'getting proper userid and weiboid'

    headers = {
        'User-Agent': random.choice(agents)}

    proper_infos = []
    for userid in userids:
        try:
            print userid
            url = "https://weibo.cn/u/%s?filter=1&page=1"%(userid)
            """
            html = requests.get(url, cookies=cookie).content
            """
            #print requests.get(url, cookies=cookie,).status_code
            proxy = {'http': 'http://1.119.193.36:8080'}
            html = requests.get(url, cookies=cookie,headers=headers,proxies=proxy).content
            selector = etree.HTML(html)
            info = selector.xpath("//div[@class='c']")
            is_empty = info[0].xpath("div/span[@class='ctt']")
            if is_empty:
                # get the first weibo
                for i in range(0, 1):
                    # weiboid
                    weibo_id = info[i].xpath("@id")[0]
                    str_time = info[i].xpath("div/span[@class='ct']")
                    str_time = str_time[0].xpath("string(.)").encode(
                        sys.stdout.encoding, "ignore").decode(
                        sys.stdout.encoding)
                    publish_time = str_time.split(u'来自')[0]
                    if u"刚刚" in publish_time:
                        publish_time = datetime.now().strftime(
                            '%Y-%m-%d %H:%M')
                    elif u"分钟" in publish_time:
                        minute = publish_time[:publish_time.find(u"分钟")]
                        minute = timedelta(minutes=int(minute))
                        publish_time = (
                            datetime.now() - minute).strftime(
                            "%Y-%m-%d %H:%M")
                    elif u"今天" in publish_time:
                        today = datetime.now().strftime("%Y-%m-%d")
                        #print isinstance(today, str)
                        #print len(today)
                        time = publish_time[3:]
                        publish_time = today + " " + time
                    elif u"月" in publish_time:
                        year = datetime.now().strftime("%Y")
                        month = publish_time[0:2]
                        day = publish_time[3:5]
                        time = publish_time[7:12]
                        publish_time = (year + "-" + month + "-" + day + " " + time)
                    else:
                        publish_time = publish_time[:16]

                    #print u"微博发布时间：" + publish_time
                    now_time = datetime.now().strftime('%Y-%m-%d %H:%M')
                    d_time = abs(datetime.strptime(now_time, '%Y-%m-%d %H:%M') -
                                 datetime.strptime(publish_time.strip(),'%Y-%m-%d %H:%M'))

                    # d_time between now time and the weibo created time
                    if (d_time.total_seconds() / 60 < 10):
                        print ""+str(userid)+"/"+str(weibo_id)+"/"+publish_time
                        proper_infos.append([userid, weibo_id])
                        print [userid, weibo_id]

        except Exception, e:
            print "Error: ", e
            traceback.print_exc()
            continue
    return proper_infos


#weiboid file name
#data
#index:write times
def write_data(weiboid,data,index):
    try:
        name = "csv/s%s%.csv" % (weiboid,datetime.now().strftime('%Y_%m_%d_%H_%M'))
        with codecs.open(name, 'a+', encoding='utf-8') as f:
            w = csv.writer(f, lineterminator='\n')
            for i in range(len(data)):
                w.writerow(data[i])
        print 'write ' + str(index) +' success!'
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()


def main():
    #inteval = 5minutes
    #total time about 24hours
    #get proper userid and weiboid
    filter = 1  # 值为0表示爬取全部微博（原创微博+转发微博），值为1表示只爬取原创微博

    ##test1
    param = config_reader()
    user_ids = param['userids']
    cookie = {"Cookie": ""}
    cookie['Cookie'] = param['cookie']

    proper_infos = get_proper_info(cookie, user_ids)
    print proper_infos


    ###test2
    #get about 48 hours data
    # index = 1
    # while(index < 288*10):
    #     now_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    #     print 'get --'+str(index) + '-- data from weibo after 1 minutes(' + now_time +')'
    #     s = sched.scheduler(time.time, time.sleep)
    #     #每隔一分钟爬一次
    #     s.enter(60, 1, task,())
    #     s.run()
    #     # time.sleep(2)
    #     index = index + 1

    ###test3
    #task()

if __name__ == "__main__":
    main()
