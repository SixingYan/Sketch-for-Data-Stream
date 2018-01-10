

#===================  Import ->
# system
import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment")
import sys; sys.path.append("..")
import copy
import random
import numpy as np
# DIY
#import lib
import lib.diyTool as diyTool
import lib.hSketch as hSketch
#===================  <- Import

#================  parameter ->
w = 10
num1 = 0
num2 = 100
increase = 30
h = 300
dataset = [ 
    #['D:/google desk PC/graph_freq_comp18.txt',338239,'comp18', 0.80],
    #['D:/google desk PC/graph_freq_comp16.txt',1391333,2,'comp16', 0.80],
    #['D:/google desk PC/graph_freq_comp14.txt',7904564,2,'comp14', 0.60],
    #['D:/google desk PC/ip_graph_refined',4213084,2,'ip', 0.70],
    ['D:/google desk PC/tweet_stream_hashed_refined',17813281,'tweet']#
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp12.txt',338239,2,'comp18', 90],
    #['D:/google desk PC/graph_freq_comp10.txt',1372146644,2,'comp1', 0.03]
]
datasetRad = []
datasetTop = []
#================ <- parameter

#===================  path area ->
homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment/result/'# use '/' as ending
Q4result_Top_Path = homePath+'Q4_Top'
Q4result_Rad_Path = homePath+'Q4_Rad'
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

for ds in dataset:
    print('========dataset:  '+str(ds))
    topNum = [100,500,1000,2000,5000] 
    radNum = [500,1000,2000,5000,10000]
    rad10000List = [];top5000List = []
    countNum = 0
    h1h2List = getH1H2(num1,num2,h)
    sketchList = []
    for i in range(len(h1h2List)):
        h1,h2 = h1h2List[i]
        print('for %d, h1 is %d   h2 is %d'%(i,h1,h2))
        hS = copy.deepcopy(hSketch.sketch(w,h1,h2,ds[1]))
        sketchList.append(hS)
    radPool = []
    print('========start stream')# start stream
    with open(ds[0],'r') as f:
        for line in f:
            line = line.strip()
            if len(line)>0:
                countNum += 1
                if countNum % 1000000 == 0:
                    print('now is '+str(countNum))
                parts = line.split(' ')
                s = int(parts[0])
                t = int(parts[1])
                freq = float(parts[2])

                #if random.randint(0,10000)>10000 * 0.5:
                #    continue

                # get rad and top
                if random.randint(0,10000)<10000 * 0.2:
                    radPool.append([s,t,freq])
                
                if len(top5000List)>5000:
                    minV = min(top5000List, key=lambda x: x[2])
                    if freq>minV[2]:
                        indx = top5000List.index(minV);top5000List[indx] = [s,t,freq]
                else:
                    top5000List.append([s,t,freq])

                # update 
                for i in range(len(sketchList)):
                    sketchList[i].update((s,t),freq)

    print('========evaluation')# evaluation
    topList = []; radList = []
    top5000List.sort(reverse = False)
    for i in range(len(topNum)):
        topList.append(top5000List[:topNum[i]])
        radList.append(getRadList(radNum[i],radPool))
    del radPool # clean

    sketchOE = {'h':h,'w':w,'ds':ds[2]}
    tem = copy.deepcopy(sketchOE)
    # topList
    print('----------top')# random
    for j in range(len(topList)): # 5
        tem[topNum[j]] = {}
        top_mean = []
        top_medium = []
        top_sum = []
        print('====now is '+str(topNum[j]))
        for i in range(len(sketchList)): #150?
            ObservedError = evaluate_top_mean(sketchList[i],topList[j]);top_mean.append(ObservedError)
            print()
            ObservedError = evaluate_top_medium(sketchList[i],topList[j]);top_medium.append(ObservedError)
            print()
            ObservedError = evaluate_top_sum(sketchList[i],topList[j]);top_sum.append(ObservedError)
            print()
        tem[topNum[j]]['top_mean'] = top_mean
        tem[topNum[j]]['top_medium'] = top_medium
        tem[topNum[j]]['top_sum'] = top_sum
    datasetTop.append(tem)

    # radList
    print('----------random')# random
    for j in range(len(radList)): # 5
        tem[radNum[j]] = {}
        rad_mean = []
        rad_medium = []
        rad_sum = []
        print('====now is '+str(radNum[j]))
        for i in range(len(sketchList)): #150?
            ObservedError = evaluate_rad_mean(sketchList[i],radList[j]);rad_mean.append(ObservedError)
            print()
            ObservedError = evaluate_rad_medium(sketchList[i],radList[j]);rad_medium.append(ObservedError)
            print()
            ObservedError = evaluate_rad_sum(sketchList[i],radList[j]);rad_sum.append(ObservedError)
            print()
        tem[radNum[j]]['rad_mean'] = rad_mean
        tem[radNum[j]]['rad_medium'] = rad_medium
        tem[radNum[j]]['rad_sum'] = rad_sum
    datasetRad.append(tem)

    print('========saving') # saving .......
    diyTool.savePickle(Q4result_Top_Path,datasetTop)
    diyTool.savePickle(Q4result_Rad_Path,datasetRad)
