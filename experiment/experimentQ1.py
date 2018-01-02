
""" 
- GOAL
get stream| std, mean
get sample stream| std, mean
get sketch| std, mean
get sample sketch| std, mean
get ratio| std, mean
get sample ratio| std, mean
"""

#===================  Import ->
# system
import sys; sys.path.append("..")
from copy import deepcopy
import random
import numpy as np
import os; os.chdir("D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment")
# DIY
import diyTool
#===================  <- Import

#===================  path area ->
homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/'# use '/' as ending

Q1result_Stream_Path = homePath+'experiment/result/Q1_streamResultData'
Q1result_Dataset_Path = homePath+'experiment/result/Q1_datasetResultData'
Q1result_Dataset_set_Path = homePath+'experiment/result/Q1_datasetResultData_set'
Q1result_Sketch_Path = homePath+'experiment/result/Q1_sketchResultData'
Q1result_Sketch_set_Path = homePath+'experiment/result/Q1_sketchResultData_set'
#===================  <- path area

#================  parameter ->
basicPercent = 0.2
wSet = [10,15]
hSet = [300,500,1000]
Epsilon = [1, 3, 5, 10]
dataset = [  #存文件名, 最大值, item数量, 数据集名称, 实验用的数据大小（%）
    #['D:/google desk PC/ip_graph_refined',4213084,2,'ip', 80],
    ['D:/google desk PC/graph_freq_comp18.txt',338239,2,'comp18', 90]#,
    #['D:/google desk PC/graph_freq_comp14.txt',7904564,2,'comp14', 70],
    #[],
    #[]
]
percent = [0.001, 0.003, 0.005, 0.01, 0.03, 0.05, 0.1, 0.2]
percentNum = len(percent)
repeatNumber = 10 # repeat times
#================ <- parameter

#多少 percent 正确率还能保障
#


#
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

def checkSketchRatio(sketch,edgeNum):
    #
    # get std and mean
    w = len(sketch)
    meanSketch = np.mean(sketch[0])
    totalSTD = 0
    for k in range(w):
        totalSTD += np.std(sketch[k])
    stdSketch = totalSTD/w 
    # get ratio by std and mean
    ratioList = []
    for e in Epsilon:
        tNum = 0
        for k in range(w):
            totalNum = 0
            for j in range(h**edgeNum):
                if (sketch[k][j]-meanSketch) < (stdSketch * e):
                    totalNum += 1
            tNum += totalNum
        ratioList.append(tNum/w/h**edgeNum)
    return stdSketch,meanSketch,ratioList

def getSketchRatio(ratioListDict):
    #
    meanList = []
    stdList = []
    for j in range(len(Epsilon)):
        totalE = []
        for repeat in range(repeatNumber):
            totalE.append(ratioListDict[repeat][j])
        meanList.append(np.mean(totalE))
        stdList.append(np.std(totalE))
    return meanList,stdList

#
streamResultData = []

sketchResultData = [] # [{},{},{},...]
datasetResultData = []

sketchResultData_set = [] # [{},{},{},...]
datasetResultData_set = []

flag = True

for w in wSet:
    print('==now w is: '+str(w))
    print()
    for h in hSet:
        print('====now h is: '+str(h))
        print()
        for ds in dataset: # 'ds' is the list [file name, N, itemNum, datasetName] of one data set
            print('========now ds is: '+ds[3])
            print()
            if True: # just incident error
                # n*2 sketches
                if flag:
                    streamList = {'mean':[[] for _ in range(repeatNumber)],'std':[[] for _ in range(repeatNumber)]}
                    streamDict = {'basicPercent':0,'percent':0,'dataset':ds[3],'mean':0,'std':0} 

                stdCSketch = []
                meanCSketch = []
                ratioListDict_cSketch = []
                datasetDict_cSketch = {'w':w,'h':h,'sketch':'cs','dataset':ds[3],'SKETCHmean':0,'SKETCHstd':0}
                sketchDict_cSketch = {'w':w,'h':h,'sketch':'cs','dataset':ds[3],'MEANratio':[0 for _ in range(len(Epsilon))],'STDratio':[0 for _ in range(len(Epsilon))]}

                stdGMatrix = []
                meanGMatrix = []
                ratioListDict_gMatrix = []
                datasetDict_gMatrix = {'w':w,'h':h,'sketch':'gm','dataset':ds[3],'SKETCHmean':0,'SKETCHstd':0}
                sketchDict_gMatrix = {'w':w,'h':h,'sketch':'gm','dataset':ds[3],'MEANratio':[0 for _ in range(len(Epsilon))],'STDratio':[0 for _ in range(len(Epsilon))]}

                stdCSketchList = [[] for _ in range(percentNum)]
                meanCSketchList = [[] for _ in range(percentNum)]
                ratioListDict_cSketchSet = [[] for _ in range(percentNum)]
                datasetDict_cSketchSet = {'w':w,'h':h,'sketch':'cs','dataset':ds[3],'percent':[],'SKETCHmean':[0 for _ in range(percentNum)],'SKETCHstd':[0 for _ in range(percentNum)]}
                sketchDict_cSketchSet = {'w':w,'h':h,'sketch':'cs','dataset':ds[3],'percent':[],'MEANratio':[[0 for _ in range(len(Epsilon))] for _ in range(percentNum)],'STDratio':[[0 for _ in range(len(Epsilon))] for _ in range(percentNum)]}

                stdGMatrixList = [[] for _ in range(percentNum)]
                meanGMatrixList = [[] for _ in range(percentNum)]
                ratioListDict_gMatrixSet = [[] for _ in range(percentNum)]
                datasetDict_gMatrixSet = {'w':w,'h':h,'sketch':'cs','dataset':ds[3],'percent':[],'SKETCHmean':[0 for _ in range(percentNum)],'SKETCHstd':[0 for _ in range(percentNum)]}
                sketchDict_gMatrixSet = {'w':w,'h':h,'sketch':'cs','dataset':ds[3],'percent':0,'MEANratio':[[0 for _ in range(len(Epsilon))] for _ in range(percentNum)],'STDratio':[[0 for _ in range(len(Epsilon))] for _ in range(percentNum)]}

                for repeat in range(repeatNumber):
                    print('============repeat: '+str(repeat))
                    stream = []
                    streamSample = [[] for _ in range(percentNum)]
                    sketch = [[0 for _ in range(h**ds[2])] for _ in range(w)]
                    cSketch = deepcopy(sketch)
                    gMatrix = deepcopy(sketch)
                    cSketchSet = [deepcopy(sketch) for _ in range(percentNum)]
                    gMatrixSet = [deepcopy(sketch) for _ in range(percentNum)]
                    cN = int(str(ds[1]) * ds[2])
                    gN = ds[1]
                    mask_c = [diyTool.getTwoRandomNum(cN) for _ in range(w)]
                    mask_g = [diyTool.getTwoRandomNum(gN) for _ in range(w)]
                    # start stream
                    print('============start stream')
                    with open(ds[0], 'r') as f:
                        for line in f:
                            if not len(line) > 0:
                                continue
                            # prepare edge
                            parts = line.strip().split(' ')
                            edge = parts[:len(parts)-1]
                            for num in range(len(edge)):
                                edge[num] = int(edge[num])
                            freq = int(float(parts[len(parts)-1]))

                            # select edge
                            randNum = random.randint(0,1000)
                            if randNum > 1000 * basicPercent: #temp percent, used ds[4] to replace
                                continue
                            # storing stream
                            if flag:
                                stream.append(freq)
                            # sketch storing
                            updateSketch(cSketch,csHash,edge,cN,freq,w,mask_c)
                            updateSketch(gMatrix,gmHash,edge,gN,freq,w,mask_g)

                            for i in range(percentNum):
                                per = percent[i]
                                if randNum > 1000 * basicPercent * per:
                                    continue
                                # storing stream
                                if flag:
                                    streamSample[i].append(freq)
                                # sketch storing
                                updateSketch(cSketchSet[i],csHash,edge,cN,freq,w,mask_c)
                                updateSketch(gMatrixSet[i],gmHash,edge,gN,freq,w,mask_g)

                    print('============start checking stream')
                    if flag: 
                        streamList['mean'][repeat].append(np.mean(stream))
                        streamList['std'][repeat].append(np.std(stream))
                        for i in range(percentNum):
                            streamList['mean'][repeat].append(np.mean(streamSample[i]))
                            streamList['std'][repeat].append(np.std(streamSample[i]))

                    print('============start checking cSketch')
                    # baseline cSketch
                    stdSketch,meanSketch,ratioList = checkSketchRatio(cSketch,ds[2])
                    stdCSketch.append(stdSketch)
                    meanCSketch.append(meanSketch)
                    ratioListDict_cSketch.append(ratioList)
                    # percent cSketch
                    for i in range(percentNum):
                        stdSketch,meanSketch,ratioList = checkSketchRatio(cSketchSet[i],ds[2])
                        stdCSketchList[i].append(stdSketch)
                        meanCSketchList[i].append(meanSketch)
                        ratioListDict_cSketchSet[i].append(ratioList)

                    print('============start checking gMatrix')
                    # baseline gMatrix
                    stdSketch,meanSketch,ratioList = checkSketchRatio(gMatrix,ds[2])
                    stdGMatrix.append(stdSketch)
                    meanGMatrix.append(meanSketch)
                    ratioListDict_gMatrix.append(ratioList)

                    # percent gMatrix
                    for i in range(percentNum):
                        stdSketch,meanSketch,ratioList = checkSketchRatio(gMatrixSet[i],ds[2])
                        stdGMatrixList[i].append(stdSketch)
                        meanGMatrixList[i].append(meanSketch)
                        ratioListDict_gMatrixSet[i].append(ratioList)
                    # clear memory  
                    del sketch; del cSketch; del cSketchSet; del gMatrix; del gMatrixSet; del stream; del streamSample
                    
                    
                print('============get stream result')
                if flag:
                    totalMean = []
                    totalStd = []
                    for i in range(repeatNumber):
                        totalMean.append(streamList['mean'][i][0])
                        totalStd.append(streamList['std'][i][0])
                    streamDict['basicPercent'] = basicPercent
                    streamDict['percent'] = 1
                    streamDict['mean'] = sum(totalMean)/repeatNum
                    streamDict['std'] = sum(totalStd)/repeatNum
                    streamResultData.append(streamDict) # put in

                    for j in range(percentNum):
                        totalMean = []
                        totalStd = []
                        for i in range(repeatNumber):
                            totalMean.append(streamList['mean'][i][j+1])
                            totalStd.append(streamList['std'][i][j+1])
                        streamDict['percent'] = percent[j]
                        streamDict['mean'] = sum(totalMean)/repeatNum
                        streamDict['std'] = sum(totalStd)/repeatNum
                        streamResultData.append(streamDict) # put in

                    diyTool.savePickle(Q1result_Stream_Path,streamResultData)

                print('============get cSketch result')

                # dataset
                datasetDict_cSketch['SKETCHstd'] = sum(stdCSketch)/(repeatNumber)
                datasetDict_cSketch['SKETCHmean'] = sum(meanCSketch)/(repeatNumber)

                datasetDict_cSketchSet['percent'] = deepcopy(percent)
                datasetDict_cSketchSet['SKETCHstd'] = [sum(stdCSk)/(repeatNumber) for stdCSk in stdCSketchList]
                datasetDict_cSketchSet['SKETCHmean'] = [sum(meanCSk)/(repeatNumber) for meanCSk in meanCSketchList]

                datasetResultData.append(datasetDict_cSketch) # put in
                datasetResultData_set.append(datasetDict_cSketchSet) # put in

                # sketch
                meanList,stdList = getSketchRatio(ratioListDict_cSketch)
                sketchDict_cSketch['MEANratio'] = meanList
                sketchDict_cSketch['STDratio'] = stdList
                sketchResultData.append(sketchDict_cSketch)

                for i in range(percentNum):
                    meanList,stdList = getSketchRatio(ratioListDict_cSketchSet[i])
                    sketchDict_cSketchSet['MEANratio'][i] = meanList
                    sketchDict_cSketchSet['STDratio'][i] = stdList
                sketchResultData_set.append(sketchDict_cSketchSet) # put in

                print('============get gMatrix result')
                # dataset
                datasetDict_gMatrix['SKETCHstd'] = sum(stdGMatrix)/(repeatNumber)
                datasetDict_gMatrix['SKETCHmean'] = sum(meanGMatrix)/(repeatNumber)

                datasetDict_gMatrixSet['percent'] = deepcopy(percent)
                datasetDict_gMatrixSet['SKETCHstd'] = [sum(stdGMa)/(repeatNumber) for stdGMa in stdGMatrixList]
                datasetDict_gMatrixSet['SKETCHmean'] = [sum(meanGMa)/(repeatNumber) for meanGMa in meanGMatrixList]

                datasetResultData.append(datasetDict_gMatrix) # put in
                datasetResultData_set.append(datasetDict_gMatrixSet) # put in
               
                # sketch
                meanList,stdList = getSketchRatio(ratioListDict_gMatrix)
                sketchDict_gMatrix['MEANratio'] = meanList
                sketchDict_gMatrix['STDratio'] = stdList
                sketchResultData.append(sketchDict_gMatrix) # put in

                for i in range(percentNum):
                    meanList,stdList = getSketchRatio(ratioListDict_gMatrixSet[i])
                    sketchDict_gMatrixSet['MEANratio'][i] = meanList
                    sketchDict_gMatrixSet['STDratio'][i] = stdList
                sketchResultData_set.append(sketchDict_gMatrixSet) # put in

                print('========saving') # saving .......
                diyTool.savePickle(Q1result_Dataset_Path,datasetResultData)
                diyTool.savePickle(Q1result_Dataset_set_Path,datasetResultData_set)
                diyTool.savePickle(Q1result_Sketch_Path,sketchResultData)
                diyTool.savePickle(Q1result_Sketch_set_Path,sketchResultData_set)
                
                print('^^^^^^^^^^^datasetResultData^^^^^^^^^^^')
                print(datasetResultData)
                print()
                print('^^^^^^^^^^^datasetResultData_set^^^^^^^^^^^')
                print(datasetResultData_set)
                print()
                print('^^^^^^^^^^^sketchResultData^^^^^^^^^^^')
                print(sketchResultData)
                print()
                print('^^^^^^^^^^^sketchResultData_set^^^^^^^^^^^')
                print(sketchResultData_set)
                print()
        flag = False