









class mSketch(object):
    """docstring for ClassName"""
    def __init__(self, arg):
        self.maxID = maxID
        self.strategy = strategy # [(),(),...]
        self.weight = weight 
        
        self.P = P
        self.PList = []
        self.h = h
        self.hNum = hNum
        self.hList = []
        self.mSketch = [[[0 for _ in range()] for _ in range(len(self.strategy))] for _ in range(self.w)]
        self.getPList()
        getHList()

    def getPList(self):
        #
        for i in range(len(self.strategy)):
            newMaxID = str(self.maxID) * len(self.strategy[i])
            newMaxID = str(newMaxID)
            PNum = get_Prime(newMaxID)
            self.PList.append(PNum)

    def getHList():
        #
        k = np.sqrt(((self.h ** self.hNum)/LianCheng(self.weight)), self.hNum)
        for i in range(hNum):
            self.hList.append(self.h * self.weight[i] * k)
    
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

    def update():
        #
        edgeList = getNewEdgeID(edgeList)
        for i in range(hNum):
            zip(self.hSketch)
    def query():
        return 