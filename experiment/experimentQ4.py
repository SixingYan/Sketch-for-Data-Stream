# -*- coding: utf-8 -*-
"""
    Test Q4, the Eq( ) 
"""
#===================  Import ->
# system
import sys; sys.path.append("..")
import copy 
import numpy as np
import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment")
# DIY
import lib.diyTool as diyTool
#===================  <- Import

#===================  path area ->
homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/'# use '/' as ending

Q4result_Rad_Path = homePath + 'Q4_Rad'
Q4result_Top_Path = homePath + 'Q4_Top'
Q4evaluate_Rad_Path = homePath + 'Q4_Rad_evaluate'
Q4evaluate_Top_Path = homePath + 'Q4_Rad_evaluate'
#===================  <- path area

#================  parameter ->
wSet = [10,15]
hSet = [300,500,1000]
Epsilon = [i+1 for i in range(10)]
dataset = [ 
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp18.txt',338239,'comp18', 0.90],
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp16.txt',1391333,'comp16', 0.90],
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp14.txt',7904564,'comp14', 0.70],
    #['D:/google desk PC/ip_graph_refined',4213084,'ip', 0.90],
    #['C:/Users/alfonso.yan/Documents/tweet_stream_hashed_refined',17813281,'tweet', 0.60],
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp10.txt',1372146644,'comp1', 0.05]
]
percent = [0.01,0.03,0.05,0.1,0.2]
evaType = {'rad':['rad_mean','rad_medium','rad_max'],'top':['top_mean','top_medium','top_max']}
h = 300
w = 10
increase = 30
#================ <- parameter
def getRecord(w,h,dsName,ty,dataset):
    #
    for ky in dataset:
        if dataset[ky]['w']==w and dataset[ky]['h']==h and dataset[ky]['dsName']==dsName:
            recordList = [dataset[ky][way] for way in evaType[ty]]
            return recordList
    print('not exist')
    return None

def Coverage(expectRange, trueRange, OElist):
    #
    h1Range = [(OElist[i]+1)*increase for i in range(len(OElist))]
    low = expectRange[0]
    up = expectRange[1]
    low_true = trueRange[0]
    up_true = trueRange[1]

    upH1 = min([up,up_true])
    lowH1 = max([low,low_true])

    coverOE = [] 
    trueOE = []
    for i in range(len(OElist)):
        if h1Range[i] < upH1 and h1Range[i] > lowH1:
            coverOE.append(OElist[i])
        if h1Range[i] < up_true and h1Range[i] > low_true:
            trueOE.append(OElist[i]) 

    coverPrecent = abs(upH1-lowH1)/(up_true-low_true)
    coverageOE = sum(coverOE)/sum(trueOE)
    return coverPrecent, coverageOE

def RelativeBias(expectOpt, trueOpt, OElist):
    #
    h1Range = [(OElist[i]+1)*increase for i in range(len(OElist))]
    expectOE = 0
    trueOE = 0
    for i in range(len(OElist)):
        if h1Range[i] > expectOpt:
            expectOE = OElist[i]
            break
    for i in range(len(OElist)):
        if h1Range[i] > trueOpt:
            trueOE = OElist[i]
            break
    rbPrecent = abs(trueOpt-expectOpt)/trueOpt
    rbOE = abs(trueOE-expectOE)/trueOE
    return rbPrecent, rbOE
# get range of sqrt beta
def getH1Range(a):
    #
    point = 1/(2*a)
    ll = min([(a+1-abs(a-1))/(2*a),(a+1+abs(a-1))/(2*a)])
    uu = max([(1-abs(2*a-1))/(2*a),(1+abs(2*a-1))/(2*a)])
    optH1 = int(h * point) 
    rangeH1 = (int(h * ll),int(h * uu))
    return optH1, rangeH1

def measureH1Range(OElist):
    # got from OE list
    baseline = OElist[9]
    optIdx = -1
    minOE = -1
    idxList = []
    for i in range(len(OElist)):
        if OElist[i]<baseline:
            idxList.append(i)
        if not minOE == -1 and minOE > OElist[i]:
            minOE = OElist
            optIdx = i 
        else:
            minOE = OElist
            optIdx = i  
    
    ll = (min(idxList)+1) * increase
    uu = (max(idxList)+1) * increase
    opt = (optIdx+1) * increase
    return (int(ll), int(uu)), int(opt)

def getMedium(valueList):
    valueList.sort()
    return (valueList[int(len(valueList)/2)] + valueList[~int(len(valueList)/2)])/ 2

evaluateRad = []
evaluateTop = []

for ds in dataset:
    resultDict = {'w':w,'h':h,'ds':ds[2]}
    AlphaDict = []
    for i in range(len(percent)):
        meanList = []
        mediumList = []
        #for repeat in range(repeatNumber):
        dictKeyList = set([])
        nodeDict = {} #{}
        path = homePath+ds[2]+'_'+str(percent[i])+'.txt'
        with open(path,'r') as f:
            # out degree
            for line in f:
                line = line.strip()
            if not len(line) > 0:
                continue
            parts = line.split(' ')
            s = int(parts[0]);t = int(parts[1]);freq = float(parts[2])
            # out degree
            if s in dictKeyList:
                nodeDict[s][1] += freq
            else:
                nodeDict[s] = [0,0]
                nodeDict[s][1] += freq
                dictKeyList.add(s)
            # in degree
            if t in dictKeyList:
                nodeDict[t][0] += freq
            else:
                nodeDict[t] = [0,0]
                nodeDict[t][0] += freq
                dictKeyList.add(t)

        aList = []
        with open(ds[0],'r') as f:
            for line in f:
                line = line.strip()
                if not len(line) > 0:
                    continue
                s = int(parts[0]);t = int(parts[1]);freq = int(float(parts[2]))
                # alpha = (i,*)/(*,j)
                a = nodeDict[s][1]/nodeDict[t][0] # * freq
                aList.append(a)
        aList.sort()
        alphaMAX = max(aList)
        alphaMEAN = np.mean(aList)
        alphaMEDIUM = getMedium(aList)

        AlphaDict.append([alphaMEAN,alphaMEDIUM,alphaMAX])

    # check optimal range 
    datasetRad = diyTool.loadPickle(Q4result_Rad_Path)
    datasetTop = diyTool.loadPickle(Q4result_Top_Path)
    # check random 
    recordDict = getRecord(w,h,ds[2],'rad',datasetRad) #[3][100]
    evaluateCG =  [[[0 for _ in range(len(recordDict))] for _ in range(len(aList))] for _ in range(len(percent))]
    evaluateRB = copy.deepcopy(evaluateCG)
    for i in range(len(percent)): # 
        aList = AlphaDict[i]  #[3]
        for j in range(len(aList)): #  3 types of getting alpha mean/medium/max
            h1h2,opt = getH1Range(aList[j])
            for k in range(len(recordDict)): # 3 types of evaluating observed error
                h1h2Data,optData = measureH1Range(recordDict[k])
                cgV = Coverage(h1h2,h1h2Data,recordDict[k])
                evaluateCG[i][j][k] = cgV
                rbV = RelativeBias(opt,optData,recordDict[k])
                evaluateRB[i][j][k] = rbV

    tem = copy.deepcopy(resultDict)
    tem['Coverge'] = evaluateCG
    tem['RelativeBias'] = evaluateRB
    tem['type'] = 'rad'
    evaluateRad.append(tem)

    recordDict = getRecord(w,h,ds[2],'top',datasetTop) #[3][100]
    evaluateCG =  [[[0 for _ in range(len(recordDict))] for _ in range(len(aList))] for _ in range(len(percent))]
    evaluateRB = copy.deepcopy(evaluateCG)
    for i in range(len(percent)): # 
        aList = AlphaDict[i]  #[3]
        for j in range(len(aList)): #  3 types of getting alpha mean/medium/max
            h1h2,opt = getH1Range(aList[j])
            for k in range(len(recordDict)): # 3 types of evaluating observed error
                h1h2Data,optData = measureH1Range(recordDict[k])
                cgV = Coverage(h1h2,h1h2Data,recordDict[k])
                evaluateCG[i][j][k] = cgV
                rbV = RelativeBias(opt,optData,recordDict[k])
                evaluateRB[i][j][k] = rbV

    tem = copy.deepcopy(resultDict)
    tem['Coverge'] = evaluateCG
    tem['RelativeBias'] = evaluateRB
    tem['type'] = 'top'
    evaluateTop.append(tem)
    
    diyTool.savePickle(Q4evaluate_Rad_Path,evaluateRad)
    diyTool.savePickle(Q4evaluate_Top_Path,evaluateTop)

