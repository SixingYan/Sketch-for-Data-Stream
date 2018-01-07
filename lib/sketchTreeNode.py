#
#
# partID nodeID
# edgeType = 'C'/'S'
class node(object):
    """docstring for ClassName"""
    def __init__(self, partID, nodeID, priorID, order):
        #super(ClassName, self).__init__()
        self.isLeaf = False # true/false
        self.partID = partID
        self.nodeID = nodeID
        self.priorID = priorID
        self.order = order 
        self.nextNode = {}

    def function(self, ):
        pass
def getPathDict(pathStr):
    # input a string 
    pathDict = {'partID':[],'edgeType':[]}
    preIndex = 0
    for i in range(len(pathStr)):
        if pathStr[i] == 'S' or pathStr[i] == 'C':
            pathDict['partID'].append(int(pathStr[preIndex:i]))
            if pathStr[i] == 'S':
                pathDict['edgeType'].append(0)
            else:
                pathDict['edgeType'].append(1)
            preIndex = i + 1
    pathStr.reverse() # reverse string
    idx = 0
    for i in range(len(pathStr)):
        if pathStr[i] == 'S' or pathStr[i] == 'C':
            idx = i
    pathStr.reverse()
    pathDict['partID'].append(int(pathStr[-idx:]))
    return pathDict

def callSketch(pathStr):
    #

    getStrategy()

    #
    get
    return 



def getStrategy(pathDict):
    # edge=0 seperate  edge=1 combine 
    j = 0
    strategy = []#[[],...[]]
    for i in range(len(pathDict['partID'])):
        if i == len(pathDict['partID'])-1:
            continue
        if i == 0:
            strategy.append([])
            strategy[j].append(pathDict['partID'][i])
        edge = pathDict['edge'][i]
        if edge == 1:
            strategy[j].append(pathDict['partID'][i+1])
        else:
            strategy.append([])
            j += 1
            strategy[j].append(pathDict['partID'][i+1])
    return strategy    

def printPath(pathList):
    # print
    pass


def getRoot():
    return partID



























