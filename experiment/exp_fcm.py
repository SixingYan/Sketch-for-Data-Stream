import copy
import random
#import numpy as np
#import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment")
#import sys; sys.path.append("..")
# DIY
#import lib
#import diyTool
#import lib.fMODsketch as fMODsketch
#import lib.faCounter as faCounter
#from lib.diyTool import getPathDict, getStrategy
import fMODsketch
import faCounter
from diyTool import evaluate_rad_sum_counter, evaluate_top_sum_counter
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

num1 = 0
num2 = 10
dataName = 'sanus_fre_4ij'#'tr_fre_4ij' #'tweet'
maxNodeID = 100000000 #
maxIDList = [maxNodeID,maxNodeID]
h = 2000
increase = 200
w = 13
hw = 4;lw = 9
winSize = 10000
homePath = '/data1/Sixing/expdata/'# use '/' as ending
Q4result_Top_Path = homePath+'Q4_Top_symCG_'+str(h)+'_'
Q4result_Rad_Path = homePath+'Q4_Rad_symCG_'+str(h)+'_'
#streamPath = '/data1/Sixing/stream dataset/tr_fre_4ij' # process stream
streamPath = '/data1/Sixing/stream dataset/sanus_fre_4ij' # process stream
#streamPath = '/data1/Sixing/stream dataset/tweet_stream_hashed_refined' # process stream
#streamPath = 'D:/google desk PC/graph_freq_comp18.txt' # process stream

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

countNum = 0
# streaming 
radPool = [];top300List = []
print('start stream......')
with open(streamPath,'r') as f:
    for line in f:
        if not len(line) > 0:
            continue
        countNum += 1
        if countNum > 1000000:
            break
        flag = 0
        parts = line.split ('')
        s = int(parts[0]);t = int(parts[1]);freq = float(parts[2])
        mgCounter.update((s,t), freq)
        if mgCounter.query((s,t)):
            flag = 1

        if random.random()> 0.5:
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

print('\n evaluation......')
with open(Q4result_Top_Path+dataName,'a') as f:
    for i in range(len(MODList)): #
        ObservedError = evaluate_top_sum_counter(MODList[i],top300List,mgCounter)
        f.write(str(h1h2List[i])+' : '+str(ObservedError)+'\n')

    ObservedError = evaluate_top_sum_counter(cS,top300List,mgCounter)
    f.write('Count-Min: '+str(ObservedError)+'\n')

with open(Q4result_Rad_Path+dataName,'a') as f:
    for i in range(len(MODList)): #
        ObservedError = evaluate_rad_sum_counter(MODList[i],rad3000List,mgCounter)
        f.write(str(h1h2List[i])+' : '+str(ObservedError)+'\n')

    ObservedError = evaluate_rad_sum_counter(cS,rad3000List,mgCounter)
    f.write('Count-Min: '+str(ObservedError)+'\n')
