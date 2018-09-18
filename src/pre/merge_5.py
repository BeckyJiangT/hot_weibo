#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import pandas as pd
import numpy as np
from scipy.signal._savitzky_golay import savgol_filter
import matplotlib.pyplot as plt
import shutil
import time
"""
通过split分隔之后运行
合并数据
变化量
座高峰对齐
"""
# cvs_file = "data"+os.sep+"split" + os.sep + 'day'
# result_file="data"+os.sep+"result"+os.sep+"merge_3.csv"
# img_file = "data"+os.sep + "img"
# all_file = "data" + os.sep + "result" + os.sep + "all" + os.sep
# root_dir = os.path.dirname(os.path.abspath(__file__))[:-3]
# #length: the size of scraw data

def merge_data(file_path,length = 144,step = 1):
    root_dir = os.path.dirname(os.path.abspath(__file__))[:-3]
    files_dir = root_dir + file_path
    if not os.path.isdir(files_dir):
        print "path is error, please input right path name."
        sys.exit()

    print 'start data pre progress:'
    files_num = 0
    file_num = 0
    all_num = 0 #总共有多少数据集
    results=[]
    results_maxs = []
    results_maxs_index = []

    if os.path.isdir(files_dir):
        files_num += 1
        names = os.listdir(files_dir)
        for name in names:
            attentions=[]
            datas = pd.read_csv(files_dir+os.sep+name,header=None).values
            if len(datas) > 3:#clear the empty data
                all_num += 1
                len_datas = len(datas)-1
                #clear useless data
                if datas[len_datas][1] + datas[len_datas][2] < 50:
                    continue

                #0. is or not normalize data
                datas = normal_score(datas,step=step)
                for data in datas:
                    attentions.append(cal_score(data[:3]))  #获得关注度

                #1. is or not smooth
                attentions = resize_score(attentions,length=length)
                attentions = data_smooth(attentions, name,file_num)
                results_max_index = np.argmax(attentions) + 1

                #delete the peak = 1
                if results_max_index > 1:
                    print name
                    results.append(attentions)
                    results_maxs.append(max(attentions))
                    results_maxs_index.append(results_max_index)
                    file_num += 1

                #2. is or not copy file
                #copy file
                shutil.copyfile(files_dir + os.sep + name, all_dir + str(file_num) + '_' + name)
            else:
                print '------------------------file: ' + name + 'is error!------------------------'

    print len(results)
    #is or not peak_alignment
    peak = data_dist(results_maxs_index)
    results = peak_data(results,peak)

    #控制小数的位数
    plt.figure(1)
    for i in range(len(results)):
        for j in range(len(results[i])):
            results[i][j] = round(results[i][j],5)
        plt.plot(results[i])
    plt.xlabel('time series')
    plt.ylabel('attentions')
    plt.title('all data attentions')
    #plt.show()

    plt.savefig(root_dir+"data"+os.sep+"result"+os.sep+ 'day_' +str(step) + ".png",dpi=1200)
    plt.close()


    pd.DataFrame(results).to_csv(root_dir+result_file,header=None,index=False)
    print 'total files->'+ str(all_num) + '\n' \
          + 'proper result path->'+ files_dir + '\n' \
          + 'proper total dirs->'+ str(files_num) + '\n' \
          + 'proper total files->' + str(file_num)



#get attention
#data[up_num,retweet_num,comment_num]
def cal_score(data):
    #return math.log10(data[0] + 0.01) + 2 * data[1] + data[2] - math.log10(0.01)
    return 2 * data[1] + data[2]


#caculate changing vaiance of attention
def resize_score(data,length=144):
    data = np.subtract(data[1:],data[:len(data)-1])#两个数组相减
    data_len = len(data)
    if data_len>length:
        return data[:length]
    else:
        temp=np.zeros(length,dtype=float).tolist()
        temp[:data_len]=data
        return temp

#normailze data
def normal_score(datas,step = 1):
    if len(datas[0]) < 3:
        print 'input data error in normal_score!'
        sys.exit()
    else:
        #get data use step
        j = 0
        temps = []

        for i in range(0,len(datas),step):
            temp = []
            # a=len(datas)
            # print(a)
            for k in range(len(datas[i])):
                temp.append(datas[i][k])
            temps.append(temp)
        datas = temps

        maxs = []
        mins = []
        for col in range(3):
            temp = column(datas,col)
            maxs.append(max(temp))
            mins.append(min(temp))

        for col in range(len(maxs)):
            if maxs[col] == 0 or maxs[col] == mins[col]:
                continue
            for row in range(len(datas)):
                datas[row][col] = (datas[row][col]- mins[col])*1.0 / (maxs[col]-mins[col]) * 100
                #datas[row][col] = datas[row][col]
    return datas


def column(matrix, i):
    return [row[i] for row in matrix]


#get the peak of the attentions
def data_dist(data):
    #visual data by cicle plot
    f,ax = plt.subplots(1,1,figsize=(12,12))#图表的整个绘图区域被分成 numRows 行和 numCols 列
                                           #plotNum 参数指定创建的 Axes 对象所在的区域
    temp = pd.value_counts(data,sort=True)
    temp.plot.pie(autopct='%1.1f%%',ax=ax,shadow=True,startangle=90)
    ax.set_title('time series max')
    ax.set_ylabel('mximum index distribution')
    #plt.show()
    plt.savefig(img_file)
    plt.close()

    #get max index and caculate the peak
    temps = temp.values
    # total = sum(temps)*0.85
    total = sum(temps)
    d = 0
    total_peak = 0
    for i in range(len(temps)):
        d += temps[i]
        total_peak += temps[i]*temp._index[i]
        if d >= total:
            #average_peak = (int)((sum(temp._index[:i+1]))/i+1) #算出最高峰值对应的索引
            average_peak = total_peak/d
            #print temp._index[:i+1]
            print 'peak index',average_peak
            break
        continue

    return average_peak

#peak alignment
def peak_data(data,peak):
    for i in range(len(data)):

        plt.figure(0)
        plt.plot(data[i],label='Before peak alignment')

        max_index = np.argmax(data[i])
        if max_index >= peak:
            dist = max_index - peak #需要移动的数量单位
            total = len(data[i])
            data[i][:total-dist] = data[i][dist:]
            for k in range(dist):
                data[i][total-dist + k] = 0
        else:
            dist = abs(max_index - peak)
            total = len(data[i])
            data[i][dist:] = data[i][:total-dist]
            for k in range(dist):
                data[i][k] = 0
        # visual
        print str(i+1) + '.png'
        plt.plot(data[i], color='red',label='After peak alignment')
        #plt.show()
        plt.xlabel('time series')
        plt.ylabel('attentions')
        plt.title('data peak alignment')
        plt.legend(loc='upper right')
        plt.savefig(peak_dir + str(i+1))
        plt.close(0)

    return data

#smooth the attention
def data_smooth(data,name,file_num):

    plt.figure(0)
    plt.plot(data,label='Before smoothing')
    data = savgol_filter(data, 31, 3)
    plt.plot(data, color='red',label='After smoothing')
    plt.xlabel('time series')
    plt.ylabel('attentions')
    plt.title('data smoothing')
    plt.legend(loc='upper right')
    plt.savefig(all_file + str(file_num+1) +"_" + name + ".png")
    plt.close(0)

    return data
    # datas = savgol_filter(data, 31, 3)
    # for i in range(len(datas)):
    #     if datas[i]< 0:
    #         datas[i] = 0
    # return datas


#init parameter
def init(name):
    results = []
    root_dirs = os.path.dirname(os.path.abspath(__file__))[:-3]
    #0 cvs_file
    results.append("data"+os.sep+"split" + os.sep + name)

    #1 result_file
    results.append("data"+os.sep+"result"+os.sep+ name + ".csv")

    #2 img_file
    results.append(root_dirs + "data"+os.sep + "result" + os.sep + "peak" + os.sep + name + '.png')

    #3 all_file
    results.append(root_dirs+"data" + os.sep + "result" + os.sep + "img"  + os.sep + name + os.sep)
    if not os.path.isdir(results[3]):
        os.makedirs(results[3])
    else:
        shutil.rmtree(results[3])
        time.sleep(3)
        os.makedirs(results[3])

    #4 all_dir
    results.append(root_dirs + "data" + os.sep + "result" + os.sep + "all" + os.sep + name + os.sep)
    if not os.path.isdir(results[4]):
        os.makedirs(results[4])
    else:
        shutil.rmtree(results[4])
        time.sleep(3)
        os.makedirs(results[4])


    #5
    results.append(root_dirs+"data" + os.sep + "result" + os.sep + "img"  + os.sep + "peak" + os.sep + name + os.sep)
    if not os.path.isdir(results[5]):
        time.sleep(1)
        os.makedirs(results[5])
    else:
        shutil.rmtree(results[5])
        time.sleep(1)
        os.makedirs(results[5])

    return results


if __name__ == "__main__":
    results = init('day')
    if results:
        cvs_file = results[0] #read the scv file about including the weibo infos
        result_file = results[1]#the result root path
        img_file = results[2] #the stastic result path
        all_file = results[3] #the smooth visual result imgs path
        all_dir = results[4] #save the copy fils
        peak_dir = results[5] #save visual aftering peak alignment

        step = 2
        len_data = 700/step
        merge_data(cvs_file, length=len_data, step = step)
    else:
        print 'parameter error!'