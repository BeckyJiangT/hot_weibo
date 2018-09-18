#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division, print_function
from pyksc import dist
from pyksc import ksc

import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pylab as plt
import sys
import os
import time
import tools


'''
1. 保存数据
2. 进行预测
使用方法：ksc
'''
#数据集路径
#dataset = ['data/twitter.csv','data/phrase.csv','data/day.csv','data/night.csv']
dataset = ['data/twitter.csv','data/phrase.csv','data/result/day.csv','data/result/night.csv']

#聚类个数
cluster_k = 4

#数据集名称
items = ['twitter','phrase','day','night']
root_dir = os.path.dirname(os.path.abspath(__file__))[:-3]


#Dealing with incomplete data
# https://blog.csdn.net/u013764485/article/details/53012978
def data_pre(item):
    print ('dataset:', items[item])
    data = pd.read_csv(root_dir+os.sep+dataset[item], header=None)
    if np.isnan(data.values).any():
        data.dropna(inplace=True)
    return data


'''
1. get cent and label
2. visual cent and label
'''
def draw_ksc(item):
    data = tools.data_pre(item).values
    train_data = []
    for i in range(len(data)):
        train_data.append(data[i])

    centroid, label, shift, distc = ksc.ksc(np.array(train_data), cluster_k)
    #[centroid, label, inertia] = cluster.k_means(train_data, cluster_k)

    #sava data into the csv files
    root_path = root_dir+os.sep+'data' + os.sep +'ksc'+ os.sep + items[item] + os.sep
    print('result path:', root_path)
    if not os.path.isdir(root_path):
        os.makedirs(root_path)
        time.sleep(2)

    label_path = root_path + items[item] + '_label.csv'
    count_path = root_path + items[item] + '_count.csv'
    cent_path = root_path + items[item] + '_cent.csv'

    np.savetxt(label_path, label, delimiter=',')
    pd.value_counts(label).T.to_csv(count_path)  # value_counts()计算非空值计数的直方图。
    df = pd.DataFrame(centroid)  # T 转置; to_csv()将数据写入csv文件
    df.to_csv(cent_path,float_format='%.5f')

    index = 1
    for i in centroid:
        plt.figure(index)
        title_name = items[item] + '_ksc_' + str(index) #标题名称
        plt.title(title_name)
        pd.Series(i).plot() #画图
        path = root_dir+'data'+os.sep+'ksc'+ os.sep + items[item] + '_ksc_' + str(index) +'.png'
        plt.savefig(path) #保存
        index += 1


#prediction
#1. Random partition data[test,train]
#2. prediction by using ksc
#item 数据类别，rate 分割比例，long 测试数据长度，prelong 预测长度
def split_predict(item,rate=0.2,long=64,prelong=12):
    #item 数据类别，rate 分割比例，long 测试数据长度，prelong 预测长度
    data = data_pre(item)

    len_data = len(data)
    len_test = int(len_data * rate)
    len_train = len_data

    PBS = []
    PVS = []
    CRS = []

    data_temp = data
    for i in range(5):
        train_data = []
        test_data = []

        data = np.random.permutation(data_temp).tolist()  # 打乱数据顺序
        for i in range(len_test):
            test_data.append(data[i])
        for i in range(len_train):
            train_data.append(data[i])


        #[centroid, label_all] = cluster.k_means(train_data, cluster_k)
        centroid, label_all, shift, distc= ksc.ksc(np.array(train_data), cluster_k)
        print('ksc finish!')


        num = 0
        labels = []
        class_right = 0
        PD = []
        for i in range(len(test_data)):
            temp = test_data[i]
            td = temp[:long]
            index = 0
            label = 0
            min = sys.maxint
            num += 1

            for j in range(len(centroid)):
                index += 1
                temp = centroid[j]
                cent = temp[:long]
                dis = np.linalg.norm(td-cent)
                if dis < min:
                    label = index - 1
                    min = dis
                    t1 = centroid[j]
                    pre = t1[long:(long+prelong)] #预测结果

            if label == label_all[i]: #统计分类正确的个数
                 class_right += 1


            t2 = test_data[i]
            real = t2[long:(long+prelong)] #真实情况
            dis_p_r = np.linalg.norm(pre-real)
            PD.append(dis_p_r)
            labels.append(label)

        CRS.append(class_right)

        num = 0
        for i in PD:
            num += i
        aver = num/len(test_data)
        PB = num/(len(test_data)*1) #计算预测偏差
        PBS.append(PB)
        t = 0
        for i in PD:
            t += (i-aver)*(i-aver)
        PV = t/(len(test_data)*1) #计算预测方差
        PVS.append(PV)

        print ('1. PD result: ', PB,'2. PV result:',PV,'3. class_right:',class_right)

    num_pbs = 0
    num_pvs = 0
    num_crs = 0
    for i in PBS:
        num_pbs += i
    for j in PVS:
        num_pvs += j
    for k in CRS:
        num_crs += k

    final_PB = num_pbs/10
    final_PV = num_pvs/10
    final_CRS = num_crs/10

    print('PB = %f ,PV = %f' % (final_PB, final_PV),'class right:',final_CRS)


def main():
    #use ksc method to get center and label
    draw_ksc(2)

    #prediciton
    split_predict(2,0.2,64,24)
    split_predict(2,0.2,64,48)
    split_predict(2,0.2,64,96)
    split_predict(2,0.2,175,24)
    split_predict(2,0.2,175,48)
    split_predict(2,0.2,175,96)


if __name__ == '__main__':

    main()