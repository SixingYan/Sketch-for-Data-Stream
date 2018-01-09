# -*- coding: utf-8 -*-
'''
""" 
- GOAL
#get stream| std, mean
#get sample stream| std, mean
get sketch| std, mean
get sample sketch| std, mean
get ratio| std, mean
get sample ratio| std, mean
"""
#===================  Import ->
# system
import sys; sys.path.append("..")
from copy import deepcopy
import random
import numpy as np
import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment")
# DIY
import diyTool
#===================  <- Import

#===================  path area ->
homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/'# use '/' as ending

Q1result_Stream_Path = homePath+'experiment/result/Q1_streamResultData'
Q1result_Dataset_Path = homePath+'experiment/result/Q1_datasetResultData'
Q1result_Dataset_set_Path = homePath+'experiment/result/Q1_datasetResultData_set'
Q1result_Sketch_Path = homePath+'experiment/result/Q1_sketchResultData'
Q1result_Sketch_set_Path = homePath+'experiment/result/Q1_sketchResultData_set'
#===================  <- path area

#多少 percent 正确率还能保障
'''

#===================  Import ->
# system
#import sys; sys.path.append("..")
from copy import deepcopy
import random
import numpy as np
#import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment")
# DIY
import lib.diyTool
#===================  <- Import

#===================  path area ->
homePath = 'C:/Users/alfonso.yan/Downloads/'# use '/' as ending

Q1result_Stream_Path = homePath+'Q1_streamResultData'
Q1result_Dataset_Path = homePath+'Q1_datasetResultData'
Q1result_Dataset_set_Path = homePath+'Q1_datasetResultData_set'
Q1result_Sketch_Path = homePath+'Q1_sketchResultData'
Q1result_Sketch_set_Path = homePath+'Q1_sketchResultData_set'
#===================  <- path area

#================  parameter ->
basicPercent = 0.7
wSet = [10,15]
hSet = [300,500,1000]
Epsilon = [1, 3, 5, 10]
dataset = [ 
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp18.txt',338239,2,'comp18', 0.90],
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp16.txt',1391333,2,'comp16', 0.90],
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp14.txt',7904564,2,'comp14', 0.70],
    ['C:/Users/alfonso.yan/Documents/ip_graph_refined',4213084,2,'ip', 0.90],
    ['C:/Users/alfonso.yan/Documents/tweet_stream_hashed_refined',17813281,2,'tweet', 0.60],
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp12.txt',338239,2,'comp18', 90],
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp10.txt',1372146644,2,'comp1', 0.05]
]
percent = [0.001, 0.003, 0.005, 0.01, 0.03, 0.05, 0.1, 0.2]
n=[int(1/i) for i in percent]
percentNum = len(percent)
repeatNumber = 1 # repeat times
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

def getSTD(sketch,edgeNum):
    #
    w = len(sketch)
    stdList = []
    for k in range(w):
        stdList.append(np.std(sketch[k])) 
    meanSTD = np.mean(stdList) 
    mediumSTD = getMedium(stdList)
    return meanSTD, mediumSTD

def checkSketchRatio(sketch,baselineSTD):
    w = len(sketch)
    meanSketch = np.mean(sketch[0])
    mean_ratio = []
    medium_ratio = []
    for e in Epsilon:
        for k in range(w):
            totalNum = 0
            for j in range(len(sketch[k])):
                if (sketch[k][j]-meanSketch) < (baselineSTD * e):
                    totalNum += 1
            mean_ratioList.append(totalNum)
            medium_ratioList.append(totalNum)
        mean_ratio.append(np.mean(mean_ratioList))
        medium_ratio.append(getSTD(medium_ratioList))
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
            print('========now ds is: '+ds[3])
            print()
            if True: # just incident error
                # n*2 sketches
                sketchDict = {'w':w,'h':h,'dataset':ds[3]}
                mediumSTD_CSketch = []
                meanSTD_CSketch = []
                mediumSTD_GMatrix = []
                meanSTD_GMatrix = []
                for repeat in range(repeatNumber):
                    print('============repeat: '+str(repeat))
                    sketch = [[0 for _ in range(h**ds[2])] for _ in range(w)]
                    cSketch = deepcopy(sketch)
                    gMatrix = deepcopy(sketch)
                    cSketchSet = [deepcopy(sketch) for _ in range(percentNum)]
                    gMatrixSet = [deepcopy(sketch) for _ in range(percentNum)]
                    cN = int(str(ds[1]) * ds[2])
                    gN = ds[1]
                    mask_c = [diyTool.getTwoRandomNum(cN) for _ in range(w)]
                    mask_g = [diyTool.getTwoRandomNum(gN) for _ in range(w)]
                    # start stream
                    print('============start stream')
                    with open(ds[0], 'r') as f:
                        for line in f:
                            if not len(line) > 0:
                                continue
                            # prepare edge
                            parts = line.strip().split(' ')
                            edge = parts[:len(parts)-1]
                            for num in range(len(edge)):
                                edge[num] = int(edge[num])
                            freq = int(float(parts[len(parts)-1]))

                            # select edge
                            randNum = random.randint(0,1000)
                            if randNum > 1000: #temp percent, used ds[4] to replace
                                continue

                            # sketch storing
                            updateSketch(cSketch,csHash,edge,cN,freq,w,mask_c)
                            updateSketch(gMatrix,gmHash,edge,gN,freq,w,mask_g)

                            for i in range(percentNum):
                                per = percent[i]
                                if randNum > 1000 * per:
                                    continue
                                # sketch storing
                                updateSketch(cSketchSet[i],csHash,edge,cN,freq,w,mask_c)
                                updateSketch(gMatrixSet[i],gmHash,edge,gN,freq,w,mask_g)

                    print('============start checking cSketch')
                    # baseline cSketch
                    meanSTD, mediumSTD = getSTD(cSketch,ds[2])
                    mediumSTD_CSketch.append(mediumSTD)
                    meanSTD_CSketch.append(meanSTD)
                    
                    print('============start checking gMatrix')
                    # baseline gMatrix
                    meanSTD, mediumSTD = getSTD(gMatrix,ds[2])
                    mediumSTD_GMatrix.append(mediumSTD)
                    meanSTD_GMatrix.append(meanSTD)
                    
                    # clear memory  
                    del sketch; del cSketch; del cSketchSet; del gMatrix; del gMatrixSet; del stream; del streamSample

                print('============get cSketch result')
                # sketch
                temDict = deepcopy(sketchDict)
                temDict['sketch'] = 'cs'
                baselineSTD = np.mean(meanSTD_CSketch)
                for i in range(percentNum):
                    mean_ratio, medium_ratio = checkSketchRatio(sketchDict_cSketchSet[i],baselineSTD)
                    temDict['meanSTD_mean'] = deepcopy(mean_ratio)
                    temDict['mediumSTD_mean'] = deepcopy(medium_ratio)
                baselineSTD = np.mean(mediumSTD_CSketch)
                for i in range(percentNum):
                    mean_ratio, medium_ratio = checkSketchRatio(sketchDict_cSketchSet[i],baselineSTD)
                    temDict['meanSTD_medium'] = deepcopy(mean_ratio)
                    temDict['mediumSTD_medium'] = deepcopy(medium_ratio)
                sketchResultData_set.append(temDict) # put in
                
                print('============get gMatrix result')
                # sketch
                temDict = deepcopy(sketchDict)
                temDict['sketch'] = 'gm'
                baselineSTD = np.mean(meanSTD_CSketch)
                for i in range(percentNum):
                    mean_ratio, medium_ratio = checkSketchRatio(sketchDict_gMatrixSet[i],baselineSTD)
                    temDict['meanSTD_mean'] = deepcopy(mean_ratio)
                    temDict['mediumSTD_mean'] = deepcopy(medium_ratio)
                baselineSTD = np.mean(mediumSTD_CSketch)
                for i in range(percentNum):
                    mean_ratio, medium_ratio = checkSketchRatio(sketchDict_gMatrixSet[i],baselineSTD)
                    temDict['meanSTD_medium'] = deepcopy(mean_ratio)
                    temDict['mediumSTD_medium'] = deepcopy(medium_ratio)
                sketchResultData_set.append(temDict) # put in
                
                print('========saving') # saving .......
                diyTool.savePickle(Q1result_Sketch_set_Path,sketchResultData_set)
                
                print('^^^^^^^^^^^sketchResultData_set^^^^^^^^^^^')
                print(sketchResultData_set)
                print()
        flag = False