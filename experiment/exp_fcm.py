"""
1. filter: store high freq. edge  
    @ store
    @ update

2. sketch update
    @ if high-freq. or not 
    @ offset/gap/# to update the sketch 
"""



'''

'''
sgStrList = [
'3C0S2C1','3C0S2S1','3C1C0S2',
'3C1S2C0','3C1S2S0','3C2C0S1',
'3C2C1C0','3C2C1S0','3C2S1C0',
'3C2S1S0','3S2C0S1','3S2C1C0',
'3S2C1S0','3S2S1C0','3S2S1S0',
]

from diyTool import getPathDict, getStrategy



N = 4
maxIDList = [255 for _ in range(N)]
h = 10
w = 13
wh = 4
wl = 9

def getMODlist():
    for ss in sgStrList:
        d = getPathDict(ss)
        sg = getStrategy(d)

        hList = []
        for tp in sg
         
        
        return 


winSize = 10000

# preparing

MODList = []

#CM = 
mgCounter = faCounter.faCounter(winSize)

# streaming 
with open() as f:

    edge, freq
    flag = 0
    if mgCounter.query(item):
        flag = 1

    for i in range(len(MODList)):
        MODList[i].update(flag, edge, freq)
    #CM.update(flag, edge, freq)



# querying
    if edge in 
    MOD.query(flag, edge)


#