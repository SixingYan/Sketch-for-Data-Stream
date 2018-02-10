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

sDict


radPool = []
top1000List = []

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

        # out degree
        if s in sDict.keys():
            sDict[s] += freq
        else:
            sDict[s] = 0
            sDict[s] += freq
        # in degree
        if t in tDict.keys():
            tDict[t] += freq
        else:
            tDict[t] = 0
            tDict[t] += freq
        
        edge = [s,t]

        for _ in range(int(freq)):
            if random.random() < 0.2:
                radPool.append(edge) # make it flat stream


# 计算 s/t of sample
for edge in radPool:


# 计算 alpha
with open(, 'r') as f:



# sort
alphaList = alphaDict.items()
alphaList.sort()


# alpha = 1 


for 













