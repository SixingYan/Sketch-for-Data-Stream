'''
evaluate #h
'''
#import os;os.chdir('D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment');import testGSketch_h
import random
import newPartition
import gS_StreamList
import gSketch
import modSketch_parti
#from diyTool import savePickle
import cSketch
import hSketch
dataP = 'D:/google desk PC/' # '/data1/Sixing/stream_dataset/' 
dicPath = 'D:/google desk PC/'# '/data1/Sixing/expdata/' #
dataset = [
#[0 dataP, 1 sampleP, 2 sampleP1, 3 sampleP2, 4 n, 5 P, 6 top2000ListPickle, 7 nfoListPicke, 8 efoList_mPickle, 9 resultPath, 10 query type],
#[dataP+'tweet_stream_hashed_refined',dicPath+'tweet_new_0.02.txt',dicPath+'tweet_new_0.1.txt',dicPath+'tweet_new_0.05.txt',2,1391353,dicPath+'tw_top2000',dicPath+'tw_nfo.pk',dicPath+'tw_efo.pk',dicPath+'tw_result.txt','rad'],
[dataP+'sanus_fre_4ij', dicPath+'sanus4ij_new1000_0.2.txt',
dicPath+'sanus4ij_new1000_0.2.txt',dicPath+'sanus4ij_new1000_0.2.txt',2,71863249,dicPath+'sanus_top2000',dicPath+'sanus_nfo.pk',dicPath+'sanus_efo.pk',
dicPath+'sanus_result.txt','rad'], # result
]

##########################################parameter
##########################################parameter
samplePath = dataset[0][1]
w = 5
hDict = [500, 2000] #[300, 500, 1000, 2000]

n = dataset[0][4]
P = dataset[0][5]

hListDict = [[500, 500],[2000, 2000]] #[[159, 566], [265, 944], [530, 1888], [1060, 3777]] 
#hParList = [int(n * 0.9) for n in hList]
#hOutList = [int(n * 0.1) for n in hList]
PList = [P for _ in range(n)]
print('start!')

##########################################gSketch
##########################################gSketch
# 1. get and sort
gSList = []
for h in hDict:
    hPar = int(h**2*0.9)
    hOut = int(h**2*0.1)
    nfoList = gS_StreamList.getSortedStream(dataset[0][1],n)
    print('nfo complete!')
    # 2. get partitioning 
    nrDict = newPartition.callPartition(nfoList, hPar)
    # 3. get gSketch
    gS = gSketch.gSketch(w, n, hPar, hOut, P, nrDict)
    del(nrDict)
    del(nfoList)
    gSList.append(gS)
print('\n\ngSketch complete!')

##########################################pMOD
##########################################pMOD
pMODList = []
for hhh in hListDict:
    hParList = [int(n * 0.9) for n in hhh]
    hOutList = [int(n * 0.1) for n in hhh]
    # 1. get and sort
    efoList_m = gS_StreamList.getSortedStream_m(dataset[0][1], n)
    print('efo complete!')
    # 2. get partitioning 
    nrDict_m = []
    for i in range(n):
        nrDict_m.append(newPartition.callPartition(efoList_m[i], hParList[i]))
    # 3. get gSketch
    mod_p = modSketch_parti.modSketch_parti(w, hParList, hOutList, PList, nrDict_m)
    del(nrDict_m)
    del(efoList_m)
    pMODList.append(mod_p)
print('\n\npMOD complete!')
########################################## cSketch + MODSketch
########################################## cSketch + MODSketch
cSList = []
for h in hDict:
    cS = cSketch.sketch(w, h**2, int(str(P)*2))
    cSList.append(cS)

modList = []
for hhh in hListDict:
    MOD = hSketch.sketch(w, hhh[0], hhh[1], P)
    modList.append(MOD)

########################################## evaluate
########################################## evaluate
def pushTop(item):
    global top2000List

    if len(top2000List) < 2000:
        top2000List.append(item)
        if len(top2000List) == 2000:
            top2000List.sort(key=lambda x: x[1], reverse=True) # from big to small
    else:
        idx = -1
        flag = False
        for i in range(2000):
            if (not idx==-1) and (item[1] > top2000List[i][1]):
                idx = i
            if top2000List[i][0] == item[0]:
                top2000List[i][1] += item[1]
                flag = True
            break
    if not flag:
        top2000List[idx] = item

# 4. evaluate 
print('start streaming')
dataPath = dataset[0][0]
radDict = {}
def performSketch(dataPath):
    global radDict
    count = 0
    with open(dataPath, 'r') as f:
        for line in f:
            line = line.strip()
            if not len(line) > 0:
                continue
            parts = line.split(' ')
            edge = tuple([int(i) for i in parts[:len(parts)-1]])
            freq = float(parts[len(parts)-1])
            if random.random() > 0.4:
                continue
            if edge in radDict.keys():
                radDict[edge] += freq
            else:
                if random.random() < 0.2:
                    radDict[edge] = freq
            count += 1
            if count % 1000000 == 0:
                print('now is '+str(count))
            
            for cS in cSList:
                cS.update(edge, freq)
            for MOD in modList:
                MOD.update(edge, freq)
            for g in gSList:
                g.update(edge, freq)
            for pm in pMODList:
                pm.update(edge, freq)
    #savePickle(dataset[0][6], top2000List)
performSketch(dataPath)

def getRadList_D(num):
    radPoolKey = list(radDict.keys())
    radListKey = []
    while len(radListKey) < num:
        tem = random.choice(radPoolKey)
        if tem not in radListKey:
            radListKey.append(tem)
    radList = []
    for ky in radListKey:
        radList.append([ky,radDict[ky]])
    return radList

def evaluteOE(edgeList, sketch):
    totalFreq = 0
    totalLoss = 0
    for itemFreq in edgeList:
        freq = itemFreq[1]
        edge = itemFreq[0]
        estiFreq = sketch.query(edge)
        totalLoss += abs(estiFreq-freq)
        totalFreq += freq
    return totalLoss/totalFreq

def evaluateQuery(queryList, f):

    f.write('\n\CountMin\n')
    for cS in cSList:
        evalVal = evaluteOE(queryList, cS);f.write(str(evalVal)+' \n')
    
    f.write('\n\MOD-Sketch\n')
    for MOD in modList:
        evalVal = evaluteOE(queryList, MOD);f.write(str(evalVal)+' \n')

    f.write('\n\ngSketch\n')
    for g in gSList:
        evalVal = evaluteOE(queryList, g);f.write(str(evalVal)+' \n')

    f.write('\n\MOD_Part\n')
    for pm in pMODList:
        evalVal = evaluteOE(queryList, pm);f.write(str(evalVal)+' \n')

def evaluateRandom():
    #radList500 = getRadList_D(500)
    radList1000 = getRadList_D(1000)
    #radList2000 = getRadList_D(2000)
    #radList5000 = getRadList_D(5000)
    with open(dataset[0][9]+'_'+dataset[0][10], 'a') as f:
        evaluateQuery(radList1000, f)

evaluateRandom()

'''
            #topDict = {}
            if edge in .keys():
                topDict[edge] += freq
            else:
                if len(topDict) < 500:
                    topDict[edge] = freq
                else:
                    minEdge = getMinEdge(topDict)
                    if topDict[minEdge] < freq:
                        topDict.pop(minEdge)
                        topDict[edge] = freq

def getMinEdge(topDict):
    top
    for 
    return edgeID


def transferEdge(edge, strategy, flag):
    if flag: # (1 2 3 4 freq)

    else: # (1.2.3.4 1.2.3.4 freq)
aaa
    return newEdge
            

'''