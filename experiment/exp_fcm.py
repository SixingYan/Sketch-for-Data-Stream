"""
1. filter: store high freq. edge  
    @ store
    @ update

2. sketch update
    @ if high-freq. or not 
    @ offset/gap/# to update the sketch 
"""

sgStrList = [
'3C0S2C1','3C0S2S1','3C1C0S2',
'3C1S2C0','3C1S2S0','3C2C0S1',
'3C2C1C0','3C2C1S0','3C2S1C0',
'3C2S1S0','3S2C0S1','3S2C1C0',
'3S2C1S0','3S2S1C0','3S2S1S0',
]

from diyTool import getPathDict, getStrategy

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

def evaluate_top_sum(sketch,topList):
    totalLoss1 = 0;totalFreq1 = 0
    for parts in topList:
        s=parts[0]; t=parts[1];freq = parts[2]
        estiValue = sketch.edge_frequency_query((s,t))
        totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
    ObservedError = totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError))
    return ObservedError

streamPath = ''

N = 4
maxIDList = [255 for _ in range(N)]
h = 50
w = 13
hw = 4
lw = 9
winSize = 10000

# preparing
sghList = getMODlist
MODList = []

for sh in sghList:
    mod = copy.deepcopy(fMODsketch.fMODsketch(maxIDList,sh[1],w,hw,lw,sh[0]))
    MODList.append(mod)

mgCounter = faCounter.faCounter(winSize)

# streaming 
with open() as f:
    edge, freq
    flag = 0
    if mgCounter.query(item):
        flag = 1
    for i in range(len(MODList)):
        MODList[i].update(flag, edge, freq)


'''


# querying
    if edge in 
    MOD.query(flag, edge)
#
'''