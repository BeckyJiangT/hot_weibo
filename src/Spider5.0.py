#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import traceback
from config_reader import config_reader
from Spider import Weibo
from datetime import datetime
import codecs
import csv
import sched
import time
import thread
import logging
import sys
import random
import Spider
import requests
from lxml import etree

from Cookies import cookies, init_cookies
#every half of hour check,every five minutes crawing
#craw total time 24 hours

# global parama
logging.basicConfig(filename="log/log4.0.log",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
param = config_reader()
user_ids = param['userids']
cookie = {"Cookie": ""}
cookie['Cookie'] = param['cookie']
###cookie['Cookie']="M_WEIBOCN_PARAMS=uicode%3D20000174;SUB=_2A25382EHDeRhGeBL71cU-CfNzj6IHXVVHA9PrDV6PUJbkdAKLRX9kW1NRxjKJAlu9pO4UcQqdMUxBnym-8bTN6uL;SCF=AlSZUt5Kwzd9E9HUUN6HnCi0m7PSXRuH_bo3rvyryMBGK3_ZNcaQoF11A_qGwuwBJ_x_AIg0PE0oaBm-jgzJ95I.;SUHB=0gHi5SHt6NyUzR;SSOLoginState=1526141271;_T_WM=d64bfe6ec7ad787cc71fba980399b475"
total_process = 0

# main (main process)
def main():
    total_nums = 0  # the total get data with the get_proper_info
    global total_process
    total_process = 0  # the thread number [1,24]
    while True:
        print 'main processs ' + str(total_process)
        if total_process < 0:
            logging.info('error while break!')
            break

        #creat total thread [0,32]
        while total_process > 36:
            time.sleep(param['interval_sleep'])
            logging.info('thread is more than 24 ,main thread is sleeping')
            if total_process > 36:
                continue
            else:
                break

        try:
            #proper_infos = [['1618051664', 'M_GdRqs5xJH']]
            """
            cookie=get_cookie()
            proper_infos = Spider.get_proper_info(cookie, user_ids)
            """
            #print user_ids
            proper_infos = Spider.get_proper_info(get_cookie(),user_ids)
            #proper_infos = Spider.get_proper_info(cookie, user_ids)

            if proper_infos:
                # proper_infos is not null
                total_nums += 1
                current_time = str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
                logging.info('get proper_infos is not null')
                path_dir = os.path.split(os.path.realpath(__file__))[0] + os.sep + "csv" + os.sep + current_time
                if not os.path.isdir(path_dir):
                    os.mkdir(path_dir)
                # path_name = path_name+os.sep+current_time
                logging.info(proper_infos)
                thread.start_new_thread(task, (proper_infos, current_time, total_nums))
                total_process += 1
                print "thread:" + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                for i in range(param['interval_sleep']/2):
                    time.sleep(param['interval_sleep'])
                    logging.info('main thread is sleepping' + ' and proper_infos is not null')
                    print 'main thread is sleepping' + ' and proper_infos is not null'
                    print 'main processs ' + str(total_process)
            else:
                # proper_infos is null
                logging.info(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ' get proper_infos is null')
                for i in range(param['interval_sleep']/2):
                    time.sleep(param['interval_sleep'])
                    logging.info('main thread is sleepping' + ' and proper_infos is null')
                    print 'main thread is sleepping' + ' and proper_infos is null'
                    print 'main processs ' + str(total_process)
                continue

        except Exception as e:
            logging.error(str(e))
            logging.error(traceback.format_exc())
            continue


# start thread run gettting data next
# task_id is the number of task(thread)
# index control the thread run time
# when index = 1, save userinfo and weibo info into total.csv
# get the total gettting data, including every user has many data
def task(proper_infos, path_name, task_id):
    global total_process
    index = 1
    # crawer total time (1440 minutes = 24 hours)
    while (index < param['interval_craw']):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        #print str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        logging.info('get --' + str(index) + '-- data from weibo after 1 minutes')
        s = sched.scheduler(time.time, time.sleep)
        s.enter(0, 1, get_data_task, (proper_infos, path_name, index))
        s.run()
        # every thread run interval time (60 seconds = 1 minutes)
        #time.sleep [300-5,300+5]
        time.sleep(5*param['interval_sleep'] + random.randint(-5,5))
        index = index + 5
        logging.info('task ' + str(task_id) + 'get data!')
    logging.info(str(task_id) + 'thread is ended')
    total_process -= 1



# getting user and weibo data(up_num,retweet_num,comment_num) with proper_infos
# proper_infos must be not null
### weibo_num,following,follower could be used to caculte every user's pageRank

def get_data_task(proper_infos, path_name, index):
    try:
        # filter = 0 is all weibo,filter = 1 is all original weibo
        filter = 1
        for i in range(len(proper_infos)):
            # invoke weibo class, create weibo instance
            wb = Weibo(int(proper_infos[i][0]), filter)

            """
            get_cookie()
            wb.cookie['Cookie'] = param['cookie']
            """
            #wb.cookie['Cookie'] = param['cookie']
            wb.cookie['Cookie'] = get_cookie()['Cookie']
            wb.start_data(proper_infos[i][1])
            now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            ###INFO
            # print u"用户名：" + wb.username
            # print u"全部微博数：" + str(wb.weibo_num)
            # print u"关注数：" + str(wb.following)
            # print u"粉丝数：" + str(wb.followers)

            write_data(proper_infos[i][0],
                       [wb.up_num[0], 
                       wb.retweet_num[0], 
                       wb.comment_num[0], 
                       now_time],
                       path_name)
            if index == 1:
                # user_name = u"username"+wb.username
                # user_name.encode(sys.stdout.encoding).split()
                # user_name
                write_total_data([wb.weibo_num,
                                  wb.following,
                                  wb.followers,
                                  proper_infos[i][0],
                                  proper_infos[i][1],
                                  now_time])


                ###INFO
                # result = (u"微博数:"+wb.weibo_num+"\n"+
                #           u"关注数:"+wb.following+"\n"+
                #           u"粉丝数:"+wb.followers+"\n"+
                #           u"用户ID:"+proper_infos[i][0]+"\n"+
                #           u"微博ID:"+proper_infos[i][1]+"\n"+
                #           u"时间  :"+now_time)
                # write_txt(result)
    except Exception, e:
        logging.error(str(e))
        logging.error(traceback.format_exc())

# save total data
def write_txt(result):
    try:
        name = "csv/total.txt"
        f = open(name, 'wb')
        f.write(result.encode(sys.stdout.encoding))
        f.close
    except Exception as e:
        logging.error(str(e))
        logging.error(traceback.format_exc())

# save total data
def write_data(userid, data, path_name):
    try:
        name = "csv/%s/%s.csv" % (path_name, userid)
        with codecs.open(name, 'a+', encoding='utf-8') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(data)
    except Exception as e:
        logging.error(str(e))
        logging.error(traceback.format_exc())


def write_total_data(data):
    try:
        name = "csv/total.csv"
        with codecs.open(name, 'a+', encoding='utf-8') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(data)
    except Exception as e:
        logging.error(str(e))
        logging.error(traceback.format_exc())


#从数据库中获取cookie
#首先对获取得到的cookie是否可以使用，如果随机3次获得的cookie都无法使用，就启动重新获取获取cookie
#获取cookie启动程序
#2803301701 今日头条
def get_cookie():
    init_cookies()
    while(True):
        cookie = {"Cookie": ""}
        cnt = 0#cookie重新生产出发命令
        cookie['Cookie'] = random.choice(cookies)
        url = "https://weibo.cn/u/%s?filter=1&page=1" % (2803301701)
        if(requests.get(url,cookies=cookie).status_code == 200):
            #print cookie
            return cookie
        else:
            cnt += 1
            if(cnt == 5):
                print 'most of cookies are error!'
                logging.error('most of cookies are error!')
                ##启动获取get_cookie的程序

            continue

    return cookie

def test_cookie():
    init_cookies()
    proper_infos = [['1618051664', 'M_GdRqs5xJH']]
    total_nums = 1
    current_time = str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    task(proper_infos,current_time,total_nums)

if __name__ == "__main__":
    main()
    #test_cookie()
