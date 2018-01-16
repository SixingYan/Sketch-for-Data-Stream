import numpy as np









class mGMatrix(object):
    """docstring for ClassName"""
    def __init__(self, arg):
        self.maxID = maxID
        self.strategy = strategy # [(),(),...]
        #self.weight = weight 
        self.P = P
        self.PList = PList
        self.h = h
        #self.hNum = hNum
        #self.hList = hList
        self.mGMatrix = np.zeros(tuple([h for i in range(N)]))
        #getPList()
        #getHList()

    
    def getSketch():
        []

        self.mSketch = [deepcopy() for _ in range(self.w) ] 

    def getHash():
        #
        return

    def getNewEdgeID(edge):
        #
        edgeList = []
        for part in self.strategy:
            if len(part) == 1:
                partID = part[0]
                edgeList.append(edge[partID]) 
            else:
                partIDs = [edge[partID] for partID in part]
                newPart = getCombine(partIDs)
                edgeList.append(newPart) 
        return edgeList

    def update(self, edge, f=1):
        #
        edgeList = getNewEdgeID(edgeList)
        for i in range(hNum):
            zip(self.hSketch)
    def query(self, edge):
        return 