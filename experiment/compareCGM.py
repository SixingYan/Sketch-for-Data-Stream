
import copy
#import time
import mSketch2D
#import numpy as np 
import random
maxIDList = [
#[255255255255 for _ in range(2)],
[255255 for _ in range(4)],
[255 for _ in range(8)],
]
#print('yes')
#strList = ['7S6C5S4C2C1C0S3','7C5S6C4C3S2S1C0','7C6C5S4S3C2C0S1','7S6C5C3C1S4S2S0','7C5C4S6C2S3S1C0','7S6S5S4C2S3C0S1',
# '7S6C2S5S4C3C0S1','7C6S5C2S4S3S1C0','7C5C2C1S6C0S4S3','7C5S6C2C0S4S3C1','7C6C4S5C0S3S2S1','7S6C4S5C1C0S3S2']
#strList = ['7C6C5C4C3C2C1C0','7S6S5S4S3S2S1S0']

def getRadList(num,radPool):
    radList = [[] for i in range(5)]
    for i in range(len(radList)):
        while len(radList[i]) < num:
            tem = random.choice(radPool)
            if tem not in radList[i]:
                radList[i].append(tem)
    return radList
def evaluate_rad_sum(sketch,radList):
    #
    ObservedError = 0
    for i in range(len(radList)):
        totalLoss1 = 0;totalFreq1 = 0
        for parts in radList[i]:
            edge=parts[0]; freq = parts[1]
            estiValue = sketch.query(edge)
            totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
        ObservedError += totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError/len(radList)))
    return ObservedError/len(radList)
#---------------
def evaluate_top_sum(sketch,topList):
    totalLoss1 = 0;totalFreq1 = 0
    for parts in topList:
        edge=parts[0]; freq = parts[1]
        estiValue = sketch.query(edge)
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

dataset = ['tr_1', '/data1/Sixing/tr_1_4ij', '/data1/Sixing/tr_1_2', '/data1/Sixing/tr_1']

h = 10**7
partNum = [2,4,8]
hListC = [h]
straC = [[(0,1,2,3)],[(0,1,2,3,4,5,6,7)]]
partList = [[0,1,2,3],[0,1,2,3,4,5,6,7]]
w = 4
#strList = []
for i in range(len(partNum)):
    radPool = []
    top100List = []
    countNum = 0
    #sketchList = []
    hListG = [pow(h,1/partNum[i]) for pn in range(partNum[i])]
    straG = [[j,] for j in range(partNum[i])]
    #mS = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListM[i],w,hSet[i],straM[i],partNum[i]));mS.buildSketch()
    mC = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListC,w,pow(h,1/partNum[i]),straC[i],partNum[i]));mC.buildSketch()
    mG = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListG,w,pow(h,1/partNum[i]),straG,partNum[i]));mG.buildSketch()
    with open(dataset[i+1],'r') as f:
        # input structure of sketch 
        # open a sample of stream partList, e.g., 5,6,7
        print('getting stream ==========> ')
        for line in f.readlines():
            line = line.strip()
            if not len(line) > 0:
                continue
            if random.random()>0.3:
                continue
            countNum += 1
            if countNum > 1000000:
                break
            parts = line.split(' ')

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

            if len(top100List)>100:
                minV = min(top100List, key=lambda x: x[1])
                if fre>minV[1]:
                    indx = top100List.index(minV);top100List[indx] = [edge,fre]
            else:
                top100List.append([edge,fre])

            if random.random()<0.2:
                radPool.append([edge,fre])

            for pID in partList[i]:
                edge.append(nodeList[pID])

            #for num in sketchList:
            #    sketchList[num].update(edge,fre)

            mC.update(edge,fre)
            mG.update(edge,fre)

    print('========evaluation')# evaluation
    rad1000List = getRadList(1000,radPool)
    print('analysis')
    with open('/data1/Sixing/expdata/txt__'+dataset[0]+'_'+str(partNum[i]),'a') as f:
        print('cSketch')
        f.write('\n MC')
        value = evaluate_top_sum(mC,top100List)
        f.write('top: '+str(value)+'\n')
        value = evaluate_rad_sum(mC,rad1000List)
        f.write('rad: '+str(value)+'\n')
        f.write('\n')

        print('gMatrix')
        f.write('\n MG')
        value = evaluate_top_sum(mG,top100List)
        f.write('top: '+str(value)+'\n')
        value = evaluate_rad_sum(mG,rad1000List)
        f.write('rad: '+str(value)+'\n')
        f.write('\n')
        '''
        print('MOD')
        f.write('\n MG')
        valueList = []
        for num in range(len(sketchList)):
            value = evaluate_top_sum(sketchList[i],top100List)
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
        '''


