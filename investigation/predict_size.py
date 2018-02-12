'''
'''
import pickle
import random
sDict = {}
tDict = {}
samplePool = []
#dataPath = '/data1/Sixing/stream_dataset/tweet_stream_hashed_refined'
dataPath = '/data1/Sixing/expdata/sample/tweet_'
size = '0.05'
def savePickle(varName, var):
    varName += '.pickle'
    with open(varName, 'wb') as f:
        pickle.dump(var,f)

def loadPickle(varName):
    with open(varName, 'rb') as f:
        var = pickle.load(f)
    return var

with open(dataPath+size+'.txt', 'r') as f:
    for line in f.readlines():
        line = line.strip()
        if not len(line)>0:
            continue
        parts = line.split(' ')
        s = int(parts[0])
        t = int(parts[1])
        freq = float(parts[2])
        if s in sDict.keys():
            sDict[s] += freq
        else:
            sDict[s] = 0
            sDict[s] += freq
        if t in tDict.keys():
            tDict[t] += freq
        else:
            tDict[t] = 0
            tDict[t] += freq
        edge = [s,t]
        
        if random.random() < 0.2:
            samplePool.append([edge, freq * 0.2])
print('first part!')
with open('/data1/Sixing/expdata/txt_process'+size+'.txt','a') as f:
    f.write('first part!\n')
savePickle('/data1/Sixing/expdata/sDict.pickle'+size,sDict)
savePickle('/data1/Sixing/expdata/tDict.pickle'+size,tDict)
savePickle('/data1/Sixing/expdata/samplePool.pickle'+size,samplePool)

edgeAlphaDict = {}
alphaDict = {}
with open(dataPath+size+'.txt', 'r') as f:
    for line in f.readlines():
        line = line.strip()
        if not len(line)>0:
            continue
        parts = line.split(' ')
        s = int(parts[0])
        t = int(parts[1])
        freq = float(parts[2])
        a = round(sDict[s]/tDict[t],8)
        if a in alphaDict.keys():
            alphaDict[a] += int(freq)
        else:
            alphaDict[a] = int(freq)
        edge = [s,t]
        
        if a in edgeAlphaDict.keys():
            edgeAlphaDict[a].append([edge, freq])
        else:
            edgeAlphaDict[a] = [[edge, freq]]
print('2 part!')
with open('/data1/Sixing/expdata/txt_process'+size+'.txt','a') as f:
    f.write('second part!\n')
savePickle('/data1/Sixing/expdata/edgeAlphaDict.pickle'+size,edgeAlphaDict)
savePickle('/data1/Sixing/expdata/alphaDict.pickle'+size,alphaDict)

alphaDict_sample = {}
sDict_sample = {}
tDict_sample = {}

for pairs in samplePool:
    s, t = pairs[0]
    freq = pairs[1]
    if s in sDict_sample.keys():
        sDict_sample[s] += freq
    else:
        sDict_sample[s] = freq
    if t in tDict_sample.keys():
        tDict_sample[t] += freq
    else:
        tDict_sample[t] = freq
print('3 part!')
with open('/data1/Sixing/expdata/txt_process'+size+'.txt','a') as f:
    f.write('3 part!\n')
for pairs in samplePool:
    s, t = pairs[0]
    freq = pairs[1]
    a = round(sDict_sample[s]/tDict_sample[t],8)
    if a in alphaDict_sample.keys():
        alphaDict_sample[a] += freq
    else:
        alphaDict_sample[a] = freq    
print('4 part!')
with open('/data1/Sixing/expdata/txt_process'+size+'.txt','a') as f:
    f.write('4 part\n')

savePickle('/data1/Sixing/expdata/alphaDict_sample.pickle'+size,alphaDict_sample)
savePickle('/data1/Sixing/expdata/sDict_sample.pickle'+size,sDict_sample)
savePickle('/data1/Sixing/expdata/tDict_sample.pickle'+size,tDict_sample)

def getMedianA(alphaDict_sample):
    alphaList_sample = list(alphaDict_sample.items())
    alphaList_sample.sort(key=lambda x: x[1]) # (a,freq)   
    totalSUM = 0
    for i in range(len(alphaList_sample)):
        totalSUM += alphaList_sample[i][1]
    indx = int(totalSUM/2)
    tem = 0
    for i in range(len(alphaList_sample)):
        tem += alphaList_sample[i][1]
        if tem>indx:
            return alphaList_sample[i][0]

esti_a = getMedianA(alphaDict_sample)
print('5 part!')
with open('/data1/Sixing/expdata/txt_result'+size+'.txt','a') as f:
    f.write('esti_a:'+str(esti_a)+'\n\n')

epsilonList = [(i+1) * 0.01 for i in range(99)]
for epsilon in epsilonList:
    totalFreq = 0
    edgeTFreq = 0
    sSet = set([])
    tSet = set([])
    for a in list(edgeAlphaDict.keys()):
        for e in edgeAlphaDict[a]:
            totalFreq += e[1]
        if a < esti_a*(1+epsilon) and a > esti_a*(1-epsilon):
            for e in edgeAlphaDict[a]:
                edgeTFreq += e[1]
                s, t = e[0]
                sSet.add(s)
                tSet.add(t)

    with open('/data1/Sixing/expdata/txt_result'+size+'.txt','a') as f:
        f.write('epsilon:'+str(esti_a)+' '+'ratio'+str(edgeTFreq/totalFreq)+'\n')
        f.write('s len:'+str(len(sSet))+' '+'t len'+str(len(tSet))+'\n')
        f.write('\n')
print('6 part!')



