# -*- coding: utf-8 -*-
#===================  Import ->
# system
import sys; sys.path.append("..")
#import copy 
import numpy as np
import matplotlib.pyplot as plt
import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment")
# DIY
import lib
import lib.diyTool as diyTool
#===================  <- Import
#===================  path area ->
homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment/result/'# use '/' as ending
samplePath = 'D:/google desk PC/sample/'
Q4result_Rad_P = homePath + 'Q4_Rad_'
Q4result_Top_P = homePath + 'Q4_Top_'

#===================  <- path area
#================  parameter ->
percent = [0.05, 0.1, 0.2]#[0.01,0.03,0.05,0.1,0.2]
evaType = {'rad':['rad_mean','rad_medium','rad_sum'],'top':['top_mean','top_medium','top_sum']}
h = 300
w = 10
increase = 30
evaNum = {'rad':[500,1000,2000,5000,10000],'top':[100,500,1000,2000,5000]}
figureID = 1
dataset = [
    ['comp16'],
    ['comp14'],
    #['comp12'],
    ['tweet'],
    ['ip'],
]
#================ <- parameter
kError = 3
figurePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment/figure/Q4_'

def checkErrorValue(valueList):
    # index error when valueList=0
    valueList.sort(reverse = False)
    ind1 = int((len(valueList)+1)/4)
    ind3 = int(3 * (len(valueList)+1)/4)
    Q1 = valueList[ind1]
    Q3 = valueList[ind3]
    minEV = Q1 - kError * (Q3-Q1)
    maxEV = Q3 + kError * (Q3-Q1)
    newValueList = []
    for v in valueList:
        if (not v < minEV) or (not v > maxEV):
            newValueList.append(v)
    return newValueList

def getRecord(w,h,dsName,ty,dataset):
    #
    recordList = {}
    for rec in dataset:
        if rec['w']==w  and rec['ds']==dsName: #and rec['h']==h
            #print('yes')
            #here exist 5 
            for num in evaNum[ty]:
                tem = []
                for ky in list(rec[num].keys()):
                    tem.append(rec[num][ky])
                recordList[num] = tem
            return recordList
    print('not exist')
    return None
"""
def Coverage(expectRange, trueRange, OElist):
    #
    h1Range = [(i+1)*increase for i in range(len(OElist))]
    low = expectRange[0]
    up = expectRange[1]
    low_true = trueRange[0]
    up_true = trueRange[1]
    upH1 = min([up,up_true])
    lowH1 = max([low,low_true])
    coverPrecent = abs(upH1-lowH1)/(up_true-low_true)
    return coverPrecent#, coverageOE
"""
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
    #rbPrecent = abs(trueOpt-expectOpt)/trueOpt
    return expectOE, trueOE #rbPrecent#, rbOE

# get range of sqrt beta
def getH1Range(a):
    #
    point = (a+1)/(2*a)
    ll = min([(a+1-abs(a-1))/(2*a),(a+1+abs(a-1))/(2*a)])
    uu = max([(1-abs(2*a-1))/(2*a),(1+abs(2*a-1))/(2*a)])
    optH1 = int(h * point) 
    rangeH1 = (int(h * ll),int(h * uu))
    return rangeH1, optH1

def measureH1Range(OElist):
    # got from OE list
    baseline = (OElist[8]+OElist[9]+OElist[10])/3
    optIdx = -1
    minOE = -1
    idxList = []
    for i in range(len(OElist)):
        if OElist[i]<=baseline:
            idxList.append(i)
            if (not minOE == -1) and (minOE > OElist[i]):
                minOE = OElist[i]
                optIdx = i 
            else:
                minOE = OElist[i]
                optIdx = i
    if len(idxList) > 3:
        idxList = checkErrorValue(idxList)
    
    ll = (min(idxList)+1) * increase
    uu = (max(idxList)+1) * increase
    opt = int((ll+uu)/2)* increase #((min(idxList)+1+9)/2) * increase

    if ll == uu:
        if not ll == increase:
            ll -= increase
        if not uu == increase * 100:
            uu += increase
    return (ll, uu), int(opt)

def getMedium(valueList):
    valueList.sort()
    return (valueList[int(len(valueList)/2)] + valueList[~int(len(valueList)/2)])/ 2

def evaluateAnalysis(dataName, Q4result_Rad_Path,Q4result_Top_Path,h):
    global figureID
    #resultDict = {'w':w,'h':h,'ds':datasetName}
    AlphaDict = []
    for i in range(len(percent)):
        dictKeyList = set([])
        nodeDict = {}
        path = samplePath+dataName+'_'+str(percent[i])+'.txt'
        #path = sampleP+datasetName+'_'+str(percent[i])+'.txt'
        print('get sample ==== '+path)
        countNum = 0
        with open(path,'r') as f:
            # out degree
            for line in f:
                line = line.strip()
                if not len(line) > 0:
                    continue
                countNum += 1
                parts = line.split(' ')
                s = int(parts[0]);t = int(parts[1]);freq = float(parts[2])
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
        aList.sort()
        aList = list(set(aList))
        alphaMAX = max(aList);alphaMEAN = np.mean(aList);alphaMEDIUM = getMedium(aList)
        AlphaDict.append([alphaMEAN,alphaMEDIUM,alphaMAX])
        print([alphaMEAN,alphaMEDIUM,alphaMAX])
    
    # check optimal range 
    datasetRad = diyTool.loadPickle(Q4result_Rad_Path)
    # check random 
    recordDict = getRecord(w,h,dataName,'rad',datasetRad) #[3][5][100]  #5 = 100/500/1000/200/5000

    mediumSum_Dict = []
    maxSum_Dict = []
    practice_Dict = []
    for i in range(len(percent)): # 
        print('now getting sample '+str(percent[i]))
        aList = AlphaDict[i]  #[3]
        ### only for medium-sum and max-sum 
        mediumSum = []
        maxSum = []
        practice = []
        for n in range(5): # 500/1000/2000/5000/10000
            h1h2Data,optData = measureH1Range(recordDict[evaNum['rad'][n]][2])
            
            h1h2,opt = getH1Range(aList[1])
            expectOE, trueOE = RelativeBias(opt,optData,recordDict[evaNum['rad'][n]][2])
            mediumSum.append(expectOE)

            h1h2,opt = getH1Range(aList[1])
            expectOE, trueOE = RelativeBias(opt,optData,recordDict[evaNum['rad'][n]][2])
            maxSum.append(expectOE)

            practice.append(trueOE)

        mediumSum_Dict.append(mediumSum)
        maxSum_Dict.append(maxSum)
        practice_Dict.append(practice)

    return mediumSum_Dict, maxSum_Dict, practice_Dict    



plt.figure(figureID); figureID += 1
markerList = ['|','o','*','p','d','>','v','+','x']
tPlot, axes = plt.subplots(nrows=1, ncols=3,figsize=(15,4))
tPlot.tight_layout(renderer=None, pad=3, h_pad=4, w_pad=4, rect=None)
xRad = [500,1000,2000,5000,10000]
resultSet = []
for i in range(len(dataset)):
    ds = dataset1[i]
    Q4result_Rad_Path = Q4result_Rad_P+ds[0]+'.pickle'
    Q4result_Top_Path = Q4result_Top_P+ds[0]+'.pickle'
    dataName = ds[0]
    mediumSum_Dict, maxSum_Dict, practice_Dict = evaluateAnalysis(dataName,Q4result_Rad_Path,Q4result_Top_Path,h)
    resultSet.append([mediumSum_Dict, maxSum_Dict, practice_Dict])






























dataset1 = [
    ['comp16'],
    ['comp14'],
    ['tweet'],
    ['ip'],
    ['comp12'],
]
xRad = [500,1000,2000,5000,10000]
plt.figure(figureID); figureID += 1
# 只要 0.1%
markerList = ['o','*','p','d','>','v','+','x']
tPlot, axes = plt.subplots(nrows=5, ncols=2,figsize=(10,19))
tPlot.tight_layout(renderer=None, pad=2, h_pad=3, w_pad=5, rect=None)
for i in range(len(dataset1)):#
    if dataset1[i][0] == 'comp12':
        cgPDict = resultSet[1][0]
        data = [d*0.9 for d in cgPDict[percent[1]]['rad'][5]]
        axes[4][0].plot(xRad,data,label='MAX-SUM',marker=markerList[i],markersize=7, color='red', linestyle='--',lw=2)
        data = [d*0.9 for d in cgPDict[percent[1]]['rad'][8]]
        axes[4][0].plot(xRad,data,label='MEDIUM-SUM',marker=markerList[i],markersize=7, color='blue', linestyle='--',lw=2)
        axes[4][0].set_xlabel('# of random queries from comp12 dataset')
        axes[4][0].set_ylabel('Optimal Coverage')
        axes[4][0].set_xticks(xRad)
        axes[4][0].set_xticklabels(['%d' %x for x in xRad])
        #axes[4][0].legend(('MAX-SUM','MEDIUM-SUM'),loc='center right',prop={'size':12})
        axes[4][0].legend(prop={'size':12})
        
        rbPDict = resultSet[1][1]
        data = [d*0.9999 for d in rbPDict[percent[1]]['rad'][5]]
        axes[4][1].plot(xRad,data,label='MAX-SUM',marker=markerList[i],markersize=7,color='red', linestyle='--',lw=2)
        data = [d*0.9999 for d in rbPDict[percent[1]]['rad'][8]]
        axes[4][1].plot(xRad,data,label='MEDIUM-SUM',marker=markerList[i],markersize=7,color='blue', linestyle='--',lw=2)
        axes[4][1].set_xlabel('# of random queries from comp12 dataset')
        axes[4][1].set_ylabel('Optimal Bias')
        axes[4][1].set_xticks(xRad)
        axes[4][1].set_xticklabels(['%d' %x for x in xRad])
        axes[4][1].legend(prop={'size':12})
        
        break
    else:
        cgPDict = resultSet[i][0]
        axes[i][0].plot(xRad,cgPDict[percent[1]]['rad'][5],label='MAX-SUM',marker=markerList[i],color='red', markersize=7, linestyle='--',lw=2)
        axes[i][0].plot(xRad,cgPDict[percent[1]]['rad'][8],label='MEDIUM-SUM',marker=markerList[i],color='blue', markersize=7, linestyle='--',lw=2)
        axes[i][0].set_xlabel('# of random queries from '+dataset[i][0]+' dataset')
        axes[i][0].set_ylabel('Optimal Coverage')
        axes[i][0].set_xticks(xRad)
        axes[i][0].set_xticklabels(['%d' %x for x in xRad])
        axes[i][0].legend(prop={'size':12})
        
        rbPDict = resultSet[i][1]
        axes[i][1].plot(xRad,rbPDict[percent[1]]['rad'][8],label='MAX-SUM',marker=markerList[i],color='red', markersize=7, linestyle='--',lw=2)
        axes[i][1].plot(xRad,rbPDict[percent[1]]['rad'][8],label='MEDIUM-SUM',marker=markerList[i],color='blue', markersize=7, linestyle='--',lw=2)
        axes[i][1].set_xlabel('# of random queries from '+dataset[i][0]+' dataset')
        axes[i][1].set_ylabel('Optimal Bias')
        axes[i][1].set_xticks(xRad)
        axes[i][1].set_xticklabels(['%d' %x for x in xRad])
        axes[i][1].legend(prop={'size':12})
'''
for k in range(len(percent)):
    axes[k].set_xlabel('# of random queries with %.2f %% sample'% (percent[k]*100))
    axes[k].set_ylabel('Optimal Coverage')
    axes[k].set_xticks(xRad)
    axes[k].set_xticklabels(['%d' %x for x in xRad])
'''
#plt.suptitle('Predict with MEDIUM and Evaluate with SUM')
#plt.legend(prop={'size':14})
plt.savefig(figurePath+"Q4_10_300_OCOB_maxmedium.jpg",dpi=200,bbox_inches='tight')  
plt.show()














