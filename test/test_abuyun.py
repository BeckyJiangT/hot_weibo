# ! -*- encoding:utf-8 -*-

import requests

# 要访问的目标页面
targetUrl = "http://test.abuyun.com"

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "HRCL947BRW2363HD"
proxyPass = "B904C3F40C6B7DC2"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}


#agent =
cookie = {"Cookie":"SUB=_2A252B9H9DeRhGeBL6FsQ9yzPyjSIHXVVC_-1rDV6PUJbkdAKLU7AkW1NRwMGRk0KVWt75YCrr0VG9xmcoPLBFCz-;SCF=AptbUkY2wOOeiuYZ_grD09SYipaxRU6VK3iqHUHNXPyyK0DT342A2bU9TOq7c8jxuJt8Gosn_Wttn4IEPdZmQnM.;SUHB=0JvgBVIJEdailX;SSOLoginState=1526964652;_T_WM=52b16d6bef0e737c18fe57c29f8d193f"}
print proxies
resp = requests.get(targetUrl, proxies=proxies)

print resp.status_code
print resp.content