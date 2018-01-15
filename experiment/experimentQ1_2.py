# -*- coding: utf-8 -*-
#import os;os.chdir('D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment');import experimentQ1_2
#===================  Import ->
# system
import sys; sys.path.append("..")
from copy import deepcopy
import numpy as np
import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment")
# DIY
import lib
import lib.diyTool as diyTool
#===================  <- Import

#===================  path area ->
homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment/result/'# use '/' as ending
samplePath = 'D:/google desk PC/sample/'
Q1result_Sketch_set_Path = homePath+'Q1_percentSketch_set_'
#===================  <- path area

#================  parameter ->
wSet = [10,15]
hSet = [300,500,1000,2000]
Epsilon = [i+2 for i in range(9)]
dataset = [ 
    ['D:/google desk PC/graph_freq_comp18.txt',338239,'comp18', 1],
    ['D:/google desk PC/graph_freq_comp16.txt',1391333,'comp16', 1],
    ['D:/google desk PC/graph_freq_comp14.txt',7904564,'comp14', 1]
    #['C:/Users/alfonso.yan/Documents/ip_graph_refined',4213084,'ip', 1],
    #['C:/Users/alfonso.yan/Documents/tweet_stream_hashed_refined',17813281,'tweet', 1]
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp12.txt',31160379,'comp12', 0.8],
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp10.txt',56175513,'comp1', 0.1]
]
percent = [0.001, 0.003, 0.005, 0.01, 0.03, 0.05, 0.1, 0.2]
#================ <- parameter

def getMedium(valueList):
    valueList.sort()
    return (valueList[int(len(valueList)/2)] + valueList[~int(len(valueList)/2)])/ 2

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

def getSTD(sketch):
    #
    w = len(sketch)
    stdList = []
    for k in range(w):
        stdList.append(np.std(sketch[k])) 
    meanSTD = np.mean(stdList) 
    #mediumSTD = getMedium(stdList)
    return meanSTD #, mediumSTD

def getRatio(sketch,baselineSTD):
    w = len(sketch)
    meanSketch = np.mean(sketch[0])
    mean_ratio = [] #[9]
    medium_ratio = []
    for e in Epsilon:
        mean_ratioList = []
        medium_ratioList = []
        ratio = 0
        for k in range(w):
            totalNum = 0
            for j in range(len(sketch[k])):
                if (sketch[k][j]-meanSketch) < (baselineSTD * e):
                    totalNum += 1
            ratio += totalNum/len(sketch[k])
            
        ratio /= w
        mean_ratioList.append(ratio)
        medium_ratioList.append(ratio)
        mean_ratio.append(np.mean(mean_ratioList))
        medium_ratio.append(getMedium(medium_ratioList))
    return mean_ratio, medium_ratio
#
sketchResultData_set = [] # [{},{},{},...]

for w in wSet:
    print('==now w is: '+str(w))
    print()
    for h in hSet:
        print('====now h is: '+str(h))
        print()
        for ds in dataset: # 'ds' is the list [file name, N, itemNum, datasetName] of one data set
            sketchDict = {'w':w,'h':h,'dataset':ds[2]}
            print('========now ds is: '+ds[2]) # 
            # for original data
            sketch = [[0 for _ in range(h**2)] for _ in range(w)]
            cSketch = deepcopy(sketch)
            gMatrix = deepcopy(sketch)
            cN = int(str(ds[1]) * 2)
            gN = ds[1]
            mask_c = [diyTool.getTwoRandomNum(cN) for _ in range(w)]
            mask_g = [diyTool.getTwoRandomNum(gN) for _ in range(w)]
            print('start streaming')
            with open(ds[0], 'r') as f:
                for line in f:
                    if not len(line.strip()) > 0:
                        continue
                    # prepare edge
                    parts = line.strip().split(' ')
                    edge = parts[:len(parts)-1]
                    for num in range(len(edge)):
                        edge[num] = int(edge[num])
                    freq = float(parts[len(parts)-1])
                    updateSketch(cSketch,csHash,edge,cN,freq,w,mask_c)
                    updateSketch(gMatrix,gmHash,edge,gN,freq,w,mask_g)
            # given a stream
            cSketchSTD = getSTD(cSketch)
            gMatrixSTD = getSTD(gMatrix)
            del cSketch; del gMatrix
            # for sample data
            for i in range(len(percent)):
                print('start sample with '+str(percent[i]))
                sampleP = samplePath+ds[2]+'_'+str(percent[i])+'.txt'
                cSketch_percent = deepcopy(sketch)
                gMatrix_percent = deepcopy(sketch)
                # given a stream
                with open(sampleP, 'r') as f:
                    for line in f:
                        if not len(line.strip()) > 0:
                            continue
                        # prepare edge
                        parts = line.strip().split(' ')
                        edge = parts[:len(parts)-1]
                        for num in range(len(edge)):
                            edge[num] = int(edge[num])
                        freq = float(parts[len(parts)-1])
                        updateSketch(cSketch_percent,csHash,edge,cN,freq,w,mask_c)
                        updateSketch(gMatrix_percent,gmHash,edge,gN,freq,w,mask_g)

                mean_ratio, medium_ratio = getRatio(cSketch_percent, cSketchSTD)
                temDict = deepcopy(sketchDict)
                temDict['sketch'] = 'cs'
                temDict['mean_ratio'] = mean_ratio
                temDict['medium_ratio'] = medium_ratio
                temDict['percent'] = percent[i]
                sketchResultData_set.append(temDict) # put in

                mean_ratio, medium_ratio = getRatio(gMatrix_percent, gMatrixSTD)
                temDict = deepcopy(sketchDict)
                temDict['sketch'] = 'gm'
                temDict['mean_ratio'] = mean_ratio
                temDict['medium_ratio'] = medium_ratio
                temDict['percent'] = percent[i]
                sketchResultData_set.append(temDict) # put in

                print('========saving') # saving .......
                diyTool.savePickle(Q1result_Sketch_set_Path+ds[2],sketchResultData_set)

                del cSketch_percent; del gMatrix_percent