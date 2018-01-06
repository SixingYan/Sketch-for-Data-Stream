

import sketchTreeNode
import diyTool
[]
'''

return best path

最后一段edge, 最小的那个最好



先建树
后搜索
'''
globalNodeID = 0

def buildTree(node):
    # node is not leaf
    candidate = getCandidate() # 没出现在path上的partID
    for partID in candidate:
        if partID < node.partID:
            subnode = sketchTreeNode()
            cost = getCost()
            node.nextNodeEdge((partID,cost,'solid'))
            if :# not leaf 
                buildTree(node)
            else:
                subnode.isLeaf = True # use for search 

    for partID in candidate:
        subnode = sketchTreeNode()
        cost = getCost()
        node.nextNodeEdge((partID,cost,'dotted'))
        if :# not leaf 
            buildTree(candi)
        else:
            subnode.isLeaf = True #
        break

    # 找边

    # 如果边不能再继续了，return ''

    #
    return

def searchBest():
    pass

root = sketchTreeNode(globalNodeID)
globalNodeID += 1

buildTree(root)

searchBest(root)
















