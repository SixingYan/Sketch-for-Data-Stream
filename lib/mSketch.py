import numpy as np
from lib.diyTool import get_Prime, getTwoRandomNum
'''
Given m parts stream
'''
def generateEdgeID(edge,maxID):
    total = ''
    for i in range(len(edge)):
        if len(str(edge[i])) < (len(str(maxID))/len(edge)):
            num = int(len(str(maxID))/len(edge))-len(str(edge[i]))
            nStr = '0' * num + str(edge[i])
            total += nStr
    return int(total)



class mSketch(object):
    """docstring for ClassName"""
    def __init__(self, maxID, hList, w, sg):  # 255255255255 255255255255255
        self.sg = sg # [(1,3),(2,5),(4)...] the parts to be combined start by 0!!!
        self.maxIDList = maxIDList
        self.PList = []#[get_Prime(i) for i in self.maxIDList]
        self.hList = []
        #self.n = n
        self.w = w
        self.mSketch = [] #[[0 for _ in range(self.h**self.n)] for _ in range(self.w)] 
        self.mask = [getTwoRandomNum(self.P) for _ in range(self.w)]

    def buildSketch(self):
        #
        side = [] # [100*700, 600, 500*300]
        for tp in self.sg:
            times = 1
            for i in tp: 
                times *= self.hList[i]
            self.hList.append(times)
            side.append(times)    
        side.append(self.w)    
        self.mSketch = np.zeros(tuple(side))

        for tp in self.sg:
            mx = ''
            for i in tp:
                mx += str(self.maxIDList[i])
            self.PList.append(int(mx))

    def combineIDs(self, nodeList):
        if i in :
            if [i] < self.maxIDList[i]
        pass

    def trafEdge(self, edge):
        #
        for tp in self.sg:
            nodeList = []
            for i in tp:
                edge[i]
                nodeList.append()
            eid = combineIDs(nodeList)
        .append(eid)
        return 

    def getH(self, node, wIDX, P, h):
        #
        i = hash(node)
        a, b = self.mask[wIDX][0], self.mask[wIDX][1]
        return (i * a + b) % P % h

    def update(self, edge, f=1):
        #((1,2,3,4),(1,2,3,4))
        newEdge = trafEdge(edge) # 已经combine了
        for wIDX in range(self.w):
            idx = []
            for i in range(len(newEdge)):
                hv = getH(newEdge[i], wIDX, self.PList[i], self.hList[i])
                idx.append(hv)
            self.mSketch[wIDX][tuple(idx)] += f

    def query(self, edge):
        s, t = edge #sourceNode, destinationNode
        e = list(s);e.extend(list(t))
        edgeID = generateEdgeID(e,self.maxID)
        return min(wDimension[p] for wDimension, p in zip(self.mCSketch, self.getH(edgeID)))