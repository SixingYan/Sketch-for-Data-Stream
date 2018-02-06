'''
exp_f_cg
4 part 
'''
import copy
import random
'''
import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment")
import sys; sys.path.append("..")
import lib.fMODsketch as fMODsketch
import lib.faCounter as faCounter
import lib.mSketch2D as mSketch2D
from lib.diyTool import evaluate_rad_sum_counter, evaluate_rad_sum,getRadList
'''
import mSketch2D
import fMODsketch
import faCounter
from diyTool import evaluate_rad_sum_counter, evaluate_rad_sum,getRadList

num1 = 0
num2 = 10
dataName = 'tr_fre_2' #'sanus_fre_2'#'sanus_fre_4ij'# #'tweet'
maxNodeID = 700000 #
maxIDList = [maxNodeID,maxNodeID,maxNodeID,maxNodeID]
h = 2000
H = 2000 * 2000
increase = 200
w = 13
hw = 4;lw = 9
winSize = 160

homePath = '/data1/Sixing/expdata/'# use '/' as ending
#homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment/result/'# use '/' as ending
Q4result_Top_Path = homePath+'Q4_Top_symCG_'+str(h)+'_'
Q4result_Rad_Path = homePath+'Q4_Rad_symCG_'+str(h)+'_'
#streamPath = '/data1/Sixing/stream dataset/tr_fre_4ij' # process stream sanus_fre_4ij
streamPath = '/data1/Sixing/stream dataset/sanus_fre_2' # process stream
#streamPath = 'D:/google desk PC/sanus_fre_2'

print('build......')
print('cs')
cS = copy.deepcopy(mSketch2D.mSketch2D(maxIDList,[H],w,pow(H,1/4),[[0,1,2,3]],4))
cS.buildSketch()
print('gm')
gM = copy.deepcopy(mSketch2D.mSketch2D(maxIDList,[pow(H,1/4) for _ in range(4)],w,pow(H,1/4),[[0],[1],[2],[3]],4))
gM.buildSketch()
print('csF')
cSF = copy.deepcopy(fMODsketch.fMODsketch(maxIDList,[H],w,hw,lw,[[0,1,2,3]]))
cSF.buildSketch()
print('gmF')
gMF = copy.deepcopy(fMODsketch.fMODsketch(maxIDList,[pow(H,1/4) for _ in range(4)],w,hw,lw,[[0],[1],[2],[3]]))
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
        if random.random()> 0.5:
            continue
        countNum += 1
        if countNum > 100000000:
            break
        flag = 0
        parts = line.split(' ')
        s1 = int(parts[0]);s2 = int(parts[1]);
        t1 = int(parts[2]);t2 = int(parts[3]);
        edge = (s1,s2,t1,t2)
        freq = float(parts[4])
        mgCounter.update(edge, freq)
        if mgCounter.query(edge):
            flag = 1

        if random.random()< 0.3:
            radPool.append([edge,freq])

        '''
        if len(top300List)>300:
            minV = min(top300List, key=lambda x: x[1])
            if freq>minV[1]:
                indx = top300List.index(minV);top300List[indx] = [edge,freq]
        else:
            top300List.append([edge,freq])
        '''
        cS.update(edge,freq)
        cSF.update(flag, edge,freq)
        gM.update(edge,freq)
        gMF.update(flag,edge,freq)

print('getting random')
rad3000List = getRadList(3000,radPool)
del radPool # clean

print('evaluate....')
with open(Q4result_Rad_Path+dataName+'.txt','a') as f:
    '''
    for i in range(len(MODList)): #
        ObservedError = evaluate_rad_sum_counter(MODList[i],rad3000List,mgCounter)
        f.write(str(h1h2List[i])+' : '+str(ObservedError)+'\n')
    '''
    print('CS')
    ObservedError = evaluate_rad_sum(cS,rad3000List)
    f.write('CS: '+str(ObservedError)+'\n')
    
    print('GM')
    ObservedError = evaluate_rad_sum(gM,rad3000List)
    f.write('GM: '+str(ObservedError)+'\n')
    
    print('CSF')
    ObservedError = evaluate_rad_sum_counter(cSF,rad3000List,mgCounter)
    f.write('CSF: '+str(ObservedError)+'\n')
    
    print('GMF')
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