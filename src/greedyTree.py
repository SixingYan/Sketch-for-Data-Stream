"""
greedyTree

中途需要计算边

"""
 
N = 

def buildTree(node):
    # node is not leaf
    candidate = getCandidate() # 没出现在path上的partID
    minCost = 0
    bestNode = []

    for partID in candidate:
        if partID < node.partID:
            cost = getCost()
            if cost < minCost:
                minCost = cost
                bestNode = [partID,'solid']

    for partID in candidate:
        cost = getCost()
        if cost < minCost:
            minCost = cost
            bestNode = [partID,'dotted']
        break 
    #def __init__(self, partID, nodeID, priorID, order):        
    globalNodeID += 1
    subnode = sketchTreeNode(bestNode[0], globalNodeID, node.nodeID, node.order+1);
    nodeDict[subnode.nodeID] = subnode # store this node
    node.nextNodeEdge((bestNode[0],minCost,bestNode[1]))
    
    if not subnode.order == N:# not leaf 
        buildTree(node)
    else:
        currentPath = getPath() # dict-type
        leafDict[subnode.nodeID] = [cost,currentPath]

def main():
    rootID = diyTool.getRoot()
    root = sketchTreeNode(globalNodeID, rootID,    ,)
    nodeList.append(root) # store this node
    globalNodeID += 1

    buildTree(root)
    minCost, bestPathList = searchBest()
    print(minCost)
    printPath(bestPathList)

if __name__ == '__main__':
    main()