# -*- coding: utf-8 -*-
"""
greedyTree

"""
#import os;os.chdir('D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment');import experimentQ4_1
#===================  Import ->
# system
import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/src")
import sys; sys.path.append("..")
import random
import copy
import numpy as np
# DIY
#from diyTool import getSTD2
import lib
from lib.diyTool import treenode
import lib.mSketch2D as mSketch2D
#import lib.diyTool as diyTool
from lib.diyTool import getRatio
dataPath = 'D:/google desk PC/sample/tr_fre_2_0.001.txt'
samplePath = 'D:/google desk PC/sample/' 
dataName = 'tr_fre_2'
percent = '0.001'
w = 10
h = 20
N = 4
globalNodeID = 0
maxList = [255 for i in range(N)]
hList = [h for i in range(N)]
globalNodeID = 0
partList = [i for i in range(N)]
nodeDict = {}
leafDict = {}

def getSTD(sketch):
    return np.mean([np.std(wd) for wd in sketch.mSketch2D])

def getCandidate(node,partList):
    pathStr = getPath(node)
    #print('obtaining path '+pathStr)
    pd = getPathDict(pathStr)
    return list(set(partList) - set(pd['partID']))

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

def getPath(node):
    # return path = {'partID':[0,3,5,7],'edge':[S,C,S,...]}
    if node.priorID == -1:
        return str(node.partID)
    else:
        priorNode = nodeDict[node.priorID]
        edgeType = priorNode.nextNodes[node.nodeID]
        return getPath(priorNode) + edgeType + str(node.partID) 

def getStream(sketch,partList):
    # input structure of sketch 
    # open a sample of stream partList, e.g., 5,6,7
    pool = []
    print('getting stream ==========> ')
    with open(dataPath,'r') as f:
        for line in f:
            line = line.strip()
            if not len(line) > 0:
                continue
            parts = line.split(' ')
            #print('line '+line)
            # should be multi-part
            if len(parts) > 5: # for 8 parts
                sNode = [int(i) for i in parts[0].split('.')];
                tNode = [int(i) for i in parts[1].split('.')];
                fre = float(parts[2])
                nodeList = sNode + tNode
                #print('8 parts')
            else:# for 4 parts
                nodeList = [int(i) for i in parts[:4]]
                #print('4 parts')
            fre = float(parts[-1])
            edge = []
            #print('nodeList '+str(nodeList))
            for pID in partList:
                edge.append(nodeList[pID])
            if random.random() > 0.5:
                pool.append([edge,fre]) 
            #print(type(edge[0]))
            #print(fre)
            sketch.update(edge,fre)
    print('getting std')
    std = getSTD(sketch)
    #std = getSTD2(sketch,pool)
    del pool
    return std
 
def changeDict(d):
    # 0,6,4,3 -> 0,3,2,1
    partList = d['partID']
    partList.sort(reverse = False)
    #num = len(partList)
    newPartList = []
    for p in d['partID']:
        idx = partList.index(p)
        newPartList.append(idx)
    d['partID'] = newPartList
    return d    

def getRatioDist(stra):
    # input ((1,2),(3,4),(5))
    stra.reverse() # ((5),(3,4),(1,2))
    h1 = [0 for _ in range(len(stra))]
    for i in range(len(stra)):
        sList = stra[i]
        tList = []
        for j in range(i+1,len(stra)):
            for p in stra[j]:
                tList.append(p)
        sqrtBeta = getRatio(dataName,percent,sList,tList,samplePath)
        h1[i] = int(np.sqrt(h**(len(sList)+len(tList))) * sqrtBeta)
        if i == len(stra) -2:
            # next is the last one
            h1[i+1] = int(np.sqrt(h**(len(sList)+len(tList))) / sqrtBeta)
            break
    h1.reverse()
    return h1

def getMaxList(stra,maxList):
    maxIDList = []
    for i in range(len(stra)):
        if len(stra[i]) > 1:
            total = ''
            for idx in stra[i]:
                m = maxList[idx]
                total += str(m)
            mVal = int(total)
        else:
            idx = stra[i][0]
            mVal = maxList[idx]
        maxIDList.append(mVal)
    return maxIDList

def getProfit(partID, currentPath, edgeType):
    #
    newPath = str(partID)+edgeType+currentPath 
    d = getPathDict(newPath)
    straOrig = getStrategy(d)
    partList = d['partID']
    print('partList'+str(partList))
    print('straOrig'+str(straOrig))
    d = changeDict(d) # part ID is lower!
    stra = getStrategy(d) #if the only one is combination
    print('stra: '+str(stra))
    if len(stra) == 1:
        hList = [h**(len(stra[0]))] # only one length
    else:
        hList = getRatioDist(straOrig)
    print('hList: '+str(hList))
    
    maxIDList = getMaxList(straOrig,maxList)
    print('maxIDList: '+str(maxIDList))
    #std = 0
    sketch = copy.deepcopy(mSketch2D.mSketch2D(maxIDList,hList,w,h,stra, len(partList)))
    sketch.buildSketch()
    std = getStream(sketch,partList)
    return 1/std

def buildTree(node):
    global globalNodeID
    print('YYYYYYYYYYYYYYYY now try '+str(node.partID))
    currentPath = getPath(node); #print(currentPath) # list-type
    candidate = getCandidate(node,partList); #print(candidate) #
    optEdge = ''
    optPart = 0
    optProf = 0
    for partID in candidate:
        #if partID < node.partID: #
        print('\n ^^^^^^^^^^^^^partID '+str(partID))
        profit = getProfit(partID, currentPath, 'C')
        print('C profit ' + str(profit))
        #return 0 # end 
        if profit > optProf:
            optEdge = 'C'
            optPart = partID
            optProf = profit
        profit = getProfit(partID, currentPath, 'S')
        print('S profit ' + str(profit))
        if profit > optProf:
            optEdge = 'S'
            optPart = partID
            optProf = profit
        #return 0 # end
    subnode = treenode(optPart, globalNodeID, node.nodeID, node.order+1)
    globalNodeID += 1
    nodeDict[subnode.nodeID] = subnode # store this node
    node.nextNodes[subnode.nodeID] = optEdge
    print('opt edge is '+optEdge)
    print('next opt node is '+str(subnode.partID))
    print()
    #return 0;
    if subnode.order < N:# not leaf 
        buildTree(subnode)
    else:
        subnode.leaf  = True #
        currentPath = getPath(subnode) # str-type
        leafDict[subnode.nodeID] = [optProf, currentPath]

def main():
    global globalNodeID
    rootID = max(partList) #diyTool.getRoot()
    root = treenode(rootID, globalNodeID, -1, 1)
    nodeDict[globalNodeID] = root # store this node
    globalNodeID += 1
    buildTree(root)

if __name__ == '__main__':
    main()
