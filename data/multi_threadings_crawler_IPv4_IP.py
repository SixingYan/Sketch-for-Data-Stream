# -*- coding: utf-8 -*-
"""
@author: Alfonso Ngan
Multi-threading
"""
#from bs4 import BeautifulSoup
import requests
import time
import csv
from random import randint
from queue import Queue
from threading import Thread

from publicTool import loadPickle

commHeaders = {}
commHeaders['content-type']='application/json'
commHeaders['User-Agent']='Opera/9.25 (Windows NT 5.1; U; en)'
commHeaders['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
commHeaders['Accept-Language']='zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
commHeaders['Accept-Encoding']='gzip, deflate, br'
commHeaders['Referer']='https://dl.acm.org/results.cfm?query=big+data&Go.x=30&Go.y=11'

commHttpProxies = {'https':'182.253.121.137:8080'}


#===============================================
mainPath = 'D:/google desk PC/' #saving folder path
savePath = 'D:/点击这里/Nanyang/data/' #saving folder path
useragentPath = 'D:/点击这里/Code/Data/userAgent.csv' #self ua path
httpsPath = 'D:/点击这里/Code/Data/http.txt' #self http folder path

#===============================================

useragentList = []
httpsList = []

#===============================================
with open(useragentPath, 'r', newline='',encoding='utf-8') as f:
        reader = csv.reader(f)        
        for row in reader:
            useragentList.append(row[0])
with open(httpsPath,'r') as f:
    for line in f.readlines():
        httpsList.append(line)
#===============================================


def getFile(fileIP):
    try:
        rr  = requests.get(fileIP)
        fileName = fileIP[-35:]
        with open(savePath+fileName,'wb') as f:
            f.write(rr.content)
        return '1'
    except requests.RequestException as e:
        print(e)
        return '0'
    else:
        pass

fromIPQueue = Queue()   #欲访问的下载网址
uaQueue = Queue() #user agent 修饰
httpQueue = Queue() #本地ip 修饰

class downloadWorker(Thread):
    def __init__(self,fromIPQueue,uaQueue,httpQueue):
        Thread.__init__(self)
        self.fromIPQueue = fromIPQueue #
        self.uaQueue = uaQueue #
        self.httpQueue = httpQueue #
        
    def run(self):
        while True:         

            # edit local ip
            http  = self.httpQueue.get()
            commHttpProxies['https'] = http
            self.httpQueue.put(http)

            # edit user agent
            if randint(1,3) == 2:
                ua = self.uaQueue.get()
                commHeaders['User-Agent'] = ua
                self.uaQueue.put(ua)

            time.sleep(randint(1, 15))#随机休眠

            #download
            print('start:')
            ip = self.fromIPQueue.get()
            flag = getFile(ip)

            if flag == '0':#未获取成功，重新放入
                self.fromIPQueue.put(ip)
                print('put back'+str(ip))
            print('completed: '+str(ip))
            self.fromIPQueue.task_done()


def mainFunction():

    ipSet = loadPickle('D:/点击这里/Nanyang/dataIPv4/ipSet.pickle')
    i = 0
    for ip in ipSet:
        fromIPQueue.put(ip)
        if i==3:
            break
        i+=1
    print()
    for ip in httpsList:
        httpQueue.put(ip)
    for ua in useragentList:
        uaQueue.put(ua)

    for i in range(2):
        pWorker = downloadWorker(fromIPQueue,uaQueue,httpQueue)
        pWorker.daemon = True
        pWorker.start()

mainFunction()