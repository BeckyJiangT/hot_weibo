#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import traceback
from config_reader import config_reader
from datetime import datetime
import codecs
import csv
import sched
import time
import thread
import logging
import requests
import json

#every half of hour check,every five minutes crawing
#craw total time 12 hours

# global parama
logging.basicConfig(filename="log/log.log",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
param = config_reader()
user_ids = param['userids']

total_process = 1   # the thread numbers [1,100]
total_datas = 0 # the total numbers get data
total_nums = 1  # the total numbers of running get_proper_info


# main (main process)
def main():
    global total_nums
    global total_datas
    global total_process

    try:
        headers = ['userid', 'weibo_id', 'publish_time']
        name = "csv/total.csv"
        with codecs.open(name, 'a+', encoding='utf-8') as f:
            f_csv = csv.DictWriter(f,headers)
            f_csv.writeheader()
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()


    while True:
        print 'main processs ' + str(total_process)
        if total_process < 0:
            logging.info('error while break!')
            break
        while total_process > 100:
            time.sleep(param['interval_sleep'])
            logging.info('thread is more than 24 ,main thread is sleeping')
            if total_process > 100:
                continue
            else:
                break

        try:
            #proper_infos = ['4242559120744828','4241775763930801','4242425247350121']
            proper_infos,total_infos = get_proper_info(user_ids,total_nums)

            if proper_infos:
                # proper_infos is not null
                total_nums += 1
                total_datas += len(proper_infos)
                write_total_data(total_infos)
                current_time = str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
                logging.info('get proper_infos is not null')
                path_dir = os.path.split(os.path.realpath(__file__))[0] + os.sep + "csv" + os.sep + current_time
                if not os.path.isdir(path_dir):
                    os.mkdir(path_dir)
                # path_name = path_name+os.sep+current_time
                logging.info(proper_infos)
                thread.start_new_thread(task, (proper_infos, current_time, total_nums))
                total_process += 1
                #print "thread:" + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                for i in range(param['interval_sleep']/12):
                    time.sleep(param['interval_sleep'])
                    logging.info('main thread is sleepping'+'total processs:'+str(total_process)+' and proper_infos is not null')
                    print '1. running 2. get_proper_infos:', total_nums, ' 3.total threads:', total_process, ' 4. total get datas:', total_datas
            else:
                # proper_infos is null
                logging.info(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ' get proper_infos is null')
                for i in range(param['interval_sleep']/12):
                    time.sleep(param['interval_sleep'])
                    logging.info('main thread is sleepping'+'total processs:'+str(total_process)+' and proper_infos is null')
                    print '1. sleeping 2. get_proper_infos:', total_nums, ' 3.total threads:', total_process, ' 4. total get datas:', total_datas
                continue

        except Exception as e:
            logging.error(str(e))
            logging.error(traceback.format_exc())
            continue


# start thread run gettting data next
# task_id is the number of task(thread)
def task(proper_infos, path_name, task_id):
    global total_process
    global total_datas
    index = 1
    # crawer total time (720 minutes = 12 hours)
    while (index < param['interval_craw']):
        logging.info('get --' + str(index) + '-- data from weibo after 1 minutes')
        s = sched.scheduler(time.time, time.sleep)
        s.enter(0, 1, get_data_task, (proper_infos, path_name))
        s.run()
        # every thread run interval time (300 seconds = 5 minutes)
        time.sleep(60)
        #time.sleep(1*param['interval_sleep'] + random.randint(-5,5))
        index = index + 1
        logging.info('task ' + str(task_id) + 'get data!')
    logging.info(str(task_id) + 'thread is ended')
    total_datas -= len(proper_infos)
    total_process -= 1



# getting user and weibo data(up_num,retweet_num,comment_num) with proper_infos
# proper_infos must be not null
def get_data_task(proper_infos, path_name):
    try:
        #print proper_infos
        url = 'http://118.89.219.191:8092/weibo_counts?name=Andrew&pwd=Andrew768&ids=%s' % (','.join(proper_infos))
        data = json.loads(requests.get(url).content)
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i in range(len(data)):
            write_data(proper_infos[i],
                       [data[i]['attitudes'],
                        data[i]['reposts'],
                        data[i]['comments'],
                        str(proper_infos[i]),
                        now_time],
                        path_name)
    except Exception, e:
        print "Error: ", e
        traceback.print_exc()
        logging.error(str(e))
        logging.error(traceback.format_exc())


# save total data
def write_data(weiboid, data, path_name):
    try:
        name = "csv/%s/%s.csv" % (path_name, weiboid)
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
            headers = ['userid', 'weibo_id', 'publish_time','index']
            f_csv = csv.DictWriter(f, headers)
            f_csv.writerows(data)
    except Exception as e:
        logging.error(str(e))
        logging.error(traceback.format_exc())



#get proper userid and weiboid
#return [[userid,weiip]]
def get_proper_info(userids,index):
    print 'getting proper userid and weiboid'
    proper_infos = []
    total_infos = []
    for userid in userids:
        try:
            # the first api
            url = "http://118.89.219.191:8092/user_weibo?name=Andrew&pwd=Andrew768&uid=%s"%(userid)
            result = json.loads(requests.get(url).content)
            GMT_FORMAT = '%a %b %d %H:%M:%S %Y'
            #print userid
            if result['statuses']:
                publish_time = datetime.strptime(result['statuses'][0]['created_at'].replace('+0800 ', ''), GMT_FORMAT)
                weibo_id = result['statuses'][0]['id']
                publish_time = datetime.strftime(publish_time,'%Y-%m-%d %H:%M')
                #print userid,weibo_id,publish_time
                now_time = datetime.now().strftime('%Y-%m-%d %H:%M')

                d_time = abs(datetime.strptime(now_time, '%Y-%m-%d %H:%M') -
                                datetime.strptime(publish_time.strip(),'%Y-%m-%d %H:%M'))

                # d_time between now time and the weibo created time
                if (d_time.total_seconds() / 60 < 10):
                    print "合法:"+str(userid)+"/"+str(weibo_id)+"/"+publish_time
                    proper_infos.append(str(weibo_id))
                    temp = {}
                    temp['userid'] = userid
                    temp['weibo_id'] =str(weibo_id)
                    temp['publish_time']=publish_time
                    temp['index'] = index
                    total_infos.append(temp)
        except Exception, e:
            continue

    print 'total userids',len(proper_infos)
    temp_proper_infos = []
    temp_total_infos = []
    try:
        #print proper_infos
        url = 'http://118.89.219.191:8092/weibo_counts?name=Andrew&pwd=Andrew768&ids=%s' % (','.join(proper_infos))
        data = json.loads(requests.get(url).content)
        for i in range(len(data)):
            #print int(data[i]['attitudes'])
            if int(data[i]['attitudes']) > 5:
                temp_proper_infos.append(proper_infos[i])
                temp_total_infos.append(total_infos[i])
    except Exception, e:
        #print "Error: ", e
        #traceback.print_exc()
        logging.error(str(e))
        logging.error(traceback.format_exc())

    print 'proper userids:',temp_proper_infos
    return temp_proper_infos,temp_total_infos


if __name__ == "__main__":
    main()
