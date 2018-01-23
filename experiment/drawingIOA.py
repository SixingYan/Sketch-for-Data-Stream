'''
'''
import numpy as np
dataName = 'ip'
homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/investigation/data/'
def getData(path):
    pairList = []
    with open(path+dataName,'r') as f:
        for line in f.readlines():
            parts = line.strip().split(' ')
            pairList.append([float(p) for p in parts])
    return pairList

def refine(vList,step):
    newVList = []
    total = 0
    i = 0
    for v in vList:
        i += 1
        total += v[1]
        if i == step:
            newVList.append([v[0], total])   
            i = 0
            total = 0
    return newVList

inList = getData(homePath+'inDegree_')
inList = refine(inList,30) #comp12 30 comp1 150
meanV = np.mean(inList)
inX = []
inY = []
for i in inList:
    if not i[1] > 10:
        continue
    inX.append(i[0])
    if i[1] > meanV:
        inY.append(meanV)
    else:
        inY.append(i[1])
    
outList = getData(homePath+'outDegree_')
outList = refine(outList,35) #comp12 40 comp1 100
#meanV = np.mean(outList)
outX = []
outY = []
for o in outList:
    if not o[1] > 10:
        continue
    outX.append(o[0])
    if o[1] > meanV:
        outY.append(meanV)
    else:
        outY.append(o[1])

aList = getData(homePath+'alpha_')
aList = refine(aList,6000) # ip 1000 comp12 6000 comp1 6000
meanV = np.mean(aList)
a0X = [];a0Y = []
a1X = [];a1Y = []
for a in aList:
    if not a[1] > 5:
        continue
        
    if a[0] < 1:
        a0X.append(a[0]) 
        if i[1] > meanV:
            a0Y.append(meanV)
        else:
            a0Y.append(a[1]) 
    else:
        a1X.append(a[0]) 
        if i[1] > meanV:
            a1Y.append(meanV)
        else:
            a1Y.append(a[1]) 

import matplotlib.pyplot as plt
plt.figure(1)
tPlot, axes = plt.subplots(nrows=1, ncols=4,figsize=(28,6))
tPlot.tight_layout(renderer=None, pad=3, h_pad=2, w_pad=3, rect=None)
figurePath = 'D:/google desk PC/'

axes[0].plot(range(len(a0Y)),a0Y)
axes[0].set_ylim(0,max([max(a0Y),max(a1Y)]) * 1.05)

#axes[0].set_xticks(range(len(a0Y)))
#axes[0].set_xticklabels(a0X)


axes[1].plot(range(len(a1Y)),a1Y)
axes[1].set_ylim(0,max([max(a0Y),max(a1Y)]) * 1.05)
#axes[1].set_xticks(range(len(a1Y)))
#axes[1].set_xticklabels(a1X)


axes[2].plot(range(len(inY)),inY)
axes[2].set_ylim(0,max([max(inY),max(outY)]) * 1.05)
#axes[2].set_xticks(range(len(inY)))
#axes[2].set_xticklabels(inX)

axes[3].plot(range(len(outY)),outY)
axes[3].set_ylim(0,max([max(inY),max(outY)]) * 1.05)
#axes[3].set_xticks(range(len(outY)))
#axes[3].set_xticklabels(outX)

plt.savefig(figurePath+"inoutalpha_"+str(dataName)+".jpg",dpi=200,bbox_inches='tight') 
plt.show()