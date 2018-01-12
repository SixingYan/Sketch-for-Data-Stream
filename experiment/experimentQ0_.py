# -*- coding: utf-8 -*-
#===================  Import ->
# system
import sys; sys.path.append("..")
from copy import deepcopy
import random
import numpy as np
import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment")
# DIY
import lib.diyTool
#===================  <- Import

#===================  path area ->
homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/'# use '/' as ending
Q0result_Sketch_Path = homePath+'experiment/result/Q0_sketch_result'
#===================  <- path area

#================  parameter ->
wSet = [10,15]
hSet = [300,500,1000]
Epsilon = [i+2 for i in range(10)]
dataset = [  #存文件名, 最大值, item数量, 数据集名称
    ['D:/google desk PC/tweet_stream_hashed_refined',17813281,'tweet']
    ['D:/google desk PC/ip_graph_refined',4213084,'ip'],
    ['D:/google desk PC/graph_freq_comp18.txt',338239,'comp18'],
    ['D:/google desk PC/graph_freq_comp14.txt',7904564,'comp14']
]
#================ <- parameter

def combine(edge, N):
    combinedValue = ''
    for item in edge:
        if len(str(item)) < len(str(N)):
            num = int(len(str(N))/2)-len(str(item))
            newItem = '0' * num + str(item)
            combinedValue += newItem
        else:
            combinedValue += str(item)
    return int(combinedValue)

def csHash(edge, P, h, w, mask):
    # combine
    # return hash value
    hashValue = combine(edge, P) # use P replace N
    H = h**len(edge)
    hvList = []
    for i in range(w):
        a, b = mask[i][0], mask[i][1]
        hvList.append((hashValue * a + b) % P % H)
    return hvList

def gmHash(edge, P, h, w, mask):
    hvList = []
    for k in range(w):
        a, b = mask[k][0], mask[k][1]
        totalI = 0
        for i in range(len(edge)):
            # if i=0, edge(t1,t2), then h**(2-1-0) = h
            totalI += ((a*edge[i]+b)%P%h)*(h**(len(edge)-1-i))
        hvList.append(totalI)
    return hvList

def updateSketch(sketch, hashF, edge, P, freq, w, mask):
    #
    hvList = hashF(edge, P, h, w, mask)
    for k in range(w):
        sketch[k][hvList[k]] += freq

sketchResultData = [] # [{},{},{},...]

# change sigma
for w in wSet:
    print('==now w is: '+str(w))
    print()
    for h in hSet:
        print('====now h is: '+str(h))
        print()
        for ds in dataset: # 'ds' is the list [file name, N, itemNum, datasetName] of one data set
            print('========now ds is: '+ds[2])
            ratioDict = {'w':w,'h':h,'ds':ds[2]}
            print()
            sketch = [[0 for _ in range(h**ds[2])] for _ in range(w)]
            cSketch = deepcopy(sketch)
            gMatrix = deepcopy(sketch)
            cN = int(str(ds[1]) * ds[2])
            gN = ds[1]
            mask_c = [diyTool.getTwoRandomNum(cN) for _ in range(w)]
            mask_g = [diyTool.getTwoRandomNum(gN) for _ in range(w)]
            print('============start stream')
            # make a stream
            countNum = 0
            with open(ds[0], 'r') as f:
                for line in f:
                    if not len(line) > 0:
                        continue
                    #if random.randint(0,100)>70: # random select
                    #    continue    
                    countNum += 1
                    if countNum % 1000000 == 0:
                        print('================now is '+str(countNum))
                    parts = line.strip().split(' ')
                    edge = parts[:len(parts)-1]
                    for num in range(len(edge)):
                        edge[num] = int(edge[num])
                    freq = float(parts[len(parts)-1])

                    # random select to put in
                    updateSketch(cSketch,csHash,edge,cN,freq,w,mask_c)
                    updateSketch(gMatrix,gmHash,edge,gN,freq,w,mask_g)

            print('============start checking cSketch')
            meanSketch = np.mean(cSketch[0])
            totalSTD = 0
            for k in range(w):
                totalSTD += np.std(cSketch[k])
            stdSketch = totalSTD/w 
            
            ratioList = []
            for e in Epsilon:
                tNum = 0
                for k in range(w):
                    totalNum = 0
                    for j in range(len(cSketch[k])):
                        if (cSketch[k][j]-meanSketch) < (stdSketch * e):
                            totalNum += 1
                    tNum += totalNum/len(cSketch[k])
                ratioList.append(tNum/w)
            
            tem = copy.deepcopy(ratioDict)
            tem['sketch'] = 'cs'
            tem['ratio'] = ratioList
            sketchResultData.append(tem)

            print('============start checking gMatrix')
            meanSketch = np.mean(gMatrix[0])
            totalSTD = 0
            for k in range(w):
                totalSTD += np.std(gMatrix[k])
            stdSketch = totalSTD/w 
            
            ratioList = []
            for e in Epsilon:
                tNum = 0
                for k in range(w):
                    totalNum = 0
                    for j in range(len(gMatrix[k])):
                        if (gMatrix[k][j]-meanSketch) < (stdSketch * e):
                            totalNum += 1
                    tNum += totalNum/len(gMatrix[k])
                ratioList.append(tNum/w)
            
            tem = copy.deepcopy(ratioDict)
            tem['sketch'] = 'gm'
            tem['ratio'] = ratioList
            sketchResultData.append(tem)

            print('========saving')
            diyTool.savePickle(Q0result_Sketch_Path,sketchResultData)