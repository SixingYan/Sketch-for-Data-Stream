

import sketchTreeNode as tn
import diyTool
import 
[]
'''

return best path

最后一段edge, 最小的那个最好


global tree 中途不计算边
先建树, 不用算cost, 然后得到了leaf后回溯path
后搜索



path = {'partID':[0,3,5,7],'edge':[0,1,0,...]}

'''
globalNodeID = 0
nodeDict = {} # 'nodeID':node
leafDict = {} # 'nodeID':[pathNodeList,cost]  pathNodeList = [N]


def f():
    #
    pass
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
    minCost,bestPathList = searchBest()
    print(minCost)
    printPath(bestPathList)

if __name__ == '__main__':
    main()
