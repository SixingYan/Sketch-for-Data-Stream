'''
evaluate #sample_size
'''
import random
import newPartition
import gS_StreamList
import gSketch
import modSketch_parti
from diyTool import savePickle, loadPickle
import cSketch
import hSketch
dataP = 'D:/google desk PC/' # '/data1/Sixing/stream_dataset/' 
dicPath = 'D:/google desk PC/'# '/data1/Sixing/expdata/' #
dataset = [
#[0 dataP, 1 sampleP, 2 sampleP1, 3 sampleP2, 4 n, 5 P, 6 top2000ListPickle, 7 nfoListPicke, 8 efoList_mPickle, 9 resultPath, 10 query type],
#[dataP+'tweet_stream_hashed_refined',dicPath+'tweet_new_0.02.txt',dicPath+'tweet_new_0.1.txt',dicPath+'tweet_new_0.05.txt',2,1391353,dicPath+'tw_top2000',dicPath+'tw_nfo.pk',dicPath+'tw_efo.pk',dicPath+'tw_result.txt','rad'],
[dataP+'tweet_stream_hashed_refined', # data
[dicPath+'tweet_new_0.005.txt', dicPath+'tweet_new_0.003.txt',dicPath+'tweet_new_0.05.txt',dicPath+'tweet_new_0.02.txt',dicPath+'tweet_new_0.01.txt',], # sample
dicPath+'tweet_new_0.1.txt',dicPath+'tweet_new_0.05.txt',2,17813333,dicPath+'tw_top2000',dicPath+'tw_nfo.pk',dicPath+'tw_efo.pk',
dicPath+'tweet_h_result.txt','top'], # result
]

##########################################parameter
##########################################parameter
samplePath = dataset[0][1]
w = 5
h = 2000
hPar = int(h**2*0.9)
hOut = int(h**2*0.1)
n = dataset[0][4]
P = dataset[0][5]

hList = [1060, 3777]
hParList = [int(n * 0.9) for n in hList]
hOutList = [int(n * 0.1) for n in hList]
PList = [P, P]
top2000List = []
print('start!')

##########################################gSketch
##########################################gSketch
# 1. get and sort
gSList = []
for path in dataset[0][1]:
    nfoList = gS_StreamList.getSortedStream(path, n)
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
for path in dataset[0][1]:
    # 1. get and sort
    efoList_m = gS_StreamList.getSortedStream_m(path, n)
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
cS = cSketch.sketch(w, h**2, int(str(P)*2))
MOD = hSketch.sketch(w, hList[0], hList[1], P)
print('baseline completed!')

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
sketchList = [cS, MOD]
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
            count += 1
            if count % 1000000 == 0:
                print('now is '+str(count))
            '''
            if edge in radDict.keys():
                radDict[edge] += freq
            else:
                if random.random() < 0.2:
                    radDict[edge] = freq
            '''
            #pushTop((edge, freq))
            for sketch in sketchList:
                sketch.update(edge, freq)
            for g in gSList:
                g.update(edge, freq)
            for pm in pMODList:
                pm.update(edge, freq)
    #savePickle(dataset[0][6], top2000List)

performSketch(dataPath)
top2000List = loadPickle('D:/google desk PC/tw_top2000.pickle')
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
    sketchName = ['CountMin', 'MOD-Sketch']
    for i in range(2):
        name = sketchName[i]
        f.write(name+' \n')
        sketch = sketchList[i]
        evalVal = evaluteOE(queryList, sketch);
        f.write(str(evalVal)+' \n')
        f.write('\n')

    f.write('\n\ngSketch\n')
    for g in gSList:
        evalVal = evaluteOE(queryList, g);f.write(str(evalVal)+' \n')
        
    f.write('\n\nMOD_Part\n')
    for pm in pMODList:
        evalVal = evaluteOE(queryList, pm);f.write(str(evalVal)+' \n')
        
        
def evaluateRandom():
    #radList500 = getRadList_D(500)
    radList1000 = getRadList_D(1000)
    #radList2000 = getRadList_D(2000)
    #radList5000 = getRadList_D(5000)
    #with open(dataset[0][9]+'_'+dataset[0][10], 'a') as f:
    #    evaluateQuery([radList500,radList1000,radList2000,radList5000], f)
    with open(dataset[0][9]+'_'+dataset[0][10], 'a') as f:
        evaluateQuery(radList1000, f)
        
def evaluateTop():
    top100List = top2000List[:100]
    with open(dataset[0][9]+'_'+dataset[0][10], 'a') as f:
        evaluateQuery(top100List, f)
        
evaluateTop()

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