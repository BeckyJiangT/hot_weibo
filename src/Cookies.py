#!/usr/bin/env python
# encoding: utf-8

import time
import pymongo
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
import sys
import traceback
import ast


cookies = []
client = pymongo.MongoClient("localhost", 27017)
db = client["weibo"]
userAccount = db["userAccount"]


def read_account(name):
    if not os.path.isfile(name):
        print("File path {} does not exist. Exiting...".format(name))
        sys.exit()

    accounts = []
    try:
        account_file = open(name, "r")
        line = account_file.readline().strip('\n')
        cnt = 0
        while len(line) > 10:
            if len(line) < 10:
                continue
            accounts.append( ast.literal_eval(line))
            cnt += 1
            line = account_file.readline().strip('\n')
        print 'total account :',cnt

    except Exception, e:
        print "Error: ", e
        traceback.print_exc()
    finally:
        account_file.close()

    return accounts



def init_cookies():
    for cookie in userAccount.find():
        cookies.append(cookie['cookie'])


"""
将强制设置时间设置为显示设置时间
time.sleep(XXX)
WebDriverWait(driver, XXX).until(EC.presence_of_element_located((By.ID, "elementname")))
"""
def get_cookie(username, password):
    driver = webdriver.Chrome()
    driver.get("https://passport.weibo.cn/signin/login?")
    #driver.get('https://passport.weibo.cn/signin/login?entry=mweibo&r=https://weibo.cn/')
    elem_user = WebDriverWait(driver,5).until(
        EC.visibility_of_element_located((By.ID,"loginName"))
    )
    elem_user.send_keys(username)
    elem_pwd = WebDriverWait(driver,5).until(
        EC.visibility_of_element_located((By.ID,"loginPassword"))
    )
    elem_pwd.send_keys(password)
    elem_sub = WebDriverWait(driver,5).until(
        EC.visibility_of_element_located((By.ID,"loginAction"))
    )
    elem_sub.click()
    #driver.implicitly_wait(3)
    time.sleep(5)
    cookies = driver.get_cookies()
    cookie = [item["name"] + "=" + item["value"] for item in cookies]
    cookiestr = ';'.join(item for item in cookie)  # 处理cookie使其格式与标题头中要求一致
    #print cookiestr
    driver.close()
    return cookiestr

if __name__ == "__main__":
    correct_account = []
    try:
        userAccount.drop()
        WeiBoAccounts = read_account('account.txt')
        #print WeiBoAccounts
    except Exception as e:
        pass
    for account in WeiBoAccounts:
        cookie = get_cookie(account["username"], account["password"])
        if len(cookie) < 100:
            print 'error account:',account["username"],account["password"]
            continue
        userAccount.insert_one({"id": account["username"], "cookie": cookie})
        print cookie
        correct_account.append(account)

    print correct_account
