# -*- coding: utf-8 -*-
from random import randint
import random
import pickle
from math import sqrt
import time

def get_Prime(N):
    # larger than N, the number index of nodes; Ensure N > 2 and N is an integer
    prime = N
    if prime % 2 == 0:
        prime += 1
    while True:
        flag = True
        for num in range(3,int(sqrt(prime))+1):
            if prime%num == 0:
                flag = False
                break
        if flag == False:
            prime += 2
        else:
            break
    return prime

def getTwoRandomNum(P):
    # return tuple (a,b)
    a = randint(1,P-1)
    while True:
        b = randint(1,P-1)
        if not b == a:
            break
    return (a, b)

def savePickle(varName, var):
    varName += '.pickle'
    with open(varName, 'wb') as f:
        pickle.dump(var,f)

def loadPickle(varName):
    with open(varName, 'rb') as f:
        var = pickle.load(f)
    return var

def getMedium(valueList):
    valueList.sort()
    return (valueList[int(len(valueList)/2)] + valueList[~int(len(valueList)/2)])/ 2

def getRatio(dataName,perc,sList,tList,samplePath,N):
    print('now get ratio:' + str([dataName,perc,sList,tList,samplePath]))
    #perc(ent) float value
    percent = [perc]
    for i in range(len(percent)):
        print('=========now is precent '+str(percent[i]))
        t1 = time.time()
        dictKeyList = set([])
        nodeDict = {}
        path = samplePath+dataName+'_'+str(percent[i])+'.txt'
        print('get sample ==== '+path)
        #countNum = 0
        with open(path,'r') as f:
            for line in f:
                line = line.strip()
                if not len(line) > 0:
                    continue
                #countNum += 1
                parts = line.split(' ')
                # should be multi-part ===== >
                if N > 5: # for 8 parts
                    try:
                        sNode = [int(i) for i in parts[0].split('.')];
                        tNode = [int(i) for i in parts[1].split('.')];
                    except:
                        continue
                    freq = float(parts[2])
                    nodeList = sNode + tNode
                else:# for 4 parts
                    nodeList = [int(i) for i in parts[:4]]
                    freq = float(parts[4])
                s = [];t = []
                for idx in sList:
                    s.append(nodeList[idx])
                s = tuple(s)
                for idx in tList:
                    t.append(nodeList[idx])
                t = tuple(t)
                # <===== should be multi-part
                # out degree
                if s in dictKeyList:
                    nodeDict[s][1] += freq
                else:
                    nodeDict[s] = [0,0];nodeDict[s][1] += freq
                    dictKeyList.add(s)
                # in degree
                if t in dictKeyList:
                    nodeDict[t][0] += freq
                else:
                    nodeDict[t] = [0,0];nodeDict[t][0] += freq
                    dictKeyList.add(t)
        print('predicting alpha')
        aList = []
        with open(path,'r') as f:
            for line in f:
                line = line.strip()
                if not len(line) > 0:
                    continue
                parts = line.split(' ')
                # should be multi-part ===== >
                if N > 5: # for 8 parts
                    try:
                        sNode = [int(i) for i in parts[0].split('.')];
                        tNode = [int(i) for i in parts[1].split('.')];
                    except:
                        continue
                    #freq = float(parts[2])
                    nodeList = sNode + tNode
                else:# for 4 parts
                    nodeList = [int(i) for i in parts[:4]]
                    freq = float(parts[4])
                s = [];t = []
                for idx in sList:
                    s.append(nodeList[idx])
                s = tuple(s)
                for idx in tList:
                    t.append(nodeList[idx])
                t = tuple(t)
                # <===== should be multi-part
                
                a = nodeDict[s][1]/nodeDict[t][0] # alpha = (i,*)/(*,j)
                aList.append(a)
        aList.sort();aList = list(set(aList))
        alphaMEDIUM = getMedium(aList)

    sqrtBeta = 1+alphaMEDIUM/(2 * alphaMEDIUM)
    print('completed!\n')
    return sqrtBeta

class treenode(object):
    def __init__(self, partID, nodeID, priorID, order):
        self.isLeaf = False # true/false
        self.partID = partID
        self.nodeID = nodeID
        self.priorID = priorID
        self.order = order 
        self.nextNodes = {} # key is node ID

def getSTD2(sketch,pool):
    #
    ObservedError = 0
    #for i in range(len(pool)):
    totalLoss1 = 0;totalFreq1 = 0
    for parts in pool:
        edge = parts[0]; freq = parts[1]
        estiValue = sketch.query(edge)
        totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
    ObservedError = totalLoss1/totalFreq1
    #print('ObservedError is '+str(ObservedError/len(radList)))
    return ObservedError/len(pool)

def getPathDict(pathStr):
    # input a string 
    pathDict = {}
    pathDict['partID'] = []
    pathDict['edgeType'] = []
    preIndex = 0
    for i in range(len(pathStr)):
        if pathStr[i] == 'S' or pathStr[i] == 'C':
            pathDict['partID'].append(int(pathStr[preIndex:i]))
            if pathStr[i] == 'S':
                pathDict['edgeType'].append(0)
            else:
                pathDict['edgeType'].append(1)
            preIndex = i + 1
    pathTem = pathStr[::-1]# reverse string
    idx = 0
    #print(pathTem)
    for i in range(len(pathTem)):
        if pathTem[i] == 'S' or pathTem[i] == 'C':
            idx = i
            break
    pathDict['partID'].append(int(pathStr[-idx:]))
    return pathDict

def getStrategy(pathDict):
    # edge=0 seperate  edge=1 combine 
    j = 0
    strategy = []#[[],...[]]
    for i in range(len(pathDict['partID'])):
        if i == len(pathDict['partID'])-1:
            continue
        if i == 0:
            strategy.append([])
            strategy[j].append(pathDict['partID'][i])
        edge = pathDict['edgeType'][i]
        if edge == 1:
            strategy[j].append(pathDict['partID'][i+1])
        else:
            strategy.append([])
            j += 1
            strategy[j].append(pathDict['partID'][i+1])
    return strategy

def evaluate_rad_sum_counter(sketch,radList,mgCounter):
    #
    ObservedError = 0
    for i in range(len(radList)):
        totalLoss1 = 0;totalFreq1 = 0
        for parts in radList[i]:
            edge=parts[0];freq = parts[1]
            if mgCounter.query(edge):
                flag = 1
            else:
                flag = 0
            estiValue = sketch.query(flag,edge)
            totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
        ObservedError += totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError/len(radList)))
    return ObservedError/len(radList)

def evaluate_top_sum_counter(sketch,topList,mgCounter):
    totalLoss1 = 0;totalFreq1 = 0
    for parts in topList:
        edge=parts[0];freq = parts[1]
        if mgCounter.query(edge):
            flag = 1
        else:
            flag = 0
        estiValue = sketch.query(flag,edge)
        totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
    ObservedError = totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError))
    return ObservedError

def evaluate_rad_sum(sketch,radList):
    #
    ObservedError = 0
    for i in range(len(radList)):
        totalLoss1 = 0;totalFreq1 = 0
        for parts in radList[i]:
            edge=parts[0]; freq = parts[1]
            estiValue = sketch.query(edge)
            totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
        ObservedError += totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError/len(radList)))
    return ObservedError/len(radList)
#---------------
def evaluate_top_sum(sketch,topList):
    totalLoss1 = 0;totalFreq1 = 0
    for parts in topList:
        edge=parts[0]; freq = parts[1]
        estiValue = sketch.query(edge)
        totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
    ObservedError = totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError))
    return ObservedError

def getRadList(num,radPool):
    radList = [[] for i in range(5)]
    for i in range(len(radList)):
        while len(radList[i]) < num:
            tem = random.choice(radPool)
            if tem not in radList[i]:
                radList[i].append(tem)
    return radList