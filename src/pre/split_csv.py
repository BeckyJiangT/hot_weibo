#-*-coding:utf-8 -*-

import os
import sys
import shutil
import time

'''
数据集划分
数据大小长度：doc_size > 33000
'''
cvs_file = "data"+os.sep+"csv"

def split_csv(file_path):
    root_dir = os.path.dirname(os.path.abspath(__file__))[:-3]
    files_dir = root_dir + file_path
    if not os.path.isdir(files_dir):
        print "path is error, please input right path name."
        sys.exit()

    dirs = os.listdir(files_dir) #用于返回指定的文件夹包含的文件或文件夹的名字的列表
    day_path = root_dir+'data\\split\\day' + os.sep
    night_path = root_dir+'data\\split\\night' + os.sep
    day_nums = 0
    night_nums = 0
    if not os.path.isdir(day_path):
        os.makedirs(day_path)
    else:
        shutil.rmtree(day_path)
        time.sleep(3)
        os.makedirs(day_path)


    if not os.path.isdir(night_path):
        os.makedirs(night_path)
    else:
        shutil.rmtree(night_path)
        time.sleep(3)
        os.makedirs(night_path)

    for file in dirs:
        temp = list(file)
        #get the file name (year-month-day-hour-minute-second)
        #a= int(temp[11])*10 + int(temp[12])
        files = files_dir + os.sep + file
        # state = a>=9 and a<=21
        state = True

        if state:
            names = os.listdir(files)
            for name in names:
                doc_size = int(os.path.getsize(files + os.sep + name)) #获取文件大小
                if doc_size > 30000 and doc_size < 60000 :
                    day_nums += 1
                    print 'day:' + file + '\\' + name
                    shutil.copyfile(files + os.sep + name,day_path + str(day_nums) +  '_' + name)
        else:
            names = os.listdir(files)
            for name in names:
                doc_size = int(os.path.getsize(files + os.sep + name))
                if doc_size > 30000 and doc_size < 60000:
                    night_nums += 1
                    #print 'night:' + file + '\\' + name
                    shutil.copyfile(files + os.sep + name, night_path + str(night_nums) +  '_' + name)


    print 'day total files :',day_nums,\
          'night total files:',night_nums
def main():

    split_csv(cvs_file)


if __name__ == '__main__':
    

    main()