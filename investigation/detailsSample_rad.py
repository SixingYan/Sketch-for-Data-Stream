#import os;os.chdir('D:/google desk PC');import detailsSample_rad
from publicTool import get_Prime, getTwoRandomNum, savePickle
from random import randint, choice
from copy import deepcopy

filename = 'D:/Download/ip_graph_refined'
w = 10
h = 500
sizeNum = 500
maxNodeID = 4213084
edgeMax = int(str(maxNodeID)+str(maxNodeID))
queryList = []

radPool = []
def getQueryList():
    with open(filename, 'r') as f:
        print('-----prepare and update-----')
        for line in f:
            line = line.strip()
            if len(line)>0:
                parts = line.split(' ')
                s = int(parts[0]);t = int(parts[1]);freq = int(float(parts[2]))
                if randint(0,100)<15:
                    radPool.append((s,t,freq))

print('prepare top list ')
getQueryList()

while len(queryList) < sizeNum:
    element = choice(radPool)
    if element not in queryList:
        queryList.append(element)

def prepareDict(queryList):
    d = {}
    for s,t,f in queryList:
        d[(s,t)] = []
    return d
def generateEdgeID(s,t):
    if len(str(t)) < len(str(maxNodeID)):
        num = len(str(maxNodeID))-len(str(t))
        tStr = '0' * num + str(t)
    else:
        return str(s)+str(t)
    return str(s)+tStr

class csketch(object):
    def __init__(self, w, H, N, queryList, name):
        self.name = name
        self.w = w
        self.H = H
        self.N = N
        self.qEdgeDict = prepareDict(queryList)
        self.cellDict = {}
        self.P = get_Prime(self.N)
        self.mask = [getTwoRandomNum(self.P) for _ in range(self.w)]

    def get_hash(self, node):
        i = hash(node)
        for m in self.mask:
            a, b = m[0], m[1]
            yield (i * a + b) % self.P % self.H

    def checkUpdate(self, edgeFre):
        # for 500 edges only
        s, t, f = edgeFre
        edgeID = int(generateEdgeID(s,t))
        hashEdge = []
        for wD, p in zip(range(self.w), self.get_hash(edgeID)):
            hashEdge.append((wD,p))
        hashEdge = list(set(hashEdge))
        self.qEdgeDict[(s,t)] = hashEdge
        for cell in hashEdge:
            if cell not in list(self.cellDict.keys()):
                self.cellDict[cell] = [(s, t, f)]
            else:
                self.cellDict[cell].append((s, t, f))
                
    def expUpdate(self, edge, f=1):
        # for all edges otherwise
        s, t = edge
        edgeID = int(generateEdgeID(s, t))
        for wD, p in zip(range(self.w), self.get_hash(edgeID)): 
            if (wD,p) in list(self.cellDict.keys()):
                self.cellDict[(wD,p)].append((s,t,f)) # this cell also stores which edges

    def query(self, edge): # query rad/top list only 
        #
        minV = 0; idx = 0
        for cell in self.qEdgeDict[edge]:
            cValue = getSum(self.cellDict[cell])#cValue = sum(self.cellDict[cell], key = lambda x: x[2])
            if minV == 0:
                minV = cValue; idx = cell
                continue
            if cValue < minV:
                minV = cValue; idx = cell
        return minV,self.cellDict[idx]   
    
class gmatrix(object):
    def __init__(self, w, h, N, queryList, name):
        self.name = name
        self.w = w
        self.h = h
        self.N = N
        self.qEdgeDict = prepareDict(queryList)
        self.cellDict = {}
        self.P = get_Prime(self.N)
        self.mask = [getTwoRandomNum(self.P) for _ in range(self.w)]

    def get_hash(self, node):
        i = hash(node)
        for m in self.mask:
            a, b = m[0], m[1]
            yield (i * a + b) % self.P % self.h

    def checkUpdate(self, edge):
        # for 500 edges only
        s, t, f = edge
        hashEdge = []
        for wD, p, q in zip(range(self.w), self.get_hash(s), self.get_hash(t)):
            hashEdge.append((wD,p,q))
        hashEdge = list(set(hashEdge))
        self.qEdgeDict[(s,t)] = hashEdge
        for cell in hashEdge:
            if cell not in list(self.cellDict.keys()):
                self.cellDict[cell] = [(s, t, f)]
            else:
                self.cellDict[cell].append((s, t, f))
                
    def expUpdate(self, edge, f=1):
        # for all edges otherwise
        s, t = edge
        for wD, p, q in zip(range(self.w), self.get_hash(s), self.get_hash(t)): 
            if (wD,p,q) in list(self.cellDict.keys()):
                self.cellDict[(wD,p,q)].append((s,t,f)) # this cell also stores which edges

    def query(self, edge): # query rad/top list only 
        #
        minV = 0; idx = 0
        for cell in self.qEdgeDict[edge]:
            cValue = getSum(self.cellDict[cell])#cValue = sum(self.cellDict[cell], key = lambda x: x[2])
            if minV == 0:
                minV = cValue; idx = cell
                continue
            if cValue < minV:
                minV = cValue; idx = cell
        return minV,self.cellDict[idx]
    
class hsketch(object):
    def __init__(self, w, h1, h2, N, queryList, name):
        self.name = name
        self.w = w
        self.h1 = h1
        self.h2 = h2
        self.N = N
        self.qEdgeDict = prepareDict(queryList)
        self.cellDict = {}
        self.P = get_Prime(self.N)
        self.mask = [getTwoRandomNum(self.P) for _ in range(self.w)]
        
    def get_hash(self, node, h):
        i = hash(node)
        for m in self.mask:
            a, b = m[0], m[1]
            yield (i * a + b) % self.P % h

    def checkUpdate(self, edge):
        # for 500 edges only
        s, t, f = edge
        hashEdge = []
        for wD, p, q in zip(range(self.w), self.get_hash(s,self.h1), self.get_hash(t,self.h2)):
            hashEdge.append((wD,p,q))
        hashEdge = list(set(hashEdge))
        self.qEdgeDict[(s,t)] = hashEdge
        for cell in hashEdge:
            if cell not in list(self.cellDict.keys()):
                self.cellDict[cell] = [(s, t, f)]
            else:
                self.cellDict[cell].append((s, t, f))

    def expUpdate(self, edge, f=1):
        # for all edges otherwise
        s, t = edge
        for wD, p, q in zip(range(self.w), self.get_hash(s,self.h1), self.get_hash(t,self.h2)): 
            if (wD,p,q) in list(self.cellDict.keys()):
                self.cellDict[(wD,p,q)].append((s,t,f)) # this cell also stores which edges

    def query(self, edge): # query rad/top list only 
        #
        minV = 0; idx = 0
        for cell in self.qEdgeDict[edge]:
            cValue = getSum(self.cellDict[cell])
            if minV == 0:
                minV = cValue; 
                idx = cell
                continue
            if cValue < minV:
                minV = cValue; 
                idx = cell
            
        return minV,self.cellDict[idx]

def geth2(h1):
    return int(h**2/h1)

def getSum(cells):
    total = 0
    for c in cells:
        total += c[2]
    return total

print('prepare structure')

gM = gmatrix(w,h,maxNodeID, queryList, 'gm')
cS = csketch(w,h**2,edgeMax, queryList, 'cs')
h1List = [550,650,750,4000,5000,6000]
sketchList = []

for i in range(len(h1List)):
    h1 = h1List[i]
    h2 = geth2(h1)
    print('for %d, h1 is %d   h2 is %d'%(i,h1,h2))
    hS = deepcopy(hsketch(w,h1,h2, maxNodeID, queryList, 'hs'+str(h1List[i])))
    sketchList.append(hS)

for qEdge in queryList:
    s,t,f = qEdge
    gM.checkUpdate(qEdge)  
    cS.checkUpdate(qEdge)
    for i in range(len(sketchList)):
        sketchList[i].checkUpdate(qEdge)

def getSketch():
    countNum = 0
    with open(filename, 'r') as f:
        print('-----prepare and update-----')
        for line in f:
            line = line.strip()
            if len(line)>0:
                countNum += 1
                parts = line.split(' ')
                s = int(parts[0]);t = int(parts[1]);freq = int(float(parts[2]))
                if (s,t,freq) in queryList:
                    continue
                else:
                    cS.expUpdate((s,t),freq)
                    gM.expUpdate((s,t),freq)
                    for i in range(len(sketchList)):
                        sketchList[i].expUpdate((s,t),freq)
print('start stream')
getSketch()
def evalList(sketch):
    dictName = ''
    if sketch.name == 'hs':
        dictName = sketch.name+str(sketch.h1)
    else:
        dictName = sketch.name
    obDict[dictName] = []
    for qEdge in queryList:
        s,t,f = qEdge
        esValue, esEdge = sketch.query((s,t))
        obErr = abs(esValue-f)/f;
        resultDict[qEdge][dictName] = [esValue, esEdge, obErr] 
        obDict[dictName].append(obErr)

print('start evaluating')
resultDict = {}
for s,t,f in queryList:
    resultDict[(s,t,f)] = {}
obDict = {}

evalList(cS)
evalList(gM)
for i in range(len(sketchList)):
    evalList(sketchList[i])

for ky in list(resultDict.keys()):
    print()
    print('query: '+str(ky))
    print('----------cs----------')
    print('error: '+str(resultDict[ky]['cs'][2]))
    print('return value: '+str(resultDict[ky]['cs'][0]))
    print('cell contains: '+str(resultDict[ky]['cs'][1]))
    print()
    print('----------gm----------')
    print('error: '+str(resultDict[ky]['gm'][2]))
    print('return value: '+str(resultDict[ky]['gm'][0]))
    print('cell contains: '+str(resultDict[ky]['gm'][1]))
    print()
    for i in range(len(sketchList)):
        evalList(sketchList[i])
        print('----------'+sketchList[i].name+'----------')
        print('error: '+str(resultDict[ky][sketchList[i].name][2]))
        print('return value: '+str(resultDict[ky][sketchList[i].name][0]))
        print('cell contains: '+str(resultDict[ky][sketchList[i].name][1]))
        print()


savePickle('D:/google desk PC/pickle/ip_rad500_500_resultDict',resultDict)
savePickle('D:/google desk PC/pickle/ip_rad500_500_obDict',obDict)
