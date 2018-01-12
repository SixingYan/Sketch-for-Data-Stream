"""
generate all paths of global tree

the order of root is 1
"""

import sketchTreeNode
N = 8
global globalNodeID
globalNodeID = 0
partList = [0 for i in range(N)]
nodeDict = {}
leafDict = {}

class treenode(object):
    """docstring for ClassName"""
    def __init__(self, partID, nodeID, priorID, order):
        #super(ClassName, self).__init__()
        self.isLeaf = False # true/false
        self.partID = partID
        self.nodeID = nodeID
        self.priorID = priorID
        self.order = order 
        self.nextNode = {}
def getCandidate(node):
    pathStr = getPath(node)
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
    pathTem = pathStr[::-1]
    #pathStr.reverse() # reverse string
    idx = 0
    for i in range(len(pathTem)):
        if pathTem[i] == 'S' or pathTem[i] == 'C':
            idx = i
    #pathStr.reverse()
    pathDict['partID'].append(int(pathStr[-idx:]))

    return pathDict

def getPath(node):
    # return path = {'partID':[0,3,5,7],'edge':[S,C,S,...]}
    if node.priorID == -1:
        return str(node.partID)
    else:
        priorNode = nodeDict[node.priorID]
        edgeType = priorNode.nextNodes[node.partID]
        if priorNode.order == 1: # back to root
            return str(priorNode.partID) 
        else:
            return getPath() + edgeType + str(priorNode.partID) 

def buildTree(node):
    # node is not leaf
    candidate = getCandidate(node) # 没出现在path上的partID
    for partID in candidate:
        if partID < node.partID: # MIND!!!! here should be part.order < part.order 
            globalNodeID += 1
            subnode = treenode(partID, globalNodeID, node.nodeID, node.order+1);
            globalNodeID += 1
            nodeDict[subnode.nodeID] = subnode # store this node
            node.nextNode[partID] = 'S'
            if node.order+1 < N:# not leaf 
                buildTree(subnode)
            else:
                subnode.isLeaf = True # use for search 
                currentPath = getPath(subnode) # list-type
                leafDict[subnode.nodeID] = currentPath

    for partID in candidate:
        subnode = treenode(partID, globalNodeID, node.nodeID, node.order+1)
        globalNodeID += 1
        nodeDict[subnode.nodeID] = subnode # store this node
        node.nextNode[partID] = 'D'
        if node.order+1 < N:# not leaf 
            buildTree(subnode)
        else:
            subnode.isLeaf = True #
            currentPath = getPath(subnode) # str-type
            leafDict[subnode.nodeID] = currentPath
        break # each node only have one dotted edge

#def __init__(self, partID, nodeID, priorID, order):
rootID = 0 #diyTool.getRoot()
root = sketchTreeNode.node(rootID, globalNodeID, -1, 1)
nodeDict[rootID] = root # store this node
globalNodeID += 1

buildTree(root)






