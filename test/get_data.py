# -*- coding: utf-8 -*-

import pymongo

userids = []
client = pymongo.MongoClient("localhost", 27017)
db = client["Sina"]
userAccount = db["information"]

def get_data(fan_max):
    for userid in userAccount.find():
        if int(userid['Num_Fans']) > fan_max:
        #if (int(userid['Num_Fans']) > fan_max) and (int(userid['Num_Fans']) < 2000000) :
            userids.append(userid['_id'])

    print u'',userids
    print 'fan_nums =',fan_max,':',len(userids)

if __name__=="__main__":

    # get_data(5000000)
    #get_data(2000000)
    get_data(2000000)
    # get_data(2000000)
    # get_data(1000000)





