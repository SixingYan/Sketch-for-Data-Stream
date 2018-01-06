#
#
# partID nodeID

class node(object):
    """docstring for ClassName"""
    def __init__(self, partID, nodeID, priorID, order):
        #super(ClassName, self).__init__()
        self.isLeaf = False # true/false
        self.partID = partID
        self.nodeID = nodeID
        self.priorID = priorID
        self.order = order 
        self.nextNode = []
        
    def function(self, ):
        pass
def getPath():
    # return nodelist of path
    return 

def getCost(node,subnode,edgeType):
    #
    preList = getPath()

    return cost

def getCandidate(node):
    return

def getStrategy(partList):
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
    return strategy    

def printPath(pathList):
    # print
    pass































