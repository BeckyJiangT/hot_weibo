#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import requests
import sys
import traceback
from lxml import etree
import urllib

from datetime import datetime
from datetime import timedelta

userids = ['2706896955', '3952070245', '2173825475', '2040909313', '2902408801', '1694061470', '1624923463', '3669102477', '2179447851', '2763325717', '2721879503', '1644806805', '1618051664', '5209478895', '1304194202', '3167571163', '3766773034', '1309302077', '1246229612', '3186727122', '1263498570', '1704091601', '1729370543', '1197191492', '5982879020', '1797054534', '2656274875', '6013682987', '1839167003', '1863847262', '1259295385', '1939178055', '1259110474', '1239246050', '6408414755', '1705586121', '1195242865', '2646681810', '1189313175', '6364325054', '2067446080', '6505916617', '1650450024', '2391195543', '5888671022', '1756505647', '2255638644', '1256857734', '2377156730', '5213724108', '1624923463', '5995175834', '3240435521', '6161856218', '3284704805', '1677856077', '1788283193', '6280362341', '5743923782', '2715025067', '1320355271', '1751675285', '1878206395', '1746263014', '1627500245', '1255623971', '1730330447', '1610536214', '3217456417', '2099181812', '1691761292', '1257355460', '3739825350', '1197191492', '1345467925', '1192148495', '1716658720', '1865476685', '1249220293', '1910171127', '1566301073', '1195230310', '1192329374', '1220924217', '1241148864', '2970192882', '2131819280', '1213536224', '1350995007', '2295389250', '1431308884', '1194026233', '1624923463', '1730726637', '1708767015', '1582160525', '1191044977', '1734808171', '1914100420', '1243667280', '1642512402\xef\xbc\x8c2909406375\xef\xbc\x8c1642591402\xef\xbc\x8c1653255165\xef\xbc\x8c2423763501\xef\xbc\x8c2032796017\xef\xbc\x8c1269870303\xef\xbc\x8c6004281123\xef\xbc\x8c1642088277\xef\xbc\x8c1806128454\xef\xbc\x8c2032796017\xef\xbc\x8c1893711543\xef\xbc\x8c1845864154\xef\xbc\x8c2580307963', '1291477752', '1270344441', '1549364094', '1645425130', '1742727537', '1262945510', '1827683445', '5454219536', '3591355593', '5234797239', '1536118323', '1582160525', '2718604160', '1340723374']
cookie = {'Cookie': '_T_WM=a9408f444cab089cc2bc357354525c59; WEIBOCN_WM=3349; H5_wentry=H5; backURL=http%3A%2F%2Fweibo.cn; ALF=1529308106; SCF=AhMRVDo8quQNYsbvLihRyFbUC1pqVT7Hyuvvj-XD4MnB3hehFHuZcs5jr8Aweg_717kd8M-qR64yIkFCfIZfqWc.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhwpjqWxh5xEac.U9PMfiFe5JpX5KMhUgL.Foe4e0qEeKMRSoB2dJLoIEXLxKML12zLB-eLxKqLB-BLBK-LxK.L1-BL1KzLxKBLB.2L1K2LxKMLB-zLB-qt; MLOGIN=1; SUB=_2A253-5QqDeRhGeBL6FoZ8ybNyjiIHXVVBzxirDV6PUJbkdANLXfxkW1NRwMFlRHc1ufcNlxrAgnmTgPUniCzkKGw; SUHB=03o1JTcXSvWtHy; SSOLoginState=1526719610'}


def test():

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    cookie = {'Cookie': 'SUB=_2A253_pt7DeRhGeBL6FoZ8ybIzTWIHXVVACUzrDV6PUJbkdANLWrxkW1NRwMGVUomTK640L8q4WS7HcWyTju74pZM;SCF=AoeMnvU411Sf5ljNDrbI2wayRRerg65vPCIYJeOZeGzx8samn9Kzz39npi3NCjv04BVp_6bFmtVInWbFXShIsuI.;SUHB=0IIVOSURYgoEuL;SSOLoginState=1526393643;_T_WM=e0aae068e1f3755c1a5fd6b53264a9f2'}
    url = "https://weibo.cn/u/2706896955?filter=1&page=1"
    # html = requests.get(url, cookies=cookie,headers=head).content
    proxy = {'http': 'http://122.241.72.191:808'}
    print requests.get(url, cookies=cookie).status_code
    html = requests.get(url, cookies=cookie, headers=headers, proxies=proxy).content

    selector = etree.HTML(html)



#get proper userid and weiboid
#return [[userid,weiboid]]
def get_proper_info(cookie, userids):
    print 'getting proper userid and weiboid'

    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    proper_infos = []
    for userid in userids:
        try:
            print userid
            #https://weibo.cn/%s/profile?filter=1&page=1
            #url = "https://weibo.cn/u/%s?filter=1&page=1"%(userid)
            url = 'https://weibo.cn/%s/profile?filter=1&page=1&display=0&retcode=6102'%(userid)
            #html = requests.get(url, cookies=cookie,headers=head).content
            proxy = {'http': 'http://122.241.72.191:808'}
            html = requests.get(url, cookies=cookie,headers=headers,proxies=proxy).content
            print html
            selector = etree.HTML(html)
            info = selector.xpath("//div[@class='c']")
            #info = selector.xpath('body/div[@class="c" and @id]')
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

        except Exception, e:
            print "Error: ", e
            traceback.print_exc()
            continue
    return proper_infos


if __name__ == '__main__':
    get_proper_info(cookie,userids)