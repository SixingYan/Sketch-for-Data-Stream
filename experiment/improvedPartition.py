# -*- coding: utf-8 -*-
nodeRangeDict = {} #[node] -> index range 
idx = 0
length0 = 10
C = 5
nodeFreqOdList = []
NFO = []
DDF = []
rangeList = []
NFO_s = []
DDF_s = []

#nfoList = [] # (nodeID, freq, outDegree)
#nfoSampleList = [] # (same, diff, diff)
class treeNode(object):
    def __init__(self, length):
        self.length = length
        self.left = None
        self.right = None
        self.isLeaf = True
        self.hashData = None
        self.hashDataSize = None

def prepareInfo_S(nList):
    NFO = []
    DDF = []
    totalNFO = sum(nfo[1] for nfo in nList)
    totalddf = sum((nfo[2]**2/nfo[1]) for nfo in nList)
    assNFO = 0
    assDDF = 0
    for i in range(len(nList)):
        assNFO += nList[i][1]
        NFO.append((assNFO, totalNFO-assNFO))
        assDDF += round(nList[i][2]**2/nList[i][1], 3)
        DDF.append((assDDF, totalddf-assDDF))
    return NFO, DDF

def getRError(pivot, side):
    # E = d(m)*F(S)/(f(m)/d(m))
    if side == 'left':
        idx = 0
    else:
        idx = 1
    FS = NFO[pivot][idx]
    ddfVal = DDF[pivot][idx]
    return ddfVal * FS

def getPartPivot(hashData):
    # hashData is a range e.g., (100, 150) 
    minError = float("Inf")
    minPivot = 0
    global NFO
    global DDF
    NFO = []; DDF = []
    NFO, DDF = prepareInfo_S(nodeFreqOdList[hashData[0]:hashData[1]])

    for i in range(length0, hashData[1]-hashData[0]-length0):
        currError = getRError(i, 'left') + getRError(i, 'right')
        if minError > currError:
            minError = currError
            minPivot = i
    minPivot += hashData[0]
    return minPivot

def partition(node):
    # main function
    if node.length/2 < length0 : # or node.hashDataSize < C * node.length:
        # stop partition when width is small and when hash node number is small
        return
    else: 
        node.isLeaf = False
        
        ln = treeNode(int(node.length/2))
        rn = treeNode(node.length-int(node.length/2))

        pivot = getPartPivot(node.hashData)
        ln.hashData = (node.hashData[0], pivot); ln.hashDataSize = pivot-node.hashData[0]
        rn.hashData = (pivot+1, node.hashData[1]); rn.hashDataSize = node.hashData[1] - pivot

        global NFO_s
        global DDF_s
        NFO_s = []; DDF_s = []
        NFO_s, DDF_s = prepareInfo_S(nodeFreqOdList_s[node.hashData[0]:node.hashData[1]])
        if not evaluateChange(pivot-node.hashData[0]): # stop split
            return

        node.left = ln; node.right = rn
        
        print('partitioning node.length: '+str(node.length))
        partition(ln);partition(rn)


def evaluateChange(p):
    isGood = False
    currError = evalError(p,'left') + evalError(p,'right')
    prevError = evalError(0,'right')
    if currError < prevError:
        isGood = True
    else:
        isGood = False
    return isGood


def evalError(pivot, side):
        # E = d(m)*F(S)/(f(m)/d(m))
    if side == 'left':
        ix = 0
    else:
        ix = 1
    FS = NFO_s[pivot][ix]
    ddfVal = DDF_s[pivot][ix]
    return ddfVal * FS


def visit(node):
    global rangeList
    if node == None:
        return
    else:
        visit(node.left)
        if node.isLeaf:
            rangeList.append([node.length, node.hashData])
        visit(node.right)


def visitTree(node):
    global idx
    global nodeRangeDict
    visit(node)
    for i in range(len(rangeList)):
        length = rangeList[i][0]
        rg = (idx, idx + length)
        for j in range(rangeList[i][1][0], rangeList[i][1][1]): 
            nodeID = nodeFreqOdList[j][0]
            nodeRangeDict[nodeID] = rg        
        idx += length


def getOutDegree(hashData):
    return sum(nodeFreqOdList[i][2] for i in range(hashData[0], hashData[1]))


def callPartition(nfoList, nfoList_s, h):
    # nodeFreqOdList = [] (nodeID, freq., OutDegree)
    global nodeFreqOdList
    global nodeFreqOdList_s
    global idx
    global nodeRangeDict
    global rangeList
    nodeRangeDict = {}
    rangeList = []
    idx = 0
    nodeFreqOdList = nfoList
    nodeFreqOdList_s = nfoList_s
    #prepareInfo()
    
    root = treeNode(h)
    root.hashData = (0, len(nodeFreqOdList))
    root.hashDataSize = len(nodeFreqOdList)
    partition(root)
    visitTree(root)

    return nodeRangeDict



























