# -*- coding: utf-8 -*-
"""
    Test Q4, the Eq( ) 
"""
"""


1. bias of best h1
2. coverage of h1 range of value





"""
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

Q0result_Sketch_CS_Path = homePath+'experiment/result/Q0_sketchResultData1'
Q0result_Dataset_CS_Path = homePath+'experiment/result/Q0_datasetResultData1'
Q0result_Sketch_GM_Path = homePath+'experiment/result/Q0_sketchResultData2'
Q0result_Dataset_GM_Path = homePath+'experiment/result/Q0_datasetResultData2'
#===================  <- path area

#================  parameter ->
wSet = [10,15]
hSet = [300,500,1000]
Epsilon = [i+1 for i in range(10)]
dataset = [ 
    #['D:/google desk PC/ip_graph_refined',4213084,2,'ip', 80],
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp18.txt',338239,2,'comp18', 0.90],
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp16.txt',1391333,2,'comp16', 0.90],
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp14.txt',7904564,2,'comp14', 0.70],
    ['D:/google desk PC/ip_graph_refined',4213084,2,'ip', 0.90],
    ['C:/Users/alfonso.yan/Documents/tweet_stream_hashed_refined',17813281,2,'tweet', 0.60],
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp12.txt',338239,2,'comp18', 90],
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp10.txt',1372146644,2,'comp1', 0.05]
]

repeatNumber = 10 # repeat times
alphaType = ['Mean','Medium','Max']
evaluateType = [['meanEval','meanEvalBest'],['mediumEval','mediumEvalBest'],['sumEval','sumEvalBest']]
h = 300
oeIdx = {'Rad':['oeRad100','oeRad500','oeRad1000'],'Top':['oeTop100','oeTop500','oeTop1000']}
#================ <- parameter

def getH1Range(alpha):
    # get range basing on sqrt beta
    h1Predict = [] # point, uu, ll
    point = 1/(2*alpha)
    ll = max([0,min([(1-abs(2*alpha-1))/(2*alpha),(1+abs(2*alpha-1))/(2*alpha)])])
    uu = max([(1-abs(2*alpha-1))/(2*alpha),(1+abs(2*alpha-1))/(2*alpha)])
    h1_point = int(h * point) 
    h1Predict.append(point)
    h1_ll = int(h * ll) 
    h1Predict.append((h1,h2))
    h1_ii = int(h * uu) 
    h1Predict.append((h1,h2))
    return h1Predict

def getMedium(valueList):
    return (valueList[int(len(valueList)/2)] + valueList[~int(len(valueList)/2)])/ 2

def getRecord(resultDict,h,w,ds,qType):
    # resultDict = {'w':w,'h':h,'dataset':ds[3],'type':'Rad','100':oeRad100,'500':oeRad500,'1000':oeRad1000}
    # return dict-type record
    returnD = None
    for ky in list(resultDict.keys()):
        if resultDict[ky]['h']==h and resultDict[ky]['w']==w and resultDict[ky]['dataset']==ds and resultDict[ky]['type']==qType:
            returnD = resultDict[ky]
            break
    return returnD

def getBaseLine(record, num):
    # num = '100'/500/1000  没写入这个
    # h1Range = [3][3][3]   100/500/1000  mean/medium/sum  point/ll/uu
    increace = int(record['h']/100)
    h1Range = []
    oeList = record[num] # oe100List = mean/medium/sum 100 sketch [3][100]
    # [9] is the place of h1=h2
    return_mms = []
    for k in range(3): #mean/medium/sum
        base = oeList[9]
        rangeIndex = []
        for j in range(oeList[k]): # 100 sketches
            if oeList[j] < base:
                rangeIndex.append(j)
        h1_uu = (max(rangeIndex)+1) * increace 
        h1_ll = (min(rangeIndex)+1) * increace
        h1_point = (index(min(oeList))+1) * increace
        return_mms.append([h1_ll,h1_uu,h1_point])
    h1Range.append(return_mms)
    return h1Range 

AlphaList = []
for ds in dataset:
    meanList = []
    mediumList = []

    for repeat in range(repeatNumber):
        dictKeyList = set([])
        nodeDict = {} #{}
        # first stream for degree
        with open(ds[0],'r') as f:
            # out degree
            for line in f:
                line = line.strip()
                if not len(line) > 0:
                    continue
                s = int(parts[0]);t = int(parts[1]);freq = int(float(parts[2]))
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
        # second stream for alpha
        aList = []
        with open(ds[0],'r') as f:
            
            for line in f:
                line = line.strip()
                if not len(line) > 0:
                    continue
                s = int(parts[0]);t = int(parts[1]);freq = int(float(parts[2]))
                # alpha = (i,*)/(*,j)
                a = nodeDict[s][1]/nodeDict[t][0] * freq
                aList.append(a)
        aList.sort()
        alphaMAX = max(aList)
        alphaMEAN = np.mean(aList)
        alphaMEDIUM = getMedium(aList)

        meanList.append(alphaMEAN)
        mediumList.append(alphaMEDIUM)
        maxList.append(alphaMAX)
    # <- repeat end

    # evaluating rad   given h, w, ds, type
    record = getRecord(resultDict,h,w,ds,'Rad')
    # one type per time 
    for num in ['100','500','1000']:
        h1Range = getBaseLine(record,'100') # [[[point, ll, uu],[],...],[[]....]....] mean/medium/sum point/uu/ll h1Range = [3][3][3]

        evaluateResult = [[] for _ in range(3)] # mean/medium/max repeat10 alpha3 metric2 [3][10][3][2] 
        for repeat in range(repeatNumber): # repeat 10
            a = meanList[repeat]; valueRange = getH1Range(a,h); 
            result = evaluate(valueRange,h1Range) # result = [3][2]
            evaluateResult[0].append(result)

            a = mediumList[repeat]; valueRange = getH1Range(a,h); result = evaluate(valueRange,h1Range)
            evaluateResult[1].append(result)

            a = maxList[repeat]; valueRange = getH1Range(a,h); result = evaluate(valueRange,h1Range)
            evaluateResult[2].append(result)

    # evaluateResult = [3][10][3][2] # 3 evaluating way 10 repeat time 3 alpha 2 metric
    # keep 10 results, find the best as return [3][3]
        result_bias = [] # [3][3] 3evaluate 3 alpha
        result_cover = []
        for i in range(3):# 3 evaluating way
            resultList_bias = [0,0,0] # the smaller the better min
            resultList_cover = [0,0,0] # the bigger the better max
            for j in range(3): # 3 alpha
                totalResult_b = []
                totalResult_c = []
                for repeat in range(repeatNumber): # 10 repeat find best as the final
                    totalResult_b.append(evaluateResult[i][repeat][j][0])
                    totalResult_c.append(evaluateResult[i][repeat][j][1])
                bestValue = min(totalResult_b);resultList_bias[j] = bestValue
                bestValue = min(totalResult_c);resultList_cover[j] = bestValue

            result_bias.append(resultList_bias)
            result_cover.append(resultList_cover)
        #{'w':0,'h':h,'meanEval':[0,0,0],}
        #evaluteDict = {'w':0,'h':h,'ds':[],'metrix':'','evaluate':'oeRad100','meanEval':[3],'meanEvalBest':'','mediumEval':[],'mediumEvalBest':'','sumEval':[],'sumEvalBest':''}
        evaluteDict = {'w':w,'h':h,'ds':[],'metrix':'','evaluate':'','meanEval':[],'meanEvalBest':'','mediumEval':[],'mediumEvalBest':'','sumEval':[],'sumEvalBest':''}
        temDict = copy.deepcopy(evaluteDict)
        temDict['metrix'] = 'bias'
        temDict['evaluate'] = 'oeRad100'
        for i in range(3):
            temDict[evaluateType[i][0]] = result_bias[i]
            idx = result_bias[i].index(min(result_bias[i])) # return 0,1,2 -> mean/medium/max
            temDict[evaluateType[i][1]] = alphaType[idx]
        Q42_datasetRad.append(temDict)

        temDict = copy.deepcopy(evaluteDict)
        temDict['metrix'] = 'cover'
        temDict['evaluate'] = 'oeRad100'
        for i in range(3):
            temDict[evaluateType[i][0]] = result_cover[i]
            idx = result_cover[i].index(min(result_cover[i])) # return 0,1,2 -> mean/medium/max
            temDict[evaluateType[i][1]] = alphaType[idx]
        Q42_datasetRad.append(temDict)
        
    # evaluating rad












