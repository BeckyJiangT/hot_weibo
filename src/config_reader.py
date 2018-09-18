#!usr/bin/env python
#coding:utf-8
from configobj import ConfigObj


def config_reader():
    config = ConfigObj('config')

    param = config['param']
    param['cookie'] = param['cookie']
    param['userids'] = param['userids']
    param['interval'] = int(param['interval'])
    param['nums_topic'] = int(param['nums_topic'])
    param['hour'] = int(param['hour'])
    param['minute'] = int(param['minute'])
    param['second'] = int(param['second'])

    param['sleeptime'] = int(param['hour'])*3600 + int(param['minute']) *60 + int(param['second'])
    param['interval_craw'] = int(param['interval_craw'])*60
    param['interval_sleep'] = int(param['interval_sleep'])

    return param


def setKeyword(keyword):
    return keyword.decode('utf-8','ignore').encode("utf-8")


if __name__ == "__main__":
    print config_reader()
    print setKeyword('胡')