"""
k-TolerantTree

中途需要计算边

"""


n = 1 # default
def buildTree(node):

    return

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











