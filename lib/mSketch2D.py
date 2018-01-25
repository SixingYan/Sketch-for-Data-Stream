import numpy as np
#from lib.diyTool import get_Prime, getTwoRandomNum
from diyTool import get_Prime, getTwoRandomNum
'''
Given m parts stream
'''
def combineIDs(nodeList):
    newEdgeID = ''
    for i in range(len(nodeList)):
        if len(str(nodeList[i][0])) < len(str(nodeList[i][1])):
            num = len(str(nodeList[i][1]))-len(str(nodeList[i][0]))
            newID = '0'*num + str(nodeList[i][0])
        else:
            newID = str(nodeList[i][0])
        newEdgeID += newID
    return int(newEdgeID) #int

class mSketch2D(object):
    def __init__(self, maxIDList, hList, w,h, sg):  # 255255255255 255255255255255
        self.n = len(sg)
        self.sg = sg # [(1,3),(2,5),(4)...] the parts to be combined start by 0!!!
        self.maxIDList = maxIDList
        self.PList = []#[get_Prime(i) for i in self.maxIDList]
        self.hList = hList # h13, h25, h4 ...  
        self.w = w
        self.h = h
        self.mSketch2D = [[0 for _ in range(self.h**self.n)] for _ in range(self.w)]
        self.mask = []

    def buildSketch(self):
        #
        for mx in self.maxIDList:
            self.PList.append(get_Prime(int(mx)))
        self.mask = [getTwoRandomNum(max(self.PList)) for _ in range(self.w)]

    def getH(self, edgeList):
        #
        for m in self.mask:
            finalH = 0
            a, b = m[0], m[1]
            for i in len(edgeList):
                itemH = 0
                if len()>1:
                    tID = combineIDs(edgeList[i]) 
                    tID = hash(tID)
                else:
                    tID = hash(edgeList[i])
                itemH = (a * tID + b) % self.PList[i] % self.hList[i]
                for j in range(i,len(self.hList)):
                    itemH *= self.hList[j]
                finalH += itemH
            yield finalH

    def trafEdge(self, edge):
        #
        newEdge = [] # (),(),()....
        for tp in self.sg:
            if not len(tp) >1:
                eid = edge[tp[0]]
            else:
                nodeList = []
                for i in tp:
                    nodeList.append([edge[i], self.maxIDList[i]])
                eid = combineIDs(nodeList)
            newEdge.append(eid)
        return newEdge
    
    def getEdge(self, edge):
        # release all the parts
        s, t = edge #sourceNode, destinationNode
        e = list(s);e.extend(list(t))
        return e

    def update(self, edge, f=1):
        #input: ((11,22,33,44),(55,66,77,88)) #sg = (1,3) (2) (4, 5, 6) (7)
        #operate (11,33) (22) (44, 55, 66) (77)
        e = self.getEdge(edge)
        newEdge = self.trafEdge(e) #
        for wIDX in range(self.w):
            hv = self.getH(wIDX)
            self.mSketch2D[wIDX][hv] += f

    def query(self, edge):
        #input: ((11,22,33,44),(55,66,77,88)) #sg = (1,3) (2) (4, 5, 6) (7)
        #operate (11,33) (22) (44, 55, 66) (77)
        e = self.getEdge(edge)
        newEdge = self.trafEdge(e)
        return min(wDimension[p] for wDimension, p in zip(self.mSketch2D, self.getH(newEdge)))
