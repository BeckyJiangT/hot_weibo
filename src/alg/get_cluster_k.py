#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from sklearn import cluster
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cdist


dataset = ['data/twitter.csv','data/phrase.csv','data/day.csv','data/night.csv']

#确定聚类个数K
def determine_k(item):
    print ''
    nums = 10 #平均轮廓系数计算次数
    max_k = 10
    min_k = 2
    result = [0] * (max_k-min_k)
    data = data_pre(item)
    for j in range(nums):
        scs = []
        for i in range(min_k,max_k):
            [centroid, label, inertia] = cluster.k_means(data, i)
            sc = silhouette_score(data, label, metric='euclidean')  # 平均轮廓系数
            scs.append(sc)
            result[i-min_k] += sc


    for i in range(len(scs)):
        result[i] = result[i] / nums
    temp = pd.DataFrame(result)
    temp.to_csv('data/Silhouette'+str(item)+'.csv',index=False)#index设置是否显示行号

    plt.plot(result,'rx-')
    plt.title('scs'+str(nums))
    plt.xlabel('the numbers of clusters')
    plt.ylabel('Silhouette Coefficient')
    plt.savefig('img/Silhouette Coefficient.png')
    #plt.show()
    plt.close()


# 处理丢失的数据
# 判断数据是否完整
# https://blog.csdn.net/u013764485/article/details/53012978
def data_pre(item):
    print dataset[item]
    data = pd.read_csv(dataset[item], header=None)
    if np.isnan(data.values).any():
        data.dropna(inplace=True)
    return data

#平均畸变程求解函数
def get_cluster(item):
    data = data_pre(item)
    # data = dataset(item)
    aa = []
    K = range(1, 10)
    for k in range(1, 10):
        kmeans = cluster.KMeans(n_clusters=k)
        kmeans.fit(data)
        aa.append(sum(np.min(cdist(data, kmeans.cluster_centers_, 'euclidean'), axis=1)) / data.shape[0])
    plt.figure()
    plt.plot(np.array(K), aa, 'rx-')
    plt.xlabel('the numbers of clusters')
    plt.ylabel('Average distortion degree')
    #plt.show()
    plt.savefig('img/distortion_degree.png')
    plt.close()
    print('success')

def main():
    determine_k(2)
    get_cluster(2)

if __name__ == '__main__':
        main()