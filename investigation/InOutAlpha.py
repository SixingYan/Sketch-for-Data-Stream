import math
import random
#ds = ['/data1/Sixing/stream dataset/tweet_stream_hashed_refined','tweet']
#ds = ['/data1/Sixing/stream dataset/ipv4_sr_4ij','sr_4ij']
ds = ['/data1/Sixing/stream dataset/ipv4_st_4ij','st_4ij']
sSet = set([])
tSet = set([])
sDict = {}
tDict = {}
homePath = '/data1/Sixing/expdata/'

"""
ds = ['D:/google desk PC/graph_freq_comp18.txt','comp18']
#ds = ['D:/google desk PC/graph_freq_comp18.txt','comp18']
#ds = ['D:/google desk PC/graph_freq_comp18.txt','comp18']
sSet = set([])
tSet = set([])
sDict = {}
tDict = {}
homePath = 'D:/google desk PC/'
"""
def refine(vList):
    vSet = set([])
    valueDict = {}
    for v in vList:
        if v == 0:
            continue
        if v in vSet:
            valueDict[v] += 1
        else:
            vSet.add(v)
            valueDict[v] = 0
            valueDict[v] += 1
    # valueList is the refined version of vList
    valueList = sorted(list(vSet),reverse=False) # from small to big
    vfList = []
    for v in valueList:
        vfList.append([v,valueDict[v]])
    del valueDict; del valueList; 
    return vfList

# first stream for degree
with open(ds[0],'r') as f:
    for line in f.readlines():
        #if count > 10:
        #    break
        line = line.strip()
        if not len(line.strip()) > 0:
            continue
        if random.random(0,1) > 0.5:
            continue
        #count += 1
        parts = line.split(' ')
        s = int(parts[0]);t = int(parts[1]);freq = math.ceil(float(parts[2]))
        #print(t)
        # out degree
        if s in sSet:
            sDict[s] += freq
        else:
            sDict[s] = 0
            sDict[s] += freq
            sSet.add(s)
        # in degree
        if t in tSet:
            tDict[t] += freq
        else:
            tDict[t] = 0
            tDict[t] += freq
            tSet.add(t)
tList = []
tNum = len(tSet)
for t in tSet:
    tList.append(tDict[t]) # in degree value list
tList = [int(t) for t in tList]
tfList = refine(tList)
with open(homePath+'inDegree_'+ds[1],'w') as f:
    for t in tfList:
        f.write(str(t[0])+' '+str(t[1])+'\n') # inDegree, freq
del tfList; del tList
sNum = len(sSet)
sList = []
for s in sSet:
    sList.append(sDict[s])
sList = [int(s) for s in sList]
sfList = refine(sList)
with open(homePath+'outDegree_'+ds[1],'w') as f:
    for s in sfList:
        f.write(str(s[0])+' '+str(s[1])+'\n') # inDegree, freq
del sfList; del sList

aList = []
with open(ds[0],'r') as f:
    # out degree
    for line in f.readlines():
        line = line.strip()
        if not len(line.strip()) > 0:
            continue
        parts = line.split(' ')
        s = int(parts[0])
        t = int(parts[1])
        if s in sSet and t in tSet:
            if sDict[s] * tDict[t] == 0:
                continue
            a = round(sDict[s]/tDict[t], 5) # O(i,*)/O(*,j)
            aList.append(a)

afList = refine(aList)
with open(homePath+'alpha_'+ds[1],'w') as f:
    for a in afList:
        f.write(str(a[0])+' '+str(a[1])+'\n') # inDegree, freq
del afList; del aList

del sSet; del tSet; del sDict; del tDict;

with open(homePath+'outin_'+ds[1],'w') as f:
    f.write(str(sNum)+' '+str(tNum)+'\n') #