# -*- coding: utf-8 -*-
import lib
import lib.mSketch as mSketch
import lib.sketchTreeNode as tn

def buildTree(node):
    global globalNodeID
    candidate = tn.getCandidate(node) # 没出现在path上的partID
    for partID in candidate:
        if partID < node.partID: # MIND!!!! here should be part.order < part.order 
            subnode = tn.treenode(partID, globalNodeID, node.nodeID, node.order+1);
            globalNodeID += 1
            nodeDict[subnode.nodeID] = subnode # store this node
            node.nextNodes[subnode.nodeID] = 'C' # 因为part ID 不唯一
            if subnode.order < N:# not leaf 
                buildTree(subnode)
            else:
                subnode.isLeaf = True # use for search 
                currentPath = tn.getPath(subnode) # list-type
                leafDict[subnode.nodeID] = currentPath
    #for partID in candidate:
    subnode = tn.treenode(max(candidate), globalNodeID, node.nodeID, node.order+1)
    globalNodeID += 1
    nodeDict[subnode.nodeID] = subnode # store this node
    node.nextNodes[subnode.nodeID] = 'S'
    if subnode.order < N:# not leaf 
        buildTree(subnode)
    else:
        subnode.order  = True #
        currentPath = tn.getPath(subnode) # str-type
        leafDict[subnode.nodeID] = currentPath



w = 10
h = 50
n = 4
maxIDList = [255 for i in range(n)]
hList = [h for i in range(n)]
globalNodeID = 0

pathNum = []


    globalNodeID = 0
    N = num
    globalNodeID = 0
    partList = [i for i in range(N)]
    nodeDict = {}
    leafDict = {}
    rootID = max(partList) #diyTool.getRoot()
    root = tn.treenode(rootID, globalNodeID, -1, 1)
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



'''
人工找到最佳的结构
2 个数据集
get sketch
open stream
judge sketch
'''
















