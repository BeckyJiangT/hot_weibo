# -*- coding: UTF-8 -*-

'''
Python 2.X
无忧代理IP Created on 2017年08月21日
描述：本DEMO演示了使用爬虫（动态）代理IP请求网页的过程，代码使用了多线程
逻辑：每隔5秒从API接口获取IP，对于每一个IP开启一个线程去抓取网页源码
@author: www.data5u.com
'''
import urllib;
import time;
import threading;

ips = [];

# 爬数据的线程类
class CrawlThread(threading.Thread):
    def __init__(self,proxyip):
        super(CrawlThread, self).__init__();
        self.proxyip=proxyip;
    def run(self):
        # 开始计时
        start = time.time();
        # 使用代理IP请求目标网址
        html = urllib.urlopen(targetUrl, proxies={'http':'http://' + self.proxyip})
        # 转码， 如果使用的是Python 3.x版本，请去掉这行代码的注释
        # html = html.read().decode('gb2312').encode('utf-8');
        # 转码， 如果使用的是Python 2.x版本，请去掉这行代码的注释
        # html = unicode(html.read(), "gb2312").encode("utf8");
        # 结束计时
        end = time.time();
        # 输出内容
        print(threading.current_thread().getName() +  "使用代理IP, 耗时 " + str(end - start) + "毫秒 " + self.proxyip + " 获取到如下HTML内容：\n" + html + "\n*************")

# 获取代理IP的线程类
class GetIpThread(threading.Thread):
    def __init__(self,fetchSecond):
        super(GetIpThread, self).__init__();
        self.fetchSecond=fetchSecond;
    def run(self):
        global ips;
        while True:
            # 获取IP列表
            res = urllib.urlopen(apiUrl).read().strip("\n");
            # 按照\n分割获取到的IP
            ips = res.split("\n");
            # 利用每一个IP
            for proxyip in ips:
                # 开启一个线程
                CrawlThread(proxyip).start();
            # 休眠
            time.sleep(self.fetchSecond);

if __name__ == '__main__':
    # 这里填写无忧代理IP提供的API订单号（请到用户中心获取）
    order = "9f7adb42b8154668d27cfc6433d5b1c4";
    # 获取IP的API接口
    apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + order;
    # 要抓取的目标网站地址
    targetUrl = "http://ip.chinaz.com/getip.aspx";
    # 获取IP时间间隔，建议为5秒
    fetchSecond = 5;
    # 开始自动获取IP
    GetIpThread(fetchSecond).start();
