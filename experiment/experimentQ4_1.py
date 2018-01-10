

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
    ['D:/google desk PC/graph_freq_comp18.txt',338239,2,'comp18', 0.80],
    ['D:/google desk PC/graph_freq_comp16.txt',1391333,2,'comp16', 0.80],
    ['D:/google desk PC/graph_freq_comp14.txt',7904564,2,'comp14', 0.60],
    ['D:/google desk PC/ip_graph_refined',4213084,2,'ip', 0.70],
    ['D:/google desk PC/tweet_stream_hashed_refined',17813281,2,'tweet', 0.50],  #here
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp12.txt',338239,2,'comp18', 90],
    ['D:/google desk PC/graph_freq_comp10.txt',1372146644,2,'comp1', 0.03]
]
repeatNumber = 10 #repeat times
datasetRad = []
datasetTop = []
#================ <- parameter

#===================  path area ->

homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment/result/'# use '/' as ending
Q4result_ResultTop_Path = homePath+'Q4_ResultTop'
Q4result_ResultRad_Path = homePath+'Q4_ResultRad'
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

def getValue(twoDlist):
    # work for all the sketch
    result = [] # result = [100]
    for i in range(num2-num1):
        valueList = []
        for repeat in range(repeatNumber):
            valueList.append(twoDlist[repeat][i])
        result.append(np.mean(valueList))
    return result

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
    #top = [100,500,1000,2000,5000] rand=[500,1000,2000,5000,10000]
    oeListTop = [[[] for _  in range(3) ] for _ in range(5)]
    oeListRad = [[[] for _  in range(3) ] for _ in range(5)]
    '''
    oeListTop100Dict=[[] for _ in range(3)];  oeListRad100Dict=[[] for _ in range(3)]
    oeListTop500Dict=[[] for _ in range(3)];  oeListRad500Dict=[[] for _ in range(3)]
    oeListTop1000Dict=[[] for _ in range(3)]; oeListRad1000Dict=[[] for _ in range(3)]'''
    # three types of oe evaluation mean/medium/sum, 100 sketches  oeListTop100Dict = [3][100]
    #for repeat in range(repeatNumber):
    #print('============repeat: '+str(repeat))
    rad1000List = [];top1000List = []
    countNum = 0
    h1h2List = getH1H2(num1,num2,h)
    sketchList = []
    for i in range(len(h1h2List)):
        h1,h2 = h1h2List[i]
            #print('for %d, h1 is %d   h2 is %d'%(i,h1,h2))
        hS = copy.deepcopy(hSketch.sketch(w,h1,h2,ds[1]))
        sketchList.append(hS)
    radPool = []
    print('========start stream')# start stream
    with open(ds[0],'r') as f:
        for line in f:
            line = line.strip()
            if not len(line)>0:
                    continue
                countNum += 1
                if countNum % 1000000 == 0:
                    print('now is '+str(countNum))
                parts = line.split(' ')
                s = int(parts[0])
                t = int(parts[1])
                freq = int(float(parts[2]))

                if random.randint(0,10000)>10000 * ds[4]:
                    continue

                # get rad and top
                if random.randint(0,10000)<10000* ds[4] * 0.1:
                    radPool.append([s,t,freq])
                
                if len(top1000List)>1000:
                    minV = min(top1000List, key=lambda x: x[2])
                    if freq>minV[2]:
                        indx = top1000List.index(minV);top1000List[indx] = [s,t,freq]
                else:
                    top1000List.append([s,t,freq])

                # update 
                for i in range(len(sketchList)):
                    sketchList[i].update((s,t),freq)

        print('========evaluation')# evaluation
        top1000List.sort(reverse = False)
        top100List = top1000List[:100]
        top500List = top1000List[:500]
        rad100List = getRadList(100,radPool)
        rad500List = getRadList(500,radPool)
        rad1000List = getRadList(1000,radPool)

        oeListTop100=[[] for _ in range(3)];oeListRad100=[[] for _ in range(3)] # three types of oe evaluation mean/medium/sum
        oeListTop500=[[] for _ in range(3)];oeListRad500=[[] for _ in range(3)]
        oeListTop1000=[[] for _ in range(3)];oeListRad1000=[[] for _ in range(3)]

        for i in range(len(sketchList)):
            print('********for %d'%i)
            print('----------Top')# top
            ObservedError = evaluate_top_mean(sketchList[i],top100List);oeListTop100[0].append(ObservedError)
            ObservedError = evaluate_top_mean(sketchList[i],top500List);oeListTop500[0].append(ObservedError)
            ObservedError = evaluate_top_mean(sketchList[i],top1000List);oeListTop1000[0].append(ObservedError)
            print()
            ObservedError = evaluate_top_medium(sketchList[i],top100List);oeListTop100[1].append(ObservedError)
            ObservedError = evaluate_top_medium(sketchList[i],top500List);oeListTop500[1].append(ObservedError)
            ObservedError = evaluate_top_medium(sketchList[i],top1000List);oeListTop1000[1].append(ObservedError)
            print()
            ObservedError = evaluate_top_sum(sketchList[i],top100List);oeListTop100[2].append(ObservedError)
            ObservedError = evaluate_top_sum(sketchList[i],top500List);oeListTop500[2].append(ObservedError)
            ObservedError = evaluate_top_sum(sketchList[i],top1000List);oeListTop1000[2].append(ObservedError)
            print()

            print('----------random')# random
            ObservedError = evaluate_rad_mean(sketchList[i],rad100List);oeListRad100[0].append(ObservedError)
            ObservedError = evaluate_rad_mean(sketchList[i],rad500List);oeListRad500[0].append(ObservedError)
            ObservedError = evaluate_rad_mean(sketchList[i],rad1000List);oeListRad1000[0].append(ObservedError)
            print()
            ObservedError = evaluate_rad_medium(sketchList[i],rad100List);oeListRad100[1].append(ObservedError)
            ObservedError = evaluate_rad_medium(sketchList[i],rad500List);oeListRad500[1].append(ObservedError)
            ObservedError = evaluate_rad_medium(sketchList[i],rad1000List);oeListRad1000[1].append(ObservedError)
            print()
            ObservedError = evaluate_rad_sum(sketchList[i],rad100List);oeListRad100[2].append(ObservedError)
            ObservedError = evaluate_rad_sum(sketchList[i],rad500List);oeListRad500[2].append(ObservedError)
            ObservedError = evaluate_rad_sum(sketchList[i],rad1000List);oeListRad1000[2].append(ObservedError)
            print()

        for i in range(3):
            oeListTop100Dict[i].append(oeListTop100[i]);oeListRad100Dict[i].append(oeListRad100[i])
            oeListTop500Dict[i].append(oeListTop500[i]);oeListRad500Dict[i].append(oeListRad500[i])
            oeListTop1000Dict[i].append(oeListTop1000[i]);oeListRad1000Dict[i].append(oeListRad1000[i])

        # delete
        del sketchList; del radPool
    
    print('========getting oe')# evaluation
    # getting
    oeRad100 = [[] for _ in range(3)];oeTop100 = [[] for _ in range(3)]
    oeRad500 = [[] for _ in range(3)];oeTop500 = [[] for _ in range(3)]
    oeRad1000 = [[] for _ in range(3)];oeTop1000 = [[] for _ in range(3)]
    # three type evaluation mean/medium/sum 100 sketch [3][100]
    for i in range(3):
        oeRad100[i] = getValue(oeListRad100Dict[i])
        oeTop100[i] = getValue(oeListTop100Dict[i])
        oeRad500[i] = getValue(oeListRad500Dict[i])
        oeTop500[i] = getValue(oeListTop500Dict[i])
        oeRad1000[i] = getValue(oeListRad1000Dict[i])
        oeTop1000[i] = getValue(oeListTop1000Dict[i])

    temDict = {'w':w,'h':h,'dataset':ds[3],'type':'Rad','100':oeRad100,'500':oeRad500,'1000':oeRad1000}
    datasetRad.append(temDict)
    temDict = {'w':w,'h':h,'dataset':ds[3],'type':'Top','100':oeTop100,'500':oeTop500,'1000':oeTop1000}
    datasetTop.append(temDict)

    print('========saving') # saving .......
    diyTool.savePickle(Q4result_ResultRad_Path,datasetRad)
    diyTool.savePickle(Q4result_ResultTop_Path,datasetTop)
