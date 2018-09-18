#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import traceback

"""
将微博账号转成需要的格式
原始格式：
    0033676673808----dgw969095l
    00557172553686----jwz137481t
转换后的格式：
    {'username': '14609407645', 'password': 'sm341859y'},
    {'username': '13441080409', 'password': 'sz598074a'},
转换备注：
    其中username和password可以修改
"""

"""
src:original file txt path and name
dist:convert account save to file
name_labe:'username'
pass_label:'password'
"""

def convert(src,dist,name_labe,pass_label):

    if not os.path.isfile(src):
        print("File path {} does not exist. Exiting...".format(src))
        sys.exit()

    account = []
    try:
        src_file = open(src, "r")
        dist_file = open(dist, "w")
        line = src_file.readline().strip('\n')
        print line
        cnt = 0
        while len(line) > 10:
            temp = {}
            temp[name_labe] = line[:line.find('-')]
            temp[pass_label] = line[line.rfind('-')+1:]
            account.append(temp)
            cnt += 1
            line = src_file.readline().strip('\n')
        print 'total account :',cnt

        dist_file.writelines(["%s\n" % item for item in account])
    except Exception, e:
        print "Error: ", e
        traceback.print_exc()
    finally:
        src_file.close()
        dist_file.close()

if __name__ == "__main__":
    convert('original.txt','account.txt','no','psw')
