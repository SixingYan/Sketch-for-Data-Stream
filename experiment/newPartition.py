# -*- coding: utf-8 -*-
nodeRangeDict = {} #[node] -> index range 
idx = 0
length0 = 50
C = 0.01
nodeFreqOdList = []
NFO = []
DDF = []
rangeList = []

class treeNode(object):
    def __init__(self, length):
        self.length = length
        self.left = None
        self.right = None
        self.isLeaf = True
        self.hashData = None
        self.hashDataSize = None

def prepareInfo_S(nodeFreqOdList):
    #global NFO
    #global DDF
    NFO = []
    DDF = []
    totalNFO = sum(nfo[1] for nfo in nodeFreqOdList)
    totalddf = sum((nfo[2]**2/nfo[1]) for nfo in nodeFreqOdList)
    assNFO = 0
    assDDF = 0
    for i in range(len(nodeFreqOdList)):
        assNFO += nodeFreqOdList[i][1]
        NFO.append((assNFO, totalNFO-assNFO))
        assDDF += round(nodeFreqOdList[i][2]**2/nodeFreqOdList[i][1], 3)
        DDF.append((assDDF, totalddf-assDDF))
    return NFO, DDF

def getPartPivot(hashData):
    # hashData is a range e.g., (100, 150) # robust: try every one
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
    #print('min Pivot is '+str(minPivot))
    return minPivot

def getRError(pivot, side):
    # E = d(m)*F(S)/(f(m)/d(m))
    if side == 'left':
        idx = 0
    else:
        idx = 1
    FS = NFO[pivot][idx]
    ddfVal = DDF[pivot][idx]
    return ddfVal * FS

def partition(node):
    # main function
    od = getOutDegree(node.hashData)
    if node.length/2 < length0 or od < C*node.length: 
        #print('od is '+str(od))
        #print('c * len'+str(C*node.length))
        # stop partition when width is small and when hash node number is small
        return
    else: 
        node.isLeaf = False
        #print('---partition----')
        ln = treeNode(int(node.length/2))
        rn = treeNode(int(node.length-int(node.length/2)))

        pivot = getPartPivot(node.hashData)
        if pivot == 0:
            node.isLeaf = True
            #print('pivot is 0 !!!!!!')
            return 
        ln.hashData = (node.hashData[0], pivot); ln.hashDataSize = pivot-node.hashData[0]
        rn.hashData = (pivot+1, node.hashData[1]); rn.hashDataSize = node.hashData[1] - pivot

        node.left = ln; node.right = rn
        
        #print('partitioning node.length: '+str(node.length))
        partition(ln);partition(rn)

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

def visitTree1(node):
    global idx
    global nodeRangeDict
    if node.isLeaf:
        for i in range(node.hashData[0], node.hashData[1]):
            nodeID = nodeFreqOdList[i][0]
            nodeRangeDict[nodeID] = (idx, idx + node.length)
        idx += node.length
    else:
        visitTree(node.left)
        visitTree(node.right)

def getOutDegree(hashData):
    return sum(nodeFreqOdList[i][2] for i in range(hashData[0], hashData[1]))

def callPartition(nfoList, h):
    # nodeFreqOdList = [] (nodeID, freq., OutDegree)
    global nodeFreqOdList
    global idx
    global nodeRangeDict
    global rangeList
    nodeRangeDict = {}
    rangeList = []
    idx = 0
    #print('len is '+str(len(nfoList)))
    nodeFreqOdList = nfoList
    #print('start partitioning!')
    
    root = treeNode(int(h))
    root.hashData = (0, len(nodeFreqOdList))
    root.hashDataSize = len(nodeFreqOdList)
    partition(root)
    visitTree(root)

    return nodeRangeDict


