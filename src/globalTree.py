

import sketchTreeNode
import diyTool
import treeTool
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



def get(partList):
    # edge=0 seperate  edge=1 combine 
    j = 0
    strategy = []#[[],...[]]
    for i in range(len(partList['partID'])):
        if i == len(partList['partID'])-1:
            continue
        if i == 0:
            strategy.append([])
            strategy[j].append(partList['partID'][i])
        edge = partList['edge'][i]
        if edge == 1:
            strategy[j].append(partList['partID'][i+1])
        else:
            strategy.append([])
            j += 1
            strategy[j].append(partList['partID'][i+1])
    return cost

def f():
    #
    pass




def buildTree(node):
    # node is not leaf
    candidate = getCandidate() # 没出现在path上的partID
    for partID in candidate:
        if partID < node.partID:
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

def searchBest():
    #
    minCost = 0
    bestPathList = []
    for leafNode in list(leafDict.items()):
        if minCost > leafDict[leafNode][0]:
            minCost = leafDict[leafNode][0]
            bestPathList = leafDict[leafNode][0]
    return minCost,bestPathList

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
