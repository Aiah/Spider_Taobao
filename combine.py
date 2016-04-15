# -*- coding: utf-8 -*-
# filename: combine.py
# Author: 'Aiah'
# time: 2016/4/15 11:10

import os

def combineReviews(path):
    dirList = os.listdir(path)
    for dir in dirList:
        nid = dir.split("&")[1].split("=")[1] # 获取nid
        # 在'E:/program/Python/spam_detection/comment'下创建文件名为nid的文件夹，其内部为1，0，-1三个txt文件，分别为好评，中评，差评
        combinePath = 'E:/program/Python/spam_detection/comment/{}/'.format(nid) # 文件夹
        os.mkdir(combinePath)
        # 创建nid文件夹下的"1.txt","0.txt","-1.txt"

        combinedPath = 'E:/program/Python/spam_detection/comments/{}/'.format(dir)
        fileList = os.listdir(combinedPath)
        for file in fileList: # file为comment&nid={}文件夹下的txt文件
            # 读file文件的内容
            review = open(combinedPath+file, 'r')
            reviews = review.readlines()
            review.close()
            rate = file.split('.')[0].split('%')[1]
            Path = open(combinePath+rate+'.txt', 'a+')
            Path.writelines(reviews)
            Path.close()

if __name__ == "__main__":
    path = 'E:/program/Python/spam_detection/comments/'
    combineReviews(path)
