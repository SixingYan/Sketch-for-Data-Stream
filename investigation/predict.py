'''
'''
import random
sDict = {}
tDict = {}
samplePool = []
dataPath = 'D:/google desk PC/graph_freq_comp18_refine.txt'
with open(dataPath, 'r') as f:
    for line in f:
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

edgeAlphaDict = {}
alphaDict = {}
with open(dataPath, 'r') as f:
    for line in f:
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

for pairs in samplePool:
    s, t = pairs[0]
    freq = pairs[1]
    a = round(sDict_sample[s]/tDict_sample[t],8)
    if a in alphaDict_sample.keys():
        alphaDict_sample[a] += freq
    else:
        alphaDict_sample[a] = freq    

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

totalFreq = 0
edgeTFreq = 0
epsilon = 0.5
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
print(edgeTFreq/totalFreq)



