# -*- coding: utf-8 -*-
"""
    Test Q0, the Eq(2) 
"""

"""
Experiment
    foreach Epsilon [1,10]
        foreach dataset (8)
            foreach h {300,500,1000,2000}, w {10,15}
                foreach skech {cM,gM}
                    repeat 10 times 
                        SKETCHstd: STD of sketch
                        SKETCHmean: MEAN of sketch
                        non-over: if estimated-average < Epsilong * SKETCHstd
                        ratio of non-over/total
                    get MEANratio & STDratio of these 10 ratios
            }

data format

dataset={
    'dataset':,
    'h':,
    'sketch':,
    'SKETCHmean',
    'SKETCHstd':.
    }

sketch={
     'Epsilon':,
     'dataset':,
     'h':,
     'sketch':,
     'MEANratio':,
     'STDratio':.
    }
"""
#===================  Import ->
# system
import sys; sys.path.append("..")
from copy import deepcopy
import random
import numpy as np
import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment")
# DIY
import lib.diyTool
#===================  <- Import

#===================  path area ->
homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/'# use '/' as ending

Q0result_Sketch_CS_Path = homePath+'experiment/result/Q0_sketchResultData1'
Q0result_Dataset_CS_Path = homePath+'experiment/result/Q0_datasetResultData1'
Q0result_Sketch_GM_Path = homePath+'experiment/result/Q0_sketchResultData2'
Q0result_Dataset_GM_Path = homePath+'experiment/result/Q0_datasetResultData2'
#===================  <- path area

#================  parameter ->
wSet = [10,15]
hSet = [300,500,1000]
Epsilon = [i+1 for i in range(10)]
dataset = [  #存文件名, 最大值, item数量, 数据集名称
    #['D:/google desk PC/graph_freq_comp18.txt',66666666,2,'comp18']
    ['D:/google desk PC/ip_graph_refined',4213084,2,'ip'],
    ['D:/google desk PC/graph_freq_comp18.txt',338239,2,'comp18'],
    ['D:/google desk PC/graph_freq_comp14.txt',7904564,2,'comp14']
]
repeatNumber = 10 # repeat times
#================ <- parameter


'''
直接random放入，别受极值影响
'''

def combine(edge, N):
    combinedValue = ''
    for item in edge:
        if len(str(item)) < len(str(N)):
            num = int(len(str(N))/2)-len(str(item))
            newItem = '0' * num + str(item)
            combinedValue += newItem
        else:
            combinedValue += str(item)

    return int(combinedValue)

def csHash(edge, P, h, w, mask):
    # combine
    # return hash value
    hashValue = combine(edge, P) # use P replace N
    H = h**len(edge)
    hvList = []
    for i in range(w):
        a, b = mask[i][0], mask[i][1]
        hvList.append((hashValue * a + b) % P % H)
    return hvList

def gmHash(edge, P, h, w, mask):
    hvList = []
    for k in range(w):
        a, b = mask[k][0], mask[k][1]
        totalI = 0
        for i in range(len(edge)):
            # if i=0, edge(t1,t2), then h**(2-1-0) = h
            totalI += ((a*edge[i]+b)%P%h)*(h**(len(edge)-1-i))
        hvList.append(totalI)
    return hvList

def updateSketch(sketch, hashF, edge, P, freq, w, mask):
    #
    hvList = hashF(edge, P, h, w, mask)
    for k in range(w):
        sketch[k][hvList[k]] += freq


sketchResultData1 = [] # [{},{},{},...]
datasetResultData1 = []

sketchResultData2 = [] # [{},{},{},...]
datasetResultData2 = []

# change sigma
for w in wSet:
    print('==now w is: '+str(w))
    print()
    for h in hSet:
        print('====now h is: '+str(h))
        print()
        for ds in dataset: # 'ds' is the list [file name, N, itemNum, datasetName] of one data set
            print('========now ds is: '+ds[3])
            print()
            ratioListDict1 = []
            datasetDict1 = {'w':w,'h':h,'sketch':'cs','dataset':ds[3],'SKETCHmean':0,'SKETCHstd':0}
            sketchDict1 = {'w':w,'h':h,'sketch':'cs','dataset':ds[3],'MEANratio':[],'STDratio':[]}
            stdSketchList1 = []
            meanSketchList1 = []

            ratioListDict2 = []
            datasetDict2 = {'w':w,'h':h,'sketch':'gm','dataset':ds[3],'SKETCHmean':0,'SKETCHstd':0}
            sketchDict2 = {'w':w,'h':h,'sketch':'gm','dataset':ds[3],'MEANratio':[],'STDratio':[]}
            stdSketchList2 = []
            meanSketchList2 = []

            for repeat in range(repeatNumber):
                print('============repeat: '+str(repeat))
                # setup sketch
                sketch = [[0 for _ in range(h**ds[2])] for _ in range(w)]
                cSketch = deepcopy(sketch)
                gMatrix = deepcopy(sketch)
                cN = int(str(ds[1]) * ds[2])
                gN = ds[1]
                mask_c = [diyTool.getTwoRandomNum(cN) for _ in range(w)]
                mask_g = [diyTool.getTwoRandomNum(gN) for _ in range(w)]
                print('============start stream')
                # make a stream
                countNum = 0
                with open(ds[0], 'r') as f:
                    for line in f:
                        if not len(line) > 0:
                            continue
                        if random.randint(0,100)>70: # random select
                            continue
                        
                        countNum += 1
                        if countNum % 1000000 == 0:
                            print('================now is '+str(countNum))
                        parts = line.strip().split(' ')
                        edge = parts[:len(parts)-1]
                        for num in range(len(edge)):
                            edge[num] = int(edge[num])
                        freq = int(float(parts[len(parts)-1]))

                        # random select to put in
                        updateSketch(cSketch,csHash,edge,cN,freq,w,mask_c)
                        updateSketch(gMatrix,gmHash,edge,gN,freq,w,mask_g)
                print('============start checking cSketch')
                # cSketch ============================
                meanSketch = np.mean(cSketch[0])
                totalSTD = 0
                for k in range(w):
                    totalSTD += np.std(cSketch[k])
                stdSketch = totalSTD/w 
                
                stdSketchList1.append(stdSketch)
                meanSketchList1.append(meanSketch)
                
                ratioList = []
                for e in Epsilon:
                    tNum = 0
                    for k in range(w):
                        totalNum = 0
                        for j in range(h**ds[2]):
                            if (cSketch[k][j]-meanSketch) < (stdSketch * e):
                                totalNum += 1
                        tNum += totalNum

                    ratioList.append(tNum/w/h**ds[2])
                ratioListDict1.append(ratioList)
                print('============start checking gMatrix')
                # gMatrix ============================
                meanSketch = np.mean(gMatrix[0])
                totalSTD = 0
                for k in range(w):
                    totalSTD += np.std(gMatrix[k])
                stdSketch = totalSTD/w 
                
                stdSketchList2.append(stdSketch)
                meanSketchList2.append(meanSketch)
                
                ratioList = []
                for e in Epsilon:
                    tNum = 0
                    for k in range(w):
                        totalNum = 0
                        for j in range(h**ds[2]):
                            if (gMatrix[k][j]-meanSketch) < (stdSketch * e):
                                totalNum += 1
                        tNum += totalNum

                    ratioList.append(tNum/w/h**ds[2])
                ratioListDict2.append(ratioList)
                del sketch; del gMatrix; del cSketch;

            print('========get STD cSketch')
            # cSketch ============================
            datasetDict1['SKETCHstd'] = sum(stdSketchList1)/(repeatNumber*w)  #ERROR!!!!!!!! sum(stdSketchList1)/(repeatNumber)
            datasetDict1['SKETCHmean'] = sum(meanSketchList1)/(repeatNumber*w) #ERROR!!!!!!!! sum(stdSketchList1)/(repeatNumber)

            meanList = []
            stdList = []
            for j in range(len(Epsilon)):
                totalE = []
                for repeat in range(repeatNumber):
                    totalE.append(ratioListDict1[repeat][j])
                meanList.append(np.mean(totalE))
                stdList.append(np.std(totalE))

            sketchDict1['MEANratio'] = meanList
            sketchDict1['STDratio'] = stdList
            
            datasetResultData1.append(datasetDict1)
            sketchResultData1.append(sketchDict1)

            print('========get STD gMatrix')
            # gMatrix ============================
            datasetDict2['SKETCHstd'] = sum(stdSketchList2)/(repeatNumber*w) #ERROR!!!!!!!! sum(stdSketchList1)/(repeatNumber)
            datasetDict2['SKETCHmean'] = sum(meanSketchList2)/(repeatNumber*w) #ERROR!!!!!!!! sum(stdSketchList1)/(repeatNumber)

            meanList = []
            stdList = []
            for j in range(len(Epsilon)):
                totalE = []
                for repeat in range(repeatNumber):
                    totalE.append(ratioListDict2[repeat][j])
                meanList.append(np.mean(totalE))
                stdList.append(np.std(totalE))

            sketchDict2['MEANratio'] = meanList
            sketchDict2['STDratio'] = stdList
            
            datasetResultData2.append(datasetDict2)
            sketchResultData2.append(sketchDict2)

            print('========saving')
            # saving .......
            diyTool.savePickle(Q0result_Dataset_CS_Path,datasetResultData1)
            diyTool.savePickle(Q0result_Sketch_CS_Path,sketchDict1)
            diyTool.savePickle(Q0result_Dataset_GM_Path,datasetResultData2)
            diyTool.savePickle(Q0result_Sketch_GM_Path,sketchDict2)
            
            print('^^^^^^^^^^^datasetDict1^^^^^^^^^^^')
            print(datasetDict1)
            print()
            print('^^^^^^^^^^^sketchDict1^^^^^^^^^^^')
            print(sketchDict1)
            print()
            print('^^^^^^^^^^^datasetDict2^^^^^^^^^^^')
            print(datasetDict2)
            print()
            print('^^^^^^^^^^^sketchDict2^^^^^^^^^^^')
            print(sketchDict2)
            print()
            print()




