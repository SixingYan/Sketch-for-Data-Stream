'''

'''
import copy
import time
import mSketch2D
#import lib.mSketch as mSketch
import numpy as np 
maxIDList = [
[255255255255 for _ in range(2)],
[255255 for _ in range(4)],
[255 for _ in range(8)],
]
strList = [
[],
[],
['7S6C5S4C2C1C0S3','7C5S6C4C3S2S1C0','7C6C5S4S3C2C0S1','7S6C5C3C1S4S2S0','7C5C4S6C2S3S1C0','7S6S5S4C2S3C0S1',
 '7C6S5S4C3S2C0S1','7C6C0S5S4S3C2S1','7C5S6C3S4C1S2S0','7C4C3S6C5C2C0S1','7S6C3C1S5C0S4S2','7C6S5C3C1S4C2C0',
 '7C1S6C5S4S3S2C0','7C6S5S4C2C0S3C1','7C0S6C3C2C1S5S4','7C4C3C2S6C5C1S0','7S6C1S5C3C2C0S4','7C3C0S6C2S5C4C1','7C5C1S6S4S3S2C0',
 '7S6C5C4C1S3C0S2','7C5S6S4C3C2C0S1','7S6C3S5C2C0S4S1','7C5C3S6C0S4C2S1','7C5C4S6S3C2C1C0','7S6C3S5C1S4S2S0',
 '7S6C2S5S4C3C0S1','7C6S5C2S4S3S1C0','7C5C2C1S6C0S4S3','7C5S6C2C0S4S3C1','7C6C4S5C0S3S2S1','7S6C4S5C1C0S3S2'],
]
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
#---------------
def evaluate_top_sum(sketch,topList):
    totalLoss1 = 0;totalFreq1 = 0
    for parts in topList:
        s=parts[0]; t=parts[1];freq = parts[2]
        estiValue = sketch.edge_frequency_query((s,t))
        totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
    ObservedError = totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError))
    return ObservedError
#----------------
def getPathDict(pathStr):
    # input a string 
    pathDict = {}
    pathDict['partID'] = []
    pathDict['edgeType'] = []
    preIndex = 0
    for i in range(len(pathStr)):
        if pathStr[i] == 'S' or pathStr[i] == 'C':
            pathDict['partID'].append(int(pathStr[preIndex:i]))
            if pathStr[i] == 'S':
                pathDict['edgeType'].append(0)
            else:
                pathDict['edgeType'].append(1)
            preIndex = i + 1
    pathTem = pathStr[::-1]# reverse string
    idx = 0
    for i in range(len(pathTem)):
        if pathTem[i] == 'S' or pathTem[i] == 'C':
            idx = i
            break
    pathDict['partID'].append(int(pathStr[-idx:]))
    return pathDict   
#----------------
def getStrategy(pathDict):
    # edge=0 seperate  edge=1 combine 
    j = 0
    strategy = []#[[],...[]]
    for i in range(len(pathDict['partID'])):
        if i == len(pathDict['partID'])-1:
            continue
        if i == 0:
            strategy.append([])
            strategy[j].append(pathDict['partID'][i])
        edge = pathDict['edgeType'][i]
        if edge == 1:
            strategy[j].append(pathDict['partID'][i+1])
        else:
            strategy.append([])
            j += 1
            strategy[j].append(pathDict['partID'][i+1])
    return strategy
#-------------

def getHList(stra):
    #
    hList = []
    for i in range(len(stra)):
        l = h**len(stra[i])
        hList.append(l)
    return hList

dataset = ['tr_1', '/data1/Sixing/tr_1_4ij', '/data1/Sixing/tr_1_2', '/data1/Sixing/tr_1']

'''

stra = [[0, 1]]
hList =  [400]
maxIDList = [255255]
w = 10
h = 20
edge = [60764, 32817]
'''
hSet = [1000,100,10]
h = 10
partNum = [2,4,8]
#hListM = [[],[],[4,100,50,200,25]]
hListC = [[10**6,],[10**8,],[10**8,]]
#straM = [[0,],[1,]],[(0,),(1,2),(3,)],[(1,),(2,3),(4,7),(0,5),(6,)]
straC = [[0,1,]],[(0,1,2,3)],[(0,1,2,3,4,5,6,7)],
partList = [[0,1],[0,1,2,3],[0,1,2,3,4,5,6,7]]
w = 10

strList = []

for i in range(len(partNum)):
    sketchList = []
    if not i == 2: # only for 8-parts
        continue
    hListG = [hSet[i] for _ in range(partNum[i])]
    straG = [[j,] for j in range(partNum[i])]
    #mS = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListM[i],w,hSet[i],straM[i],partNum[i]));mS.buildSketch()
    mC = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListC[i],w,hSet[i],straC[i],partNum[i]));mC.buildSketch()
    mG = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListG,w,hSet[i],straG,partNum[i]));mG.buildSketch()
    
    for path in strList[i]:
        d = getPathDict(path)
        stra = getStrategy(d)
        hListM = getHList(stra)
        mS = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListM,w,hSet[i],stra,partNum[i]));mS.buildSketch()
        sketchList.append(mS)

    with open(dataset[i+1],'r') as f:
        # input structure of sketch 
        # open a sample of stream partList, e.g., 5,6,7
        pool = []
        print('getting stream ==========> ')
        for line in f:
            line = line.strip()
            if not len(line) > 0:
                continue
            if random.random()>0.3:
                continue
            countNum += 1
            if countNum > 2000:
                break
            parts = line.split(' ')
            #print('line '+line)
            # should be multi-part
            if partNum[i]> 5: # for 8 parts
                try:
                    sNode = [int(k) for k in parts[0].split('.')];
                    tNode = [int(k) for k in parts[1].split('.')];
                except:
                    continue
                fre = float(parts[2])
                nodeList = sNode + tNode
                #print('8 parts')
            elif partNum[i]> 3 :# for 4 parts
                nodeList = [int(k) for k in parts[:4]]
                #print('4 parts')
            else:
                nodeList = [int(k) for k in parts[:2]]

            fre = float(parts[-1])
            edge = []

            if len(top5000List)>2000:
                minV = min(top5000List, key=lambda x: x[2])
                if freq>minV[2]:
                    indx = top5000List.index(minV);top5000List[indx] = [edge,freq]
            else:
                top5000List.append([edge,freq])

            if random.random()<0.2:
                radPool.append([edge,freq])

            for pID in partList[i]:
                edge.append(nodeList[pID])

            for num in sketchList:
                sketchList[num].update(edge,fre)

            mC.update(edge,fre)

            mG.update(edge,fre)

    print('========evaluation')# evaluation
    topList = []; radList = []
    top5000List.sort(key= lambda d : d[2], reverse = True)
    topList = top5000List[:1000]
    radList = getRadList(1000,radPool)
    del radPool

    with open('/data1/Sixing/expdata/txt_'+dataset[0]+'_'+str(partNum[i]),'a') as f:
        f.write('\n MG')
        valueList = []
        for num in range(len(sketchList)):
            value = evaluate_top_sum(sketchList[i],topList)
            valueList.append(value)
        mV = min(valueList)
        idx = valueList.index(mV)
        f.write('top stra '+str(sketchList[idx].sg))
        f.write('top: '+str(mV))
        f.write('\n')

        valueList = []
        for num in range(len(sketchList)):
            value = evaluate_rad_sum(sketchList[i],radList)
            valueList.append(value)
        mV = min(valueList)
        idx = valueList.index(mV)
        f.write('rad stra '+str(sketchList[idx].sg))
        f.write('rad: '+str(mV))
        f.write('\n')

        f.write('\n MC')
        value = evaluate_top_sum(mC,topList)
        f.write('top: '+str(mV))
        value = evaluate_rad_sum(mC,radList)
        f.write('rad: '+str(mV))
        f.write('\n')

        f.write('\n MG')
        value = evaluate_top_sum(mG,topList)
        f.write('top: '+str(mV))
        value = evaluate_rad_sum(mG,radList)
        f.write('rad: '+str(mV))
        f.write('\n')
