# -*- coding: utf-8 -*-
# filename: crawl.py
# Author: 'Aiah'
# time: 2016/4/9 15:24

import time
import random
import requests as rq
import re
import pandas as pd
import sys
import os
from selenium import webdriver
driver = webdriver.PhantomJS()

# 配置utf-8输出环境
reload(sys)
sys.setdefaultencoding("utf-8")

def getids():
    oriURL = 'https://s.taobao.com/list?spm=a21bo.50862.201867-links-0.4.If9I5U&style=grid&seller_type=taobao&cps=yes&cat=51108009&sort=sale-desc'
    doc = rq.get(oriURL)
    # 正则表达式表示的是找到方括号及方括号里面的内容，即(\[.*?\])
    auctions = re.findall('\"auctions\":(\[.*?\])\,\"recommendAuctions\"', doc.text)[0]
    auctionJson = pd.read_json(auctions)
    # auctionJson.to_csv('auctions.txt')
    nids = auctionJson['nid']
    userids = auctionJson['user_id']
    output = open('ids.txt', 'w')
    for i in range(len(nids)-2):
        output.writelines(str(nids[i])+' '+str(userids[i])+'\n')
    output.write(str(nids[len(nids)-1])+' '+str(userids[len(nids)-1]))

# 可以读取商品nid，商家user_id
def readfile(file):
    lines = []
    content = open(file, 'r')
    for line in content.readlines():
        ct = line.strip('\n').split(' ') # nid user_id
        lines.append(ct)
    return lines

def getreview(nid, user_id, pagenum, ratetype):
    KsTS = str(int(time.time()*1000))+'_'+str(random.randint(1000, 9999))
    rateUrl = 'https://rate.taobao.com/feedRateList.htm?_ksTS={}&auctionNumId={}&userNumId={}&currentPageNum={}&pageSize=20&rateType={}&orderType=sort_weight&showContent=1&attribute=&folded=0&callback&ua=&callback=jsonp_reviews_list'.format(KsTS, nid, user_id, pagenum, ratetype)
    print(rateUrl)
    driver.get(rateUrl)
    current = driver.current_url
    count = 0
    content1 = driver.find_element_by_tag_name("body").text
    while current[8:11] == 'sec' or content1 == 'jsonp_reviews_list({"status":1111,"wait":5})':
        count += 1
        driver.get(rateUrl)
        current = driver.current_url
        content1 = driver.find_element_by_tag_name("body").text
        time.sleep(random.randint(1, 3))
        if count == 6:
            print('Have Been Found!! Rest for 20 minutes')
            time.sleep(1200)
            count = 0
    content = driver.find_element_by_tag_name("body").text
    return content

def getcontent(page):
    maxpage = re.compile('\"maxPage\":(\d+)\,')
    # 最大页数
    maxPage = maxpage.findall(page)[0]
    appendlist = re.compile('\"appendList\":\[(.*?)\]\,\"from\"')
    # 追加评论
    appendLists = appendlist.findall(page)
    for i in range(len(appendLists)):
        if appendLists[i] != '':
            appendreview = re.compile('\"content\":\"(.*?)\"\,\"vicious\"')
            appendLists[i] = appendreview.findall(appendLists[i])
    date = re.compile('\"date\":\"(.*?)\"\,\"dayAfterConfirm\"')
    # 评论时间
    Date = date.findall(page)
    review = re.compile('\"serviceRate\":.*?\,\"content\":\"(.*?)\"\,\"photos\"')
    # 评论内容
    Review = review.findall(page)
    rank = re.compile('\"rank\":(\d+)\,\"nick\"')
    # 等级
    Rank = rank.findall(page)
    nick = re.compile('\"nick\":\"(.*?)\"\,\"userId\"')
    # 评论内容
    Nick = nick.findall(page)
    return maxPage, Date, Review, Rank, Nick, appendLists

def action():
    ids = readfile('ids.txt')
    pagenum = 1
    ratetype = 1
    for i in range(0, len(ids)):
        while 1:
            content = getreview(ids[i][0], ids[i][1], pagenum, ratetype).encode('utf8')
            print('complete:{}, {}, {}'.format(ids[i], pagenum, ratetype))
            filename = open('E:/program/Python/spam_detection/comments/comment&nid={}/{}%{}.txt'.format(ids[i][0], pagenum, ratetype), 'w')
            maxpage, date, review, rank, nick, appendLists= getcontent(content)
            for j in range(len(date)):
                if appendLists[j] == '':
                    filename.write(nick[j]+'\t'+rank[j]+'\t'+date[j]+'\t'+review[j]+'\n')
                else:
                    appendContent = 'appendContent:'
                    for appendreview in appendLists[j]:
                        appendContent += appendreview+'\t'
                    filename.write(nick[j]+'\t'+rank[j]+'\t'+date[j]+'\t'+review[j]+'\t'+appendContent+'\n')
            filename.close()
            print(pagenum, maxpage)
            if pagenum < int(maxpage):
                pagenum += 1
            else:
                pagenum = 1
                if ratetype != -1:
                    ratetype -= 1
                else:
                    ratetype = 1
                    break

def createFold():
    ids = readfile('ids.txt')
    for id in ids:
        os.mkdir("E:/program/Python/spam_detection/comments/comment&nid={}/".format(id[0]))

if __name__ == "__main__":
    action()
