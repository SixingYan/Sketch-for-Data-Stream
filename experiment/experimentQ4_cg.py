#import os;os.chdir('D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment');import experimentQ4_cg
#===================  Import ->
# system
#import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment")
#import sys; sys.path.append("..")
import random
import numpy as np
# DIY
#import lib
import diyTool
#import lib.hSketch as hSketch
import gMatrix
import cSketch
#===================  <- Import

#================  parameter ->
w = 10
num1 = 0
num2 = 100
increase = 30
h = 1000
dataset = [ 
    #['D:/google desk PC/graph_freq_comp18.txt',338239,'comp18', 0.80],
    #['D:/google desk PC/graph_freq_comp16.txt',1391333,'comp16', 0.80],
    #['D:/google desk PC/graph_freq_comp14.txt',7904564,'comp14', 0.60],
    #['D:/google desk PC/ip_graph_refined',4213084,'ip', 0.70],
    #['D:/google desk PC/tweet_stream_hashed_refined',17813281,'tweet']#
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp12.txt',31160379,'comp12', 90],
    ['/data1/Sixing/stream dataset/graph_freq_comp10.txt',56175513,'comp1', 0.03]
]
datasetRad = []
datasetTop = []
#================ <- parameter

#===================  path area ->
#homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment/result/'# use '/' as ending
homePath = '/data1/Sixing/expdata/'
topPath = '/data1/Sixing/expdata/top5000_'
Q4result_Top_Path = homePath+'Q4_TopCG_'+str(h)+'_'
Q4result_Rad_Path = homePath+'Q4_RadCG_'+str(h)+'_'
#===================  <- path area

def getMedium(valueList):
    valueList.sort()
    return (valueList[int(len(valueList)/2)] + valueList[~int(len(valueList)/2)])/ 2

def getH1H2(num1,num2,h):
    h1h2List = []
    for i in range(num1,num2):
        h1 = (i+1)*increase
        h2 = int(h**2/h1)
        h1h2List.append((h1,h2))
    return h1h2List

def getRadList(num,radPool):
    radList = [[] for i in range(5)]
    for i in range(len(radList)):
        while len(radList[i]) < num:
            tem = random.choice(radPool)
            if tem not in radList[i]:
                radList[i].append(tem)
    return radList

def evaluate_top_medium(sketch,topList):
    #
    valueList = []
    for parts in topList:
        s=parts[0]; t=parts[1];freq = parts[2]
        estiValue = sketch.edge_frequency_query((s,t))
        valueList.append(abs(estiValue-freq)/freq)
    ObservedError = getMedium(valueList)
    print('ObservedError is '+str(ObservedError))
    return ObservedError

def evaluate_top_mean(sketch,topList):
    #
    valueList = []
    for parts in topList:
        s=parts[0]; t=parts[1];freq = parts[2]
        estiValue = sketch.edge_frequency_query((s,t))
        valueList.append(abs(estiValue-freq)/freq)
    ObservedError = np.mean(valueList)
    print('ObservedError is '+str(ObservedError))
    return ObservedError

def evaluate_top_sum(sketch,topList):
    totalLoss1 = 0;totalFreq1 = 0
    for parts in topList:
        s=parts[0]; t=parts[1];freq = parts[2]
        estiValue = sketch.edge_frequency_query((s,t))
        totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
    ObservedError = totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError))
    return ObservedError

def evaluate_rad_medium(sketch,radList):
    #
    ObservedError = 0
    for i in range(len(radList)):
        totalLoss1 = []
        for parts in radList[i]:
            s=parts[0]; t=parts[1];freq = parts[2]
            estiValue = sketch.edge_frequency_query((s,t))
            totalLoss1.append(abs(estiValue-freq)/freq)
        ObservedError += getMedium(totalLoss1) 
    print('ObservedError is '+str(ObservedError/len(radList)))
    return ObservedError/len(radList)

def evaluate_rad_mean(sketch,radList):
    #
    ObservedError = 0
    for i in range(len(radList)):
        totalLoss1 = []
        for parts in radList[i]:
            s=parts[0]; t=parts[1];freq = parts[2]
            estiValue = sketch.edge_frequency_query((s,t))
            totalLoss1.append(abs(estiValue-freq)/freq)
        ObservedError += np.mean(totalLoss1) 
    print('ObservedError is '+str(ObservedError/len(radList)))
    return ObservedError/len(radList)

def evaluate_rad_sum(sketch,radList):
    #
    ObservedError = 0
    for i in range(len(radList)):
        totalLoss1 = 0;totalFreq1 = 0
        for parts in radList[i]:
            s=parts[0]; t=parts[1];freq = parts[2]
            estiValue = sketch.edge_frequency_query((s,t))
            totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
        ObservedError += totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError/len(radList)))
    return ObservedError/len(radList)

def getTopList(dsName):
    top5000List = []
    #home = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/data/top5000_'
    path = topPath+dsName+'.txt'
    #path = home+dsName+'.txt'
    with open(path,'r') as f:
        for line in f.readlines():
            line = line.strip()
            if len(line)>0:
                parts = line.split(' ')
                s = int(parts[0])
                t = int(parts[1])
                freq = float(parts[2])
                top5000List.append([s,t,freq])
    return top5000List

for ds in dataset:
    print('========dataset:  '+str(ds))
    topNum = [100,500,1000,2000,5000] 
    radNum = [500,1000,2000,5000,10000]
    rad10000List = [];top5000List = []
    countNum = 0
    maxNodeID = int(ds[1]) 
    edgeMax = int(str(maxNodeID)+str(maxNodeID))
    cS = cSketch.sketch(w,h**2,edgeMax)
    gM = gMatrix.sketch(w,h,maxNodeID)
    radPool = []
    print('========start stream')# start stream
    with open(ds[0],'r') as f:
        for line in f:
        #for line in f.readlines():
            line = line.strip()
            if len(line)>0:
                countNum += 1
                if countNum % 1000000 == 0:
                    print('now is '+str(countNum))
                parts = line.split(' ')
                s = int(parts[0])
                t = int(parts[1])
                freq = float(parts[2])

                if random.random()>0.4:
                    continue
                # get rad and top
                if random.random()<0.2:
                    radPool.append([s,t,freq])
                '''
                if len(top5000List)>5000:
                    minV = min(top5000List, key=lambda x: x[2])
                    if freq>minV[2]:
                        indx = top5000List.index(minV);top5000List[indx] = [s,t,freq]
                else:
                    top5000List.append([s,t,freq])
                '''
                # update 
                cS.update((s,t),freq)
                gM.update((s,t),freq)

    print('========evaluation')# evaluation
    top5000List = getTopList(ds[2])
    topList = []; radList = []
    #top5000List.sort(key= lambda d : d[2], reverse = True)
    for i in range(len(topNum)):
        topList.append(top5000List[:topNum[i]])
        radList.append(getRadList(radNum[i],radPool))
    del radPool # clean

    print('============start top')

    tem = {'h':h,'w':w,'ds':ds[2],'sketch':'cs'}
    print('----------cs')# random
    for j in range(len(topList)): # 5
        tem[topNum[j]] = {}
        print('====now is '+str(topNum[j]))
        ObservedError = evaluate_top_mean(cS,topList[j]);top_mean = ObservedError
        ObservedError = evaluate_top_medium(cS,topList[j]);top_medium = ObservedError
        ObservedError = evaluate_top_sum(cS,topList[j]);top_sum = ObservedError
        tem[topNum[j]]['top_mean'] = top_mean
        tem[topNum[j]]['top_medium'] = top_medium
        tem[topNum[j]]['top_sum'] = top_sum
    datasetTop.append(tem)
    
    tem = {'h':h,'w':w,'ds':ds[2],'sketch':'gm'}
    print('----------gm')# random
    for j in range(len(topList)): # 5
        tem[topNum[j]] = {}
        print('====now is '+str(topNum[j]))
        ObservedError = evaluate_top_mean(gM,topList[j]);top_mean = ObservedError
        ObservedError = evaluate_top_medium(gM,topList[j]);top_medium = ObservedError
        ObservedError = evaluate_top_sum(gM,topList[j]);top_sum = ObservedError
        tem[topNum[j]]['top_mean'] = top_mean
        tem[topNum[j]]['top_medium'] = top_medium
        tem[topNum[j]]['top_sum'] = top_sum
    datasetTop.append(tem)

    print('============start rad')

    tem1 = {'h':h,'w':w,'ds':ds[2],'sketch':'cs'}
    print('----------cs')# random
    for j in range(len(radList)): # 5
        tem1[radNum[j]] = {}
        rad_mean = []
        rad_medium = []
        rad_sum = []
        print('====now is '+str(radNum[j]))
        ObservedError = evaluate_rad_mean(cS,radList[j]);rad_mean = ObservedError
        ObservedError = evaluate_rad_medium(cS,radList[j]);rad_medium = ObservedError
        ObservedError = evaluate_rad_sum(cS,radList[j]);rad_sum = ObservedError
        tem1[radNum[j]]['rad_mean'] = rad_mean
        tem1[radNum[j]]['rad_medium'] = rad_medium
        tem1[radNum[j]]['rad_sum'] = rad_sum
    datasetRad.append(tem1)

    tem1 = {'h':h,'w':w,'ds':ds[2],'sketch':'gm'}
    print('----------gm')# random
    for j in range(len(radList)): # 5
        tem1[radNum[j]] = {}
        rad_mean = []
        rad_medium = []
        rad_sum = []
        print('====now is '+str(radNum[j]))
        ObservedError = evaluate_rad_mean(gM,radList[j]);rad_mean = ObservedError
        ObservedError = evaluate_rad_medium(gM,radList[j]);rad_medium = ObservedError
        ObservedError = evaluate_rad_sum(gM,radList[j]);rad_sum = ObservedError
        tem1[radNum[j]]['rad_mean'] = rad_mean
        tem1[radNum[j]]['rad_medium'] = rad_medium
        tem1[radNum[j]]['rad_sum'] = rad_sum
    datasetRad.append(tem1)

    print('========saving') # saving .......
    diyTool.savePickle(Q4result_Top_Path+ds[2],datasetTop)
    diyTool.savePickle(Q4result_Rad_Path+ds[2],datasetRad)
