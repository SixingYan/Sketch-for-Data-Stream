
import numpy as np
"""
Training:

input a stream (list)
output the hash-partition
1. sorted
2. partition -> evaluate 

"""
dataPath = ''
h = 2000
#(node, freq), already sort
streamList = []
length0 = 5
edgeDict = {}
class node(object):
    """docstring for node"""
    def __init__(self, length):
        self.length = length
        self.left = None
        self.right = None
PList = []
root = node()        
hwList = []
hwDict = {}
lenList = []
#nodeFreqList

class gSketch_sub(object):
    def __init__(self, w, hshList, PList, hList, hwList):
        self.w = w
        self.hshList = hshList
        self.PList = PList
        self.hList = hList
        self.hwList = hwList
        self.gSketch = np.zeros(tuple([self.w] + self.hList))

    def hashPartition(self, node, i):
        val = hash(node)
        hshIdx = hwDict[val]
        hv = val % self.PList[i] % self.hshList[hshIdx]
        idx = hv
        for i in range(self.hwList[hshIdx]):
            idx += self.hwList[i]
        return idx

    def transferEdge():

        return newEdge
    
    def query(self, edge):
        newEdge = transferEdge(edge)
        idxList = []
        for i in range(len(newEdge)):
            idx = self.hashPartition(newEdge[i], i)
            idxList.append(idx)
        minV = float("inf")
        for wIdx in range(self.w):
            if minV > self.gSketch[wIdx][tuple(idxList)]:
                minV = self.gSketch[wIdx][tuple(idxList)]
        return minV 

    def update(self, edge, freq=1):
        newEdge = transferEdge(edge)
        idxList = []
        for i in range(len(newEdge)):
            idx = self.hashPartition(newEdge[i], i)
            idxList.append(idx)
        for wIdx in range(self.w):
            self.gSketch[wIdx][tuple(idxList)] = freq
        
def evaluteARE_All(sketch):
    totalErr = 0
    for ky in edgeDict.keys():
        freq = edgeDict[ky]
        estiFreq = sketch.query(ky)
        totalErr += (estiFreq/freq - 1)
    k = len(list(edgeDict.keys()))
    return totalErr/k

def evaluteOE_All(sketch):
    totalFreq = 0
    totalLoss = 0
    for ky in edgeDict.keys():
        freq = edgeDict[ky]
        estiFreq = sketch.query(ky)
        totalLoss += abs(estiFreq-freq)
        totalFreq += freq
    return totalLoss/totalFreq

def getSortedStream():
    
    with open(dataPath,'r') as f:
        for line in f.readlines():
            line = line.strip()
            if not len(line)>0:
                continue
        
            parts = line.split(' ')
            edge = [int(i) for i in parts[:4]]
            edge = ((edge[0],edge[1]),(edge[2],edge[3]))
            freq = float(parts[4])
            if edge in edgeDict.keys():
                edgeDict[edge] += freq

    print('get stream complete!\n')
    streamList = list(edgeDict.items)

    streamList.sorted()
    print('stream sorted complete!\n')

def visitTree(n):
    #
    if n == None:
        return 
    else:
        visitTree(n.left)
        visitTree(n.right)
        # 只记录叶子节点
        hwList.append(n.length)

def getPartiton():
    global hwList
    hwList = [] # clear
    visitTree(root)

def getPartitHash():

    '''
    这里不对
    '''
    global hwDict
    global lenList
    hwDict = {} # clear
    rgList = []
    p = 0 
    for i in range(len(hwList)):
        tem = [p] # setup
        p += hwList[i]
        tem.append(p)
        rgList.append(tem)
    lenList = []
    for i in range(len(rgList)):
        sIdx, eIdx = rgList[i]
        part = streamList[sIdx, eIdx]
        lenList.append(eIdx-sIdx)
        for node in part:
            hwDict[node] = i

def evalSketch():
    hshList = []
    for i in range(len(lenList)):
        hshList.append(h * lenList[i]/sum(lenList))
    gs = gSketch_sub(hshList, PList)
    
    for ky in list(edgeDict.keys()):
        gs.update(ky, edgeDict[ky])

    newErr = evaluteARE_All(gs)
    return newErr

def evaluate():
    global oldErr
    result = False
    getPartiton() # get the current partition tree
    getPartitHash() # generate partition plan
    newErr = evalSketch(hwList, hwDict)# evaluate sketch on sample

    if oldErr > newErr:
        result = True
        oldErr = newErr
    return result

def partition(n):
    if n.length/2 < length0:
        return None
    ln = node(int(n.length/2))
    rn = node(n.length-int(n.length/2))
    n.left = ln
    n.right = rn

    if evaluate():
        partition(ln)
        partition(rn)
    else:
        n.left = None
        n.right = None


for ky in list(edgeDict.keys()):
    freq = edgeDict[ky]
    if freq in freqDict.keys():
        freqDict[freq].append(ky)
    else:
        freqDict[freq] = []
        freqDict[freq].append(ky)

freqEdgeList = list(freqDict.items())
freqEdgeList.sorted()