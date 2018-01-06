









class mSketch(object):
    """docstring for ClassName"""
    def __init__(self, arg):
        #super(ClassName, self).__init__()
        self.arg = arg
        self.maxID = maxID
        self.strategy = strategy
        self.weight = weight 
        self.mSketch = [[] for _ in range(len(self.strategy))]
        self.P = P
        self.PList = self.getPList()
        self.h = h
        self.hNum = hNum
        self.hList = getHList()

    def getPList(self):
        P_List = []
        for i in range(len(self.strategy)):
            newMaxID = str(self.maxID) * len(self.strategy[i])
            newMaxID = str(newMaxID)
            PNum = get_Prime(newMaxID)
            P_List.append(PNum)
        return P_List

    def getHList():
        h_List = []
        k = np.sqrt(((self.h ** self.hNum)/LianCheng(self.weight)), self.hNum)
        for i in range(hNum):
            h_List.append(self.h * self.weight[i] * k)
        return h_List