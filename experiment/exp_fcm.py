import copy
import random
#import numpy as np
import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment")
import sys; sys.path.append("..")
# DIY
#import lib
#import diyTool
import lib.fMODsketch as fMODsketch
import lib.faCounter as faCounter
#from lib.diyTool import getPathDict, getStrategy
"""
1. filter: store high freq. edge  
    @ store
    @ update

2. sketch update
    @ if high-freq. or not 
    @ offset/gap/# to update the sketch 
"""
'''
sgStrList = ['3C0S2C1','3C0S2S1','3C1C0S2',
'3C1S2C0','3C1S2S0','3C2C0S1','3C2C1C0','3C2C1S0','3C2S1C0',
'3C2S1S0','3S2C0S1','3S2C1C0','3S2C1S0','3S2S1C0','3S2S1S0',]

def getMODlist():
    sghList = []
    for ss in sgStrList:
        d = getPathDict(ss)
        sg = getStrategy(d)
        hList = []
        for tp in sg:
            hList.append(h**len(tp))
        sghList.append([sg,hList])
    return sghList
'''
def getRadList(num,radPool):
    radList = [[] for i in range(5)]
    for i in range(len(radList)):
        while len(radList[i]) < num:
            tem = random.choice(radPool)
            if tem not in radList[i]:
                radList[i].append(tem)
    return radList

def getH1H2(num1,num2,h):
    h1h2List = []
    for i in range(num1,num2):
        h1 = (i+1)*increase
        h2 = int(h**2/h1)
        h1h2List.append((h1,h2))
    for i in range(num1,num2):
        h2 = (i+1)*increase
        h1 = int(h**2/h2)
        h1h2List.append((h1,h2))
    return h1h2List

def evaluate_rad_sum(sketch,radList,mgCounter):
    #
    ObservedError = 0
    for i in range(len(radList)):
        totalLoss1 = 0;totalFreq1 = 0
        for parts in radList[i]:
            edge=parts[0];freq = parts[1]
            if mgCounter.query(edge):
                flag = 1
            else:
                flag = 0
            estiValue = sketch.query(flag,edge)
            totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
        ObservedError += totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError/len(radList)))
    return ObservedError/len(radList)

def evaluate_top_sum(sketch,topList,mgCounter):
    totalLoss1 = 0;totalFreq1 = 0
    for parts in topList:
        edge=parts[0];freq = parts[1]
        if mgCounter.query(edge):
            flag = 1
        else:
            flag = 0
        estiValue = sketch.query(flag,edge)
        totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
    ObservedError = totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError))
    return ObservedError

'''
#samplePath = '/data1/Sixing/expdata/sample/' # train the counter
samplePath = 'F:/sample/comp18_0.05.txt'
with open(samplePath,'r') as f:
    for line in f:
        if not len(line) > 0:
            continue
        parts = line.split(' ')
        s = int(parts[0]);t = int(parts[1]);freq = float(parts[2])
        edge = (s,t) 
        faCounter.update(edge,freq)
'''
num1 = 0
num2 = 1
maxNodeID = 17813281
maxIDList = [maxNodeID,maxNodeID]
h = 100
increase = 10
w = 13
hw = 4
lw = 9
winSize = 1000

homePath = 'D:/'# use '/' as ending
Q4result_Top_Path = homePath+'Q4_Top_symCG_'+str(h)+'_'
Q4result_Rad_Path = homePath+'Q4_Rad_symCG_'+str(h)+'_'
#streamPath = '/data1/Sixing/stream dataset/tweet_stream_hashed_refined' # process stream
streamPath = 'D:/google desk PC/graph_freq_comp18.txt' # process stream

'''
sketchList = []
for i in range(len(h1h2List)):
    h1,h2 = h1h2List[i]
    print('for %d, h1 is %d   h2 is %d'%(i,h1,h2))
    hS = copy.deepcopy(hSketch.sketch(w,h1,h2,maxNodeID))
    sketchList.append(hS)
    edgeMax = int(str(maxNodeID)+str(maxNodeID))
    cS = cSketch.sketch(w,h**2,edgeMax)
    gM = gMatrix.sketch(w,h,maxNodeID)
'''
# preparing
#sghList = getMODlist
MODList = []
h1h2List = getH1H2(num1,num2,h)
print('build......')
for i in range(len(h1h2List)):
    h1,h2 = h1h2List[i]
    print(''+str((h1,h2)))
    mod = copy.deepcopy(fMODsketch.fMODsketch(maxIDList,[h1,h2],w,hw,lw,[[0],[1]]))
    mod.buildSketch()
    MODList.append(mod)

cS = copy.deepcopy(fMODsketch.fMODsketch(maxIDList,[h**2],w,hw,lw,[[0,1]]))
cS.buildSketch()
mgCounter = faCounter.faCounter(winSize)

# streaming 
radPool = [];top300List = []
print('start stream')
with open(streamPath,'r') as f:
    for line in f:
        if not len(line) > 0:
            continue
        flag = 0
        parts = line.split(' ')
        s = int(parts[0]);t = int(parts[1]);freq = float(parts[2])
        mgCounter.update((s,t), freq)
        if mgCounter.query((s,t)):
            flag = 1

        if random.random()> 0.4:
            continue
        if random.random()< 0.3:
            radPool.append([(s,t),freq])
        if len(top300List)>300:
            minV = min(top300List, key=lambda x: x[1])
            if freq>minV[1]:
                indx = top300List.index(minV);top300List[indx] = [(s,t),freq]
        else:
            top300List.append([(s,t),freq])

        # update 
        cS.update(flag, (s,t),freq)
        for i in range(len(MODList)):
            MODList[i].update(flag, (s,t),freq)

rad3000List = getRadList(3000,radPool)
del radPool # clean

print('\n evaluation')
with open(Q4result_Top_Path,'a') as f:
    for i in range(len(MODList)): #
        ObservedError = evaluate_top_sum(MODList[i],top300List,mgCounter)
        f.write(str(h1h2List[i])+' : '+str(ObservedError))

    ObservedError = evaluate_top_sum(cS,top300List,mgCounter)
    f.write('Count-Min: '+str(ObservedError))

with open(Q4result_Rad_Path,'a') as f:
    for i in range(len(MODList)): #
        ObservedError = evaluate_rad_sum(MODList[i],rad3000List,mgCounter)
        f.write(str(h1h2List[i])+' : '+str(ObservedError))

    ObservedError = evaluate_rad_sum(cS,rad3000List,mgCounter)
    f.write('Count-Min: '+str(ObservedError))
