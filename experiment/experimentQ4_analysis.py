"""
load data

evaluate

draw figure
"""
# -*- coding: utf-8 -*-
"""
    Test Q4, the Eq( ) 
"""
#===================  Import ->
# system
#import sys; sys.path.append("..")
import copy 
import numpy as np
#import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment")
# DIY
import diyTool
#===================  <- Import
#===================  path area ->
homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment/result/'# use '/' as ending
sampleP = 'D:/google desk PC/sample/'
Q4result_Rad_Path = homePath + 'Q4_Rad_'
Q4result_Top_Path = homePath + 'Q4_Top_'
Q4evaluate_Rad_Path = homePath + 'Q4_Rad_evaluate'
Q4evaluate_Top_Path = homePath + 'Q4_Top_evaluate'
#===================  <- path area
#================  parameter ->
Epsilon = [i+1 for i in range(10)]
dataset = [ 
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp18.txt',338239,'comp18', 0.90],
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp16.txt',1391333,'comp16', 0.90],
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp14.txt',7904564,'comp14', 0.70],
    #['D:/google desk PC/ip_graph_refined',4213084,'ip', 0.90]
    ['C:/Users/alfonso.yan/Documents/tweet_stream_hashed_refined',17813281,'tweet', 0.60],
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp10.txt',1372146644,'comp1', 0.05]
]
percent = [0.2]#[0.01,0.03,0.05,0.1,0.2]
evaType = {'rad':['rad_mean','rad_medium','rad_sum'],'top':['top_mean','top_medium','top_sum']}
h = 300
w = 10
increase = 30
evaNum = {'rad':[500,1000,2000,5000,10000],'top':[100,500,1000,2000,5000]}
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
        if rec['w']==w and rec['h']==h and rec['ds']==dsName:
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
    coverOE = [] 
    trueOE = []
    
    for i in range(len(OElist)):
        if (h1Range[i] <= upH1) and (h1Range[i] >= lowH1):
            coverOE.append(OElist[i])
        if (h1Range[i] <= up_true) and (h1Range[i] >= low_true):
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
    OElist.sort(reverse = False) 
    trueOE = np.mean(OElist[:3])
    rbPrecent = abs(trueOpt-expectOpt)/trueOpt
    rbOE = abs(trueOE-expectOE)/trueOE
    return rbPrecent, rbOE

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
evaluateDict = []
for ds in dataset:
    resultDict = {'w':w,'h':h,'ds':ds[2]}
    AlphaDict = []
    for i in range(len(percent)):
        meanList = []
        mediumList = []
        dictKeyList = set([])
        nodeDict = {}
        path = sampleP+ds[2]+'_'+str(percent[i])+'.txt'
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
    rad_path = Q4result_Rad_Path + ds[2]+'.pickle'
    top_path = Q4result_Top_Path + ds[2]+'.pickle'
    datasetRad = diyTool.loadPickle(rad_path)
    datasetTop = diyTool.loadPickle(top_path)
    # check random 
    recordDict = getRecord(w,h,ds[2],'rad',datasetRad) #[3][5][100]  #5 = 100/500/1000/200/5000
    cgPDict = {}
    cgVDict = {}
    rbPDict = {}
    rbVDict = {}
    for i in range(len(percent)): # 
        aList = AlphaDict[i]  #[3]
        cgPList = [[] for _ in range(9)]
        cgVList = [[] for _ in range(9)]
        rbPList = [[] for _ in range(9)]
        rbVList = [[] for _ in range(9)]
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
                    cgP, cgV = Coverage(h1h2,h1h2Data,recordDict[evaNum['rad'][n]][k])
                    #evaluateCG[i][j][k] = [cgP, cgV] 
                    print('____cgP: '+str(cgP))
                    print('____cgV: '+str(cgV))
                    rbP, rbV = RelativeBias(opt,optData,recordDict[evaNum['rad'][n]][k])
                    #evaluateRB[i][j][k] = [rbP, rbV]
                    print('____rbP: '+str(rbP))
                    print('____rbV: '+str(rbV))
                    print()
                    
                    cgPList[j*3+k].append(cgP)
                    cgVList[j*3+k].append(cgV)
                    rbPList[j*3+k].append(rbP)
                    rbVList[j*3+k].append(rbV)
        cgPDict['rad'] = cgPList
        cgVDict['rad'] = cgVList
        rbPDict['rad'] = rbPList
        rbVDict['rad'] = rbVList

        cgPList = [[] for _ in range(9)]
        cgVList = [[] for _ in range(9)]
        rbPList = [[] for _ in range(9)]
        rbVList = [[] for _ in range(9)]
        recordDict = getRecord(w,h,ds[2],'top',datasetTop) #[3][5][100]  #5 = 100/500/1000/200/5000
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
                    cgP, cgV = Coverage(h1h2,h1h2Data,recordDict[evaNum['top'][n]][k])
                    #evaluateCG[i][j][k] = [cgP, cgV] 
                    print('____cgP: '+str(cgP))
                    print('____cgV: '+str(cgV))
                    rbP, rbV = RelativeBias(opt,optData,recordDict[evaNum['top'][n]][k])
                    #evaluateRB[i][j][k] = [rbP, rbV]
                    print('____rbP: '+str(rbP))
                    print('____rbV: '+str(rbV))
                    print()
                    
                    cgPList[j*3+k].append(cgP)
                    cgVList[j*3+k].append(cgV)
                    rbPList[j*3+k].append(rbP)
                    rbVList[j*3+k].append(rbV)
        cgPDict['top'] = cgPList
        cgVDict['top'] = cgVList
        rbPDict['top'] = rbPList
        rbVDict['top'] = rbVList
    evaluateDict.append([cgPDict,cgVDict,rbPDict,rbVDict])
    #diyTool.savePickle(Q4evaluate_Rad_Path,evaluateRad)
    #diyTool.savePickle(Q4evaluate_Top_Path,evaluateTop)






import matplotlib.pyplot as plt
plt.figure(1)
tPlot, axes = plt.subplots(nrows=2, ncols=2,figsize=(20,15))
tPlot.tight_layout(renderer=None, pad=5, h_pad=5, w_pad=5, rect=None)
ax = [(0,0),(0,1),(1,0),(1,1)]
x = [500,1000,2000,5000,10000]
wholeData = [cgPDict['rad'],cgVDict['rad'],rbPDict['rad'],rbVDict['rad']]
wholeName = ["Coverage percent","Coverage value","Relaive-bias percent","Relaive-bias Value"]
markerList = ['|','o','*','p','d','>','v','+','x']
labelSet = ['mean-mean','mean-medium','mean-sum','medium-mean','medium-medium','medium-sum','max-mean','max-medium','max-sum']
for k in range(4):
    i,j = ax[k]
    for n in range(9):
        axes[i][j].plot(x,wholeData[k][n], label=labelSet[n],marker=markerList[n],markersize=8, linestyle='--',lw=3)
        axes[i][j].set_xlabel('query size')
        axes[i][j].set_ylabel('ratio value')
        axes[i][j].set_title(wholeName[k])
        axes[i][j].set_xticks(x)
        axes[i][j].set_xticklabels(x)
#plt.title("sample size = 20%, dataset = comp18, h=300")  
plt.legend(prop={'size':18})
plt.savefig("D:/google desk PC/Q4_tweet_h300_20%_rad.jpg",dpi=200)  
plt.show()

plt.figure(2)
tPlot, axes = plt.subplots(nrows=2, ncols=2,figsize=(20,15))
tPlot.tight_layout(renderer=None, pad=5, h_pad=5, w_pad=5, rect=None)
ax = [(0,0),(0,1),(1,0),(1,1)]
x = [500,1000,2000,5000,10000]
wholeData = [cgPDict['top'],cgVDict['top'],rbPDict['top'],rbVDict['top']]
wholeName = ["Coverage percent","Coverage value","Relaive-bias percent","Relaive-bias Value"]
markerList = ['|','o','*','p','d','>','v','+','x']
labelSet = ['mean-mean','mean-medium','mean-sum','medium-mean','medium-medium','medium-sum','max-mean','max-medium','max-sum']
for k in range(4):
    i,j = ax[k]
    for n in range(9):
        axes[i][j].plot(x,wholeData[k][n], label=labelSet[n],marker=markerList[n],markersize=8, linestyle='--',lw=3)
        axes[i][j].set_xlabel('query size')
        axes[i][j].set_ylabel('ratio value')
        axes[i][j].set_title(wholeName[k])
        axes[i][j].set_xticks(x)
        axes[i][j].set_xticklabels(x)
#plt.title("sample size = 20%, dataset = comp18, h=300")  
plt.legend(prop={'size':18})
plt.savefig("D:/google desk PC/Q4_tweet_h300_20%_top.jpg",dpi=200)  
plt.show()