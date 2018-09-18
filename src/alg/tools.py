#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import os

#数据集名称
items = ['twitter','phrase','day','night']
root_dir = os.path.dirname(os.path.abspath(__file__))[:-3]
dataset = ['data/twitter.csv','data/phrase.csv','data/result/day.csv','data/result/night.csv']

# 处理丢失的数据
# 判断数据是否完整
# https://blog.csdn.net/u013764485/article/details/53012978
def data_pre(item):
    print dataset[item]
    data = pd.read_csv(root_dir+os.sep+dataset[item], header=None)
    if np.isnan(data.values).any():
        data.dropna(inplace=True)
    return data