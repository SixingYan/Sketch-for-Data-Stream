we# -*- coding: utf-8 -*-
"""
单线程爬虫
"""
commHeaders = {}
commHeaders['content-type']='application/json'
commHeaders['User-Agent']='Opera/9.25 (Windows NT 5.1; U; en)'
commHeaders['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
commHeaders['Accept-Language']='zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
commHeaders['Accept-Encoding']='gzip, deflate, br'
commHeaders['Referer']='https://dl.acm.org/results.cfm?query=big+data&Go.x=30&Go.y=11'

commHttpProxies = {'https':'182.253.121.137:8080'}

from bs4 import BeautifulSoup
import requests
import time
import random
import csv
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


def getPage(url,httpProxies,headers,cookies):
    htmlText = ' '
    try:
        #requests.encoding = 'utf-8'
        if random.randint(0,1)==0:
            editInfo()
            r = requests.get(url.encode().decode('utf-8'), proxies=httpProxies, headers=headers, timeout=30)
        else:
            r = requests.get(url.encode().decode('utf-8'), proxies=httpProxies, headers=headers, timeout=30)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            htmlText = r.text
            return htmlText
        else:
            print('error: code = ' + str(r.status_code));print('error: url = '+ url)
            return ' '
    except requests.RequestException as e:
        print(e)
        return ' '
    else:
        pass
    
def editInfo():
    #change the parameters
    commHttpProxies['https'] = random.choice(httpsList)
    commHeaders['User-Agent'] = random.choice(useragentList)
    time.sleep(random.randint(5, 20))# wait a moment
    
def getIPlist(htmlText,folderIP):
    ipList = []
    soup = BeautifulSoup(''.join(htmlText),"lxml")
    try:
        if soup.findAll('a') != None:
            for a in soup.findAll('a'):
                href = a['href']
                ipList.append(folderIP+href)      
    except Exception:
        print('error:'+str(soup))
    return ipList

def getFile(fileIP):
    #rr  = requests.get('http://data.caida.org/datasets/topology/ark/ipv4/as-links/team-1/2007/cycle-aslinks.l7.t1.c000027.20070913.txt.gz')
    try:
        rr  = requests.get(fileIP)
        fileName = fileIP[-25:]
        with open(savePath+fileName,'wb') as f:
            f.write(rr.content)
    except requests.RequestException as e:
        print(e)

def getFolderIP():
    ipSet = []
    for i in range(3): # team 1 2 3
        for j in range(2008,2018): #2008 - 2017
            folderIP = 'http://data.caida.org/datasets/topology/ark/ipv4/as-links/team-'+str(i+1)+'/'+str(j)+'/'
            htmlText = getPage(folderIP)
            ipSet.extend(getIPlist(htmlText,folderIP))
    return ipSet

def mainFunction():
    ipSet = getFolderIP
    for fileIP in ipSet:
        getFile(fileIP)
        print('completed '+str())
