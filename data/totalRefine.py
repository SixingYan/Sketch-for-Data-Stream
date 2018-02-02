# refined dataset 1+1

import copy
def putinLine(line, path, endtag):
    with open(path ,'a') as f:
        f.write(line+endtag)

homePath = '/data1/Sixing/stream dataset/'
refinedPath = homePath + 'sanusfre4ij_refined'
loopPath0 = homePath + 'sanus_fre_4ij' 
total = 0
countNum = 0

with open(loopPath0, 'r') as f:
    ipDict = {}
    keyList = set([])
    for line in f:
        if not len(line.strip()) > 0:
            continue
        line = line.strip()
        countNum += 1
        if countNum % 10000000 == 0:
            print('now is '+str(countNum))
        parts = line.strip().split(' ')
        s = int(parts[0]); t = int(parts[1]); freq = float(parts[2])
        IPkey = tuple([s,t])
        if IPkey in keyList:
            ipDict[IPkey][0] += freq
        else:
            keyList.add(IPkey)
            keySize += 1
            ipDict[IPkey] = [freq,s,t]

    for IPkey in keyList:
        line = str(ipDict[IPkey][1]) + ' ' + str(ipDict[IPkey][2]) + ' ' + str(ipDict[IPkey][0])  
        putinLine(line, refinedPath,'\n')
