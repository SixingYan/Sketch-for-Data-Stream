"""
    Test Q4, the Eq( ) 
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
import diyTool
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
dataset = [ 
    #['D:/google desk PC/ip_graph_refined',4213084,2,'ip', 80],
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp18.txt',338239,2,'comp18', 0.90],
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp16.txt',1391333,2,'comp16', 0.90],
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp14.txt',7904564,2,'comp14', 0.70],
    ['D:/google desk PC/ip_graph_refined',4213084,2,'ip', 0.90],
    ['C:/Users/alfonso.yan/Documents/tweet_stream_hashed_refined',17813281,2,'tweet', 0.60],
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp12.txt',338239,2,'comp18', 90],
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp10.txt',1372146644,2,'comp1', 0.05]
]

repeatNumber = 10 # repeat times
#================ <- parameter





#================
# get range of sqrt beta


AlphaList = []
for ds in dataset:
    meanList = []
    mediumList = []

    for repeat in range(repeatNumber):
        dictKeyList = set([])
        nodeDict = {} #{}
        with open(,) as f:
            # out degree
            if s in dictKeyList:
                nodeDict[s][1] += freq
            else:
                nodeDict[s] = [0,0]
                nodeDict[s][1] += freq
                dictKeyList.add(s)
            # in degree
            if t in dictKeyList:
                nodeDict[t][0] += freq
            else:
                nodeDict[t] = [0,0]
                nodeDict[t][0] += freq
                dictKeyList.add(t)
        outList = []
        inList = []
        for key in list(dictKeyList):
            inList.append(nodeDict[key][0])
            outList.append(nodeDict[key][1])

        inList.sort(); outList.sort()

        meanOut = np.mean(outList)
        mediumOut = (outList[int(len(outList)/2)] + outList[~int(len(outList)/2)])/ 2
        meanIn = np.mean(inList)
        mediumIn = (inList[int(len(inList)/2)] + inList[~int(len(inList)/2)])/ 2

        alphaMEAN = meanOut/meanIn
        alphaMEDIUM = mediumOut/mediumIn
        meanList.append(alphaMEAN)
        mediumList.append(alphaMEDIUM)


    np.mean(meanList)
    for repeat in range(repeatNumber):
        [repeat]

    (ll,uu)
    #get h1 range

    #取最好的那次


#get sample

repeat





#








# hash function


'''
抽取sample的大小，都抽多一些
200M
'''








def function():
    pass

def function():
    pass

def  ():
    # change sigma

    pass



def ():

    #repeat 20 time












