# refined dataset 4+4
import os
import copy
def putinLine(line, path, endtag):
    with open(path ,'a') as f:
        f.write(line+endtag)

homePath = '/data1/Sixing/'
refinedPath = homePath + 'ipv4fre_refined'
loopPath0 = homePath + 'ipv4fre_0' 
total = 0
countNum = 0
ipDict = {}
time = 0
while True:    
    print('=========time is '+str(time))
    if time == 0:
        oldPath = copy.deepcopy(loopPath0)
        loopPath = copy.deepcopy(loopPath0)
    else:
        oldPath = copy.deepcopy(loopPath)
    parts = loopPath.split('_');loopPath = parts[0] # delete No. number
    time += 1
    loopPath = loopPath + '_' + str(time) 
    print('stream begin')
    print('old is '+oldPath)
    print('new is'+loopPath)
    with open(oldPath, 'r') as f:
        keyList = set([])
        keySize = 0
        for line in f.readlines():
            if not len(line) > 0:
                continue
            countNum += 1
            if countNum % 10000000 == 0:
                print('now is '+str(countNum))
            parts = line.strip().split(' ')
            s = parts[0]; t = parts[1]; freq = parts[2]
            try:
                sParts = s.strip().split('.')
                tParts = t.strip().split('.')
                for i in range(len(sParts)):
                    sParts[i] = int(sParts[i])
                for i in range(len(tParts)):
                    tParts[i] = int(tParts[i])
            except:
                continue
            allIP = []; allIP.extend(sParts); allIP.extend(tParts)
            IPkey = tuple(allIP)
            #keyList = list(ipDict.keys())
            if IPkey in keyList:
                ipDict[IPkey][0] += freq
            else:
                if keySize < 10000000: #
                    keyList.add(IPkey)
                    keySize += 1
                    ipDict[IPkey] = [freq,s,t]
                else: #
                    putinLine(line,loopPath,'')
            #if countNum > 10000:
                #break
        print('putin')
        # stream stop, put in refined stream
        for IPkey in keyList:
            line = ipDict[IPkey][1] + ' ' + ipDict[IPkey][2] + ' ' + ipDict[IPkey][0]  
            putinLine(line, refinedPath,'\n')
    if time == 3000:
        break
    os.remove(oldPath)