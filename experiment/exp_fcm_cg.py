'''
exp_f_cg
4 part 
'''
import copy
import random

import mSketch2D
import fMODsketch
import faCounter
from diyTool import evaluate_rad_sum_counter, evaluate_rad_sum

num1 = 0
num2 = 10
dataName = 'tr_fre_2'#'sanus_fre_4ij'# #'tweet'
maxNodeID = 70000 #
maxIDList = [maxNodeID,maxNodeID,maxNodeID,maxNodeID]
h = 2000
increase = 200
w = 13
hw = 4;lw = 9
winSize = 64
homePath = '/data1/Sixing/expdata/'# use '/' as ending
Q4result_Top_Path = homePath+'Q4_Top_symCG_'+str(h)+'_'
Q4result_Rad_Path = homePath+'Q4_Rad_symCG_'+str(h)+'_'
#streamPath = '/data1/Sixing/stream dataset/tr_fre_4ij' # process stream
streamPath = '/data1/Sixing/stream dataset/sanus_fre_4ij' # process stream

print('build......')
cS = copy.deepcopy(mSketch2D.mSketch2D(maxIDList,[h**2],w,pow(h,1/4),[[0,1,2,3]],4))
cS.buildSketch()

gM = copy.deepcopy(mSketch2D.mSketch2D(maxIDList,[h,h],w,pow(h,1/4),[[0],[1],[2],[3]],4))
gM.buildSketch()

cSF = copy.deepcopy(fMODsketch.fMODsketch(maxIDList,[h**2],w,hw,lw,[[0,1]]))
cSF.buildSketch()

gMF = copy.deepcopy(fMODsketch.fMODsketch(maxIDList,[h,h],w,hw,lw,[[0,1]]))
gMF.buildSketch()

mgCounter = faCounter.faCounter(winSize)

countNum = 0
# streaming 
radPool = [];top300List = []
print('start stream......')
with open(streamPath,'r') as f:
    for line in f:
        line = line.strip()
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

        cS.update(flag, (s,t),freq)
        cSF.update(flag, (s,t),freq)
        gM.update(flag, (s,t),freq)
        gMF.update(flag, (s,t),freq)

rad3000List = getRadList(3000,radPool)
del radPool # clean

with open(Q4result_Rad_Path+dataName,'a') as f:
    '''
    for i in range(len(MODList)): #
        ObservedError = evaluate_rad_sum_counter(MODList[i],rad3000List,mgCounter)
        f.write(str(h1h2List[i])+' : '+str(ObservedError)+'\n')
    '''
    ObservedError = evaluate_rad_sum(cS,rad3000List)
    f.write('CS: '+str(ObservedError)+'\n')
    ObservedError = evaluate_rad_sum(gM,rad3000List)
    f.write('GM: '+str(ObservedError)+'\n')

    ObservedError = evaluate_rad_sum_counter(cSF,rad3000List,mgCounter)
    f.write('CSF: '+str(ObservedError)+'\n')
    ObservedError = evaluate_rad_sum_counter(gMF,rad3000List,mgCounter)
    f.write('GMF: '+str(ObservedError)+'\n')

'''
print('\n evaluation......')
with open(Q4result_Top_Path+dataName,'a') as f:
    for i in range(len(MODList)): #
        ObservedError = evaluate_top_sum_counter(MODList[i],top300List,mgCounter)
        f.write(str(h1h2List[i])+' : '+str(ObservedError)+'\n')

    ObservedError = evaluate_top_sum_counter(cS,top300List,mgCounter)
    f.write('Count-Min: '+str(ObservedError)+'\n')
'''