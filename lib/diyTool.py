# -*- coding: utf-8 -*-
from random import randint
import pickle
from math import sqrt

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

def getRatio(dataName,perc,sList,tList,samplePath):
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
                # should be multi-part
                if len(parts) > 3: # for 8 parts
                    sNode = [int(i) for i in parts[0].split('.')];
                    tNode = [int(i) for i in parts[1].split('.')];
                    freq = float(parts[2])
                    nodeList = sNode + tNode
                else:# for 4 parts
                    nodeList = [int(i) for i in parts[:4]]

                s = [];t = []
                for idx in sList:
                    s.append(nodeList[idx])
                s = tuple(s)
                for idx in tList:
                    t.append(nodeList[idx])
                t = tuple(t)
                #s = int(parts[0]);t = int(parts[1]);freq = float(parts[2])

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
        aList = []
        with open(path,'r') as f:
            for line in f:
                line = line.strip()
                if not len(line) > 0:
                    continue
                parts = line.split(' ')
                s = int(parts[0]);t = int(parts[1]);#freq = int(float(parts[2]))
                # alpha = (i,*)/(*,j)
                a = nodeDict[s][1]/nodeDict[t][0] # * freq
                aList.append(a)
        aList.sort();aList = list(set(aList))
        alphaMEDIUM = getMedium(aList)

    sqrtBeta = 1+alphaMEDIUM/(2 * alphaMEDIUM)
    return sqrtBeta


class treenode(object):
    def __init__(self, partID, nodeID, priorID, order):
        self.isLeaf = False # true/false
        self.partID = partID
        self.nodeID = nodeID
        self.priorID = priorID
        self.order = order 
        self.nextNodes = {} # key is node ID

def getSTD2(sketch, pool):
    pass