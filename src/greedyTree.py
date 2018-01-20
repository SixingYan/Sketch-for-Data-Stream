"""
greedyTree

中途需要计算边

"""
 
N = 


def buildTree(node):
    global globalNodeID
    currentPath = getPath(node) # list-type
    candidate = getCandidate(node,partList) #
    optEdge = 0
    optPart = 0
    optProf = 0
    for partID in candidate:
        if partID < node.partID: #
            profit = getProfit(partID, currentPath, 'C')
            if profit > optProf:
                optEdge = 'C'
                optPart = partID
                optProf = profit

            profit = getProfit(partID, currentPath, 'S')
            if profit > optProf:
                optEdge = 'S'
                optPart = partID
                optProf = profit


            #subnode = treenode(partID, globalNodeID, node.nodeID, node.order+1);
            #globalNodeID += 1
            #nodeDict[subnode.nodeID] = subnode # store this node
            #node.nextNodes[subnode.nodeID] = 'C' #
            #if subnode.order < N:# not leaf 
            #    buildTree(subnode)
            #else:
            #    subnode.isLeaf = True # use for search 
            #    currentPath = getPath(subnode) # list-type
            #    leafDict[subnode.nodeID] = currentPath
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
