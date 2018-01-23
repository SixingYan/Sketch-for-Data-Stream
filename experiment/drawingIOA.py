'''
'''

dataName = 'tweet'
def getData(path):
    pairList = []
    with open(path+dataName,'r') as f:
        for line in f.readlines():
            parts = line.strip().split(' ')
            pairList.append(parts)
    return pairList


plt.figure(figureID)
tPlot_top, axes = plt.subplots(nrows=1, ncols=4,figsize=(5,16))
tPlot.tight_layout(renderer=None, pad=2, h_pad=2, w_pad=2, rect=None)

inX = []
inY = []
for i in inList:
    inX.append(i[0])
    inY.append(i[1])

axes[2].plot(range(len(inY)),inY)
axes[2].set_xticks(range(len(inY)))
axes[2].set_xticklabels(inX)

outX = []
outY = []
for o in outList:
    outX.append(o[0])
    outY.append(o[1])

axes[3].plot(range(len(outY)),outY)
axes[3].set_xticks(range(len(outY)))
axes[3].set_xticklabels(outX)

a0X = [];a0Y = []
a1X = [];a1Y = []
for a in aList:
    if a[0] < 1:
        a0X.append(a[0]) 
        a0Y.append(a[1]) 
    else:
        a1X.append(a[0]) 
        a1Y.append(a[1])

axes[0].plot(range(len(a0Y)),a0Y)
axes[0].set_xticks(range(len(a0Y)))
axes[0].set_xticklabels(a0X)


axes[1].plot(range(len(a1Y)),a1Y)
axes[1].set_xticks(range(len(a1Y)))
axes[1].set_xticklabels(a1X)

plt.show()