# -*- coding: utf-8 -*-


w = 10
h = 50
n = 4
maxIDList = [255 for i in range(n)]
hList = [h for i in range(n)]

class treenode(object):
    """docstring for ClassName"""
    def __init__(self, partID, nodeID, priorID, order):
        #super(ClassName, self).__init__()
        self.isLeaf = False # true/false
        self.partID = partID
        self.nodeID = nodeID
        self.priorID = priorID
        self.order = order 
        self.nextNodes = {} # key is node ID
def getCandidate(node):
    pathStr = getPath(node)
    #print('obtaining path '+pathStr)
    pd = getPathDict(pathStr)
    return list(set(partList) - set(pd['partID']))

def getPathDict(pathStr):
    # input a string 
    pathDict = {}
    pathDict['partID'] = []
    pathDict['edgeType'] = []
    preIndex = 0
    for i in range(len(pathStr)):
        if pathStr[i] == 'S' or pathStr[i] == 'C':
            pathDict['partID'].append(int(pathStr[preIndex:i]))
            if pathStr[i] == 'S':
                pathDict['edgeType'].append(0)
            else:
                pathDict['edgeType'].append(1)
            preIndex = i + 1
    pathTem = pathStr[::-1]# reverse string
    idx = 0
    #print(pathTem)
    for i in range(len(pathTem)):
        if pathTem[i] == 'S' or pathTem[i] == 'C':
            idx = i
            break
    pathDict['partID'].append(int(pathStr[-idx:]))
    return pathDict

def getPath(node):
    # return path = {'partID':[0,3,5,7],'edge':[S,C,S,...]}
    if node.priorID == -1:
        #print('getting root')
        return str(node.partID)
    else:
        priorNode = nodeDict[node.priorID]
        edgeType = priorNode.nextNodes[node.nodeID]
        return getPath(priorNode) + edgeType + str(node.partID) 

def buildTree(node):
    global globalNodeID
    # node is not leaf
    #print('getting candidate '+str(node.partID))
    candidate = getCandidate(node) # 没出现在path上的partID
    for partID in candidate:
        if partID < node.partID: # MIND!!!! here should be part.order < part.order 
            #globalNodeID += 1
            subnode = treenode(partID, globalNodeID, node.nodeID, node.order+1);
            globalNodeID += 1
            nodeDict[subnode.nodeID] = subnode # store this node
            node.nextNodes[subnode.nodeID] = 'C' # 因为part ID 不唯一
            if subnode.order < N:# not leaf 
                buildTree(subnode)
            else:
                subnode.isLeaf = True # use for search 
                currentPath = getPath(subnode) # list-type
                leafDict[subnode.nodeID] = currentPath
    
    #for partID in candidate:
    subnode = treenode(max(candidate), globalNodeID, node.nodeID, node.order+1)
    globalNodeID += 1
    nodeDict[subnode.nodeID] = subnode # store this node
    node.nextNodes[subnode.nodeID] = 'S'
    if subnode.order < N:# not leaf 
        buildTree(subnode)
    else:
        subnode.order  = True #
        currentPath = getPath(subnode) # str-type
        leafDict[subnode.nodeID] = currentPath
        #break # each node only have one dotted edge

def getStrategy(pathDict):
    # edge=0 seperate  edge=1 combine 
    j = 0
    strategy = []#[[],...[]]
    for i in range(len(pathDict['partID'])):
        if i == len(pathDict['partID'])-1:
            continue
        if i == 0:
            strategy.append([])
            strategy[j].append(pathDict['partID'][i])
        edge = pathDict['edgeType'][i]
        if edge == 1:
            strategy[j].append(pathDict['partID'][i+1])
        else:
            strategy.append([])
            j += 1
            strategy[j].append(pathDict['partID'][i+1])
    return strategy

pathNum = []
def generateSketch(num):
    globalNodeID = 0
    # -*- coding: utf-8 -*-
    N = num
    #global globalNodeID
    globalNodeID = 0
    partList = [i for i in range(N)]
    nodeDict = {}
    leafDict = {}
    rootID = max(partList) #diyTool.getRoot()
    root = treenode(rootID, globalNodeID, -1, 1)
    nodeDict[globalNodeID] = root # store this node
    globalNodeID += 1
    buildTree(root)
    #print(len(list(leafDict.keys())))
    #pathNum.append(len(list(leafDict.keys())))
    #del nodeDict; del leafDict;

    sketchList = []
    for ky in list(leafDict.keys()):
        pathStr = leafDict[ky]
        d = getPathDict(pathStr)
        stra = getStrategy(d)

        sketch = copy.deepcopy(mSketch.mSketch(maxID,hList,w,stra))
        sketchList.append(sketch)


