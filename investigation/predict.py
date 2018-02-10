'''

'''

edgeDict = {}
alphaDict = {}
sDict = {}
tDict = {}

edgeDict_sample = {}
alphaDict_sample = {}
sDict_sample = {}
tDict_sample = {}

radPool = []
samplePool = []
top1000List = []
rad2000List = []

dataPath = ''
samplePath = ''

# 计算 s/t
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
            radPool.append([edge,freq])
        
        if len(top1000List)>1000:
            minV = min(top1000List, key=lambda x: x[1])
            if freq>minV[1]:
                indx = top1000List.index(minV);top1000List[indx] = [edge,freq]
        else:
            top1000List.append([edge,freq])

        for _ in range(int(freq)):
            if random.random() < 0.2:
                samplePool.append(edge) # make it flat stream

# 计算 s/t of sample
for edge in radPool:
    s, t = edge
    if s in sDict_sample.keys():
        sDict_sample[s] += 1
    else:
        sDict_sample[s] = 0
        sDict_sample[s] += 1
    if t in tDict_sample.keys():
        tDict_sample[t] += 1
    else:
        tDict_sample[t] = 0
        tDict_sample[t] += 1

# 计算 alpha
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
        a = round(sDict[s]/tDict[t],8)
        edgeDict[edge] = [a, freq]
        alphaDict[a] += int(freq)

# sort
alphaList = alphaDict.items()
alphaList.sort(key=lambda x: x[0]) # (a, freq)

edgeList = edgeDict.items()
edgeList.sort(key=lambda x: x[1][0]) #(edge,[a,freq]) 

# alpha = 1 
for edge in radPool:
    s, t = edge
    a = round(sDict_sample[s]/tDict_sample[t],8)
    #edgeDict_sample[edge] = [a, freq]
    alphaDict_sample[a] += 1

alphaList_sample = alphaDict_sample.items()
alphaList_sample.sort(key=lambda x: x[1])

esti_a = median()











