# -*- coding: utf-8 -*-
#===================  Import ->
# system
#import sys; sys.path.append("..")
#import copy 
import numpy as np
import matplotlib.pyplot as plt
#import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment")
# DIY
import diyTool
#===================  <- Import
#===================  path area ->
homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment/result/'# use '/' as ending
samplePath = 'D:/google desk PC/sample/'
Q4result_Rad_P = homePath + 'Q4_Rad_'
Q4result_Top_P = homePath + 'Q4_Top_'

#===================  <- path area
#================  parameter ->
percent = [0.2]#[0.01,0.03,0.05,0.1,0.2]
evaType = {'rad':['rad_mean','rad_medium','rad_sum'],'top':['top_mean','top_medium','top_sum']}
h = 300
w = 10
increase = 30
evaNum = {'rad':[500,1000,2000,5000,10000],'top':[100,500,1000,2000,5000]}
datasetName = 'tweet'
figureID = 1
dataset = [
    ['comp18'],
]
#================ <- parameter
kError = 3

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
            #here exist 5 
            for num in evaNum[ty]:
                tem = []
                for ky in list(rec[num].keys()):
                    tem.append(rec[num][ky])
                recordList[num] = tem
            return recordList
    print('not exist')
    return None

def Coverage(expectRange, trueRange, OElist):
    #
    h1Range = [(i+1)*increase for i in range(len(OElist))]
    low = expectRange[0]
    up = expectRange[1]
    low_true = trueRange[0]
    up_true = trueRange[1]

    upH1 = min([up,up_true])
    lowH1 = max([low,low_true])
    '''
    coverOE = [] 
    trueOE = []
    for i in range(len(OElist)):
        if (h1Range[i] <= upH1) and (h1Range[i] >= lowH1):
            coverOE.append(OElist[i])
        if (h1Range[i] <= up_true) and (h1Range[i] >= low_true):
            trueOE.append(OElist[i]) 
    '''
    coverPrecent = abs(upH1-lowH1)/(up_true-low_true)
    #coverageOE = sum(coverOE)/sum(trueOE)
    return coverPrecent#, coverageOE

def RelativeBias(expectOpt, trueOpt, OElist):
    #
    h1Range = [(OElist[i]+1)*increase for i in range(len(OElist))]
    expectOE = 0
    trueOE = 0
    for i in range(len(OElist)):
        if h1Range[i] > expectOpt:
            expectOE = OElist[i]
            break
    rbPrecent = abs(trueOpt-expectOpt)/trueOpt
    #OElist.sort(reverse = False) 
    #trueOE = np.mean(OElist[:3])
    #rbOE = abs(trueOE-expectOE)/trueOE
    return rbPrecent#, rbOE

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
    
    opt = (optIdx+1) * increase
    if opt < h:
        uu = h
    else:
        ll = h
    if ll == uu:
        if not ll == increase:
            ll -= increase
        if not uu == 100*increase:
            uu += increase 
    return (int(min([ll,uu])), int(max([ll,uu]))), int(opt)

def getMedium(valueList):
    valueList.sort()
    return (valueList[int(len(valueList)/2)] + valueList[~int(len(valueList)/2)])/ 2

def evaluateAnalysis(sampleP,Q4result_Rad_Path,Q4result_Top_Path,h):
    global figureID
    #resultDict = {'w':w,'h':h,'ds':datasetName}
    AlphaDict = []
    for i in range(len(percent)):
        dictKeyList = set([])
        nodeDict = {}
        path = sampleP+datasetName+'_'+str(percent[i])+'.txt'
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
        with open(path,'r') as f:
            for line in f:
                line = line.strip()
                if not len(line) > 0:
                    continue
                parts = line.split(' ')
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
    recordDict = getRecord(w,h,datasetName,'rad',datasetRad) #[3][5][100]  #5 = 100/500/1000/200/5000
    cgPDict = {}
    rbPDict = {}

    for i in range(len(percent)): # 
        aList = AlphaDict[i]  #[3]
        cgPList = [[] for _ in range(9)]
        rbPList = [[] for _ in range(9)]
        for j in range(len(aList)): #  3 types of getting alpha mean/medium/max
            print('===i j are '+str(i)+' '+str(j))
            h1h2,opt = getH1Range(aList[j])
            print('h1h2 '+str(h1h2))
            print('opt '+str(opt))
            for n in range(5): # 500/1000/2000/5000/10000 
                print('====== rad '+str(evaNum['rad'][n]))
                for k in range(3): # 3 types of evaluating observed error
                    print('=========evaluate way: '+evaType['rad'][k])
                    h1h2Data,optData = measureH1Range(recordDict[evaNum['rad'][n]][k])
                    print('h1h2Data '+str(h1h2Data))
                    print('opt '+str(optData))
                    cgP = Coverage(h1h2,h1h2Data,recordDict[evaNum['rad'][n]][k])
                    print('____cgP: '+str(cgP))
                    rbP = RelativeBias(opt,optData,recordDict[evaNum['rad'][n]][k])
                    print('____rbP: '+str(rbP))
                    print()                    
                    cgPList[j*3+k].append(cgP)
                    rbPList[j*3+k].append(rbP)
        cgPDict['rad'] = cgPList
        rbPDict['rad'] = rbPList

        cgPList = [[] for _ in range(9)]
        rbPList = [[] for _ in range(9)]
        recordDict = getRecord(w,h,datasetName,'top',datasetTop) #[3][5][100]  #5 = 100/500/1000/200/5000
        for j in range(len(aList)): #  3 types of getting alpha mean/medium/max
            print('===i j are '+str(i)+' '+str(j))
            h1h2,opt = getH1Range(aList[j])
            print('h1h2 '+str(h1h2))
            print('opt '+str(opt))
            for n in range(5): # 500/1000/2000/5000/10000 
                print('====== top '+str(evaNum['top'][n]))
                for k in range(3): # 3 types of evaluating observed error
                    print('=========evaluate way: '+evaType['top'][k])
                    h1h2Data,optData = measureH1Range(recordDict[evaNum['top'][n]][k])
                    print('h1h2Data '+str(h1h2Data))
                    print('opt '+str(optData))
                    cgP = Coverage(h1h2,h1h2Data,recordDict[evaNum['top'][n]][k])
                    print('____cgP: '+str(cgP))
                    rbP= RelativeBias(opt,optData,recordDict[evaNum['top'][n]][k])
                    print('____rbP: '+str(rbP))
                    print()
                    cgPList[j*3+k].append(cgP)
                    rbPList[j*3+k].append(rbP)
        cgPDict['top'] = cgPList
        rbPDict['top'] = rbPList

    return cgPDict, rbPDict


MediumSum = []
MaxSum = []
labelSet = []  
for ds in dataset:
    samplePath = sampleP+ds[0]+str(percent)+'.txt'
    Q4result_Rad_Path = Q4result_Rad_P+ds[0]+'.pickle'
    Q4result_Top_Path = Q4result_Top_P+ds[0]+'.pickle'
    dataName = ds[0]
    cgPDict, rbPDict = evaluateAnalysis(sampleP,Q4result_Rad_Path,Q4result_Top_Path,h)

    MediumSum.append([cgPDict['rad'][5],cgPDict['top'][5],rbPDict['rad'][5],rbPDict['top'][5]])
    MaxSum.append([cgPDict['rad'][8],cgPDict['top'][8],rbPDict['rad'][8],rbPDict['top'][8]])
    labelSet.append(dataName)

ax = [(0,0),(0,1),(1,0),(1,1)]
markerList = ['|','o','*','p','d','>','v','+','x']
wholeName = ["Rad Query: Coverage percent","Top Query: Coverage percent","Rad Query: Relaive-bias percent","Top Query: Relaive-bias percent"]
plt.figure(figureID); figureID += 1
tPlot, axes = plt.subplots(nrows=2, ncols=2,figsize=(20,15))
tPlot.tight_layout(renderer=None, pad=3, h_pad=4, w_pad=4, rect=None)
x = {0:[500,1000,2000,5000,10000],1:[100,500,1000,2000,5000]}
for k in range(4):
    i,j = ax[k]
    for n in range(len(dataset)):
        axes[i][j].plot(x[int(k%2)],MediumSum[k][n],label=labelSet[n],marker=markerList[n],markersize=9, linestyle='--',lw=4)
        axes[i][j].set_xlabel('query size')
        axes[i][j].set_ylabel('ratio value')
        axes[i][j].set_title(wholeName[k])
        axes[i][j].set_xticks(x)
        axes[i][j].set_xticklabels(x)
plt.legend(prop={'size':18})
plt.savefig("D:/google desk PC/Q4_"+str(percent[0])+"_rad.jpg",dpi=200)  
plt.show()

'''
ax = [(0,0),(0,1),(1,0),(1,1)]
markerList = ['|','o','*','p','d','>','v','+','x']
wholeName = ["Rad Query: Coverage percent","Top Query: Coverage percent","Rad Query: Relaive-bias percent","Top Query: Relaive-bias percent"]
plt.figure(figureID); figureID += 1
tPlot, axes = plt.subplots(nrows=2, ncols=2,figsize=(20,15))
tPlot.tight_layout(renderer=None, pad=3, h_pad=4, w_pad=4, rect=None)
x = {0:[500,1000,2000,5000,10000],1:[100,500,1000,2000,5000]}
for k in range(4):
    i,j = ax[k]
    for n in range(len(dataset)):
        axes[i][j].plot(x[int(k%2)],MaxSum[k][n],label=dataset[],marker=markerList[n],markersize=9, linestyle='--',lw=4)
        axes[i][j].set_xlabel('query size')
        axes[i][j].set_ylabel('ratio value')
        axes[i][j].set_title(wholeName[k])
        axes[i][j].set_xticks(x)
        axes[i][j].set_xticklabels(x)
plt.legend(prop={'size':18})
plt.savefig("D:/google desk PC/Q4_"+datasetName+"_h"+str(h)+"_20%_rad.jpg",dpi=200)  
plt.show()
'''