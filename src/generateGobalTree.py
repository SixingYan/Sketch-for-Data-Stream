"""
generateGobalTree
"""

import sketchTreeNode
parthList = [0 for i in range(8)]

def buildTree(node):
    # node is not leaf
    candidate = getCandidate() # 没出现在path上的partID
    for partID in candidate:
        if partID < node.partID: # MIND!!!! here should be part.order < part.order 
            globalNodeID += 1
            subnode = sketchTreeNode(globalNodeID);
            nodeDict[subnode.nodeID] = subnode # store this node
            cost = getCost()
            node.nextNodeEdge((partID,cost,'solid'))
            if :# not leaf 
                buildTree(node)
            else:
                subnode.isLeaf = True # use for search 
                currentPath = getPath() # list-type
                leafDict[subnode.nodeID] = [cost,currentPath]

    for partID in candidate:
        subnode = sketchTreeNode();globalNodeID += 1
        nodeList.append(subnode) # store this node
        cost = getCost()
        node.nextNodeEdge((partID,cost,'dotted'))
        if :# not leaf 
            buildTree(candi)
        else:
            subnode.isLeaf = True #
            currentPath = getPath() # list-type
            leafDict[subnode.nodeID] = [cost,currentPath]
        break # each node only have one dotted edge

def main():
    #def __init__(self, partID, nodeID, priorID, order):
    rootID = 0 #diyTool.getRoot()
    root = sketchTreeNode(globalNodeID, rootID, ,)
    nodeList.append(root) # store this node
    globalNodeID += 1

    buildTree(root)
    minCost,bestPathList = searchBest()
    print(minCost)
    printPath(bestPathList)








