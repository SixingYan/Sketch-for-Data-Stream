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
'''
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
'''
#samplePath = '/data1/Sixing/expdata/sample/' # train the counter
samplePath = 'F:/sample/comp18_0.05.txt'
winSize = 10000
mgCounter = faCounter.faCounter(winSize)
with open(samplePath,'r') as f:
    for line in f:
        if not len(line) > 0:
            continue
        parts = line.split(' ')
        s = int(parts[0]);t = int(parts[1]);freq = float(parts[2])
        edge = (s,t) 
        faCounter.update(edge,freq)
'''

num1 = 0
num2 = 100


streamPath = '/data1/Sixing/stream dataset/tweet_stream_hashed_refined' # process stream
N = 4
#maxIDList = [255 for _ in range(N)]
maxID = 17813281
h = 1000
increase = 10
w = 13
hw = 4
lw = 9

'''
# preparing
sghList = getMODlist
MODList = []

for sh in sghList:
    mod = copy.deepcopy(fMODsketch.fMODsketch(maxIDList,sh[1],w,hw,lw,sh[0]))
    MODList.append(mod)
'''

# streaming 
with open(streamPath,'r') as f:
    for line in f:
        if not len(line) > 0:
            continue
        flag = 0
        s = int(parts[0]);t = int(parts[1]);freq = float(parts[2])
        mgCounter.update((s,t), freq)

        if mgCounter.query((s,t)):
            flag = 1
        for i in range(len(MODList)):
            MODList[i].update(flag, (s,t), freq)


'''
# querying
    if edge in 
    MOD.query(flag, edge)
#
'''