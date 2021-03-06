import numpy as np
#from lib.diyTool import get_Prime, getTwoRandomNum
from diyTool import get_Prime, getTwoRandomNum
'''
Given m parts stream
'''
def combineIDs(nodeList,maxValue):
    newEdgeID = ''
    for i in range(len(nodeList)):
        if len(str(nodeList[i])) < int(len(str(maxValue))/len(nodeList)):
            num = int(len(str(maxValue))/len(nodeList))-len(str(nodeList[i]))
            newID = '0'*num + str(nodeList[i])
        else:
            newID = str(nodeList[i])
        newEdgeID += newID
    return int(newEdgeID) #int

class mSketch2D(object):
    def __init__(self, maxIDList, hList, w,h, sg, n):  # 255255255255 255255255255255
        self.n = n
        self.sg = sg # [(1,3),(2,5),(4)...] the parts to be combined start by 0!!!
        self.maxIDList = maxIDList
        self.PList = [] #[get_Prime(i) for i in self.maxIDList]
        self.hList = hList # h13, h25, h4 ...  
        self.w = w
        self.h = h
        self.mask = []

    def buildSketch(self):
        #
        for mx in self.maxIDList:
            self.PList.append(get_Prime(int(mx)))
        self.mask = [getTwoRandomNum(max(self.PList)) for _ in range(self.w)]
        tH = 1
        for hL in self.hList:
            tH *= hL
        self.mSketch2D = [[0 for _ in range(tH)] for _ in range(self.w)]

    def getH(self, edgeList):
        #
        for m in self.mask:
            finalH = 0
            a, b = m[0], m[1]
            for i in range(len(edgeList)):
                tID = edgeList[i]
                itemH = (a * tID + b) % self.PList[i] % self.hList[i]
                if not i == len(edgeList)-1:
                    for j in range(i+1,len(self.hList)):
                        itemH *= self.hList[j]
                finalH += itemH
            yield finalH

    def trafEdge(self, edge):
        #
        #print(edge)
        #print(self.sg)
        newEdge = [] # (),(),()....
        for j in range(len(self.sg)):
            tp = self.sg[j]
            #print('tp is '+str(tp))
            if not len(tp) >1:
                eid = edge[tp[0]]
            else:
                nodeList = []
                for i in tp:
                    nodeList.append(edge[i])
                eid = combineIDs(nodeList,self.maxIDList[j])
            newEdge.append(eid)
        return newEdge
    
    def getEdge(self, edge):
        # deleted!
        # release all the parts
        s, t = edge #sourceNode, destinationNode
        e = list(s);e.extend(list(t))
        return e

    def update(self, edge, f=1):
        #input: ((11,22,33,44),(55,66,77,88)) #sg = (1,3) (2) (4, 5, 6) (7)
        #operate (11,33) (22) (44, 55, 66) (77)
        e = edge #self.getEdge(edge)
        newEdge = self.trafEdge(e) #
        for wD, p in zip(range(self.w), self.getH(newEdge)):
            #print(p)
            self.mSketch2D[wD][p] += f

    def query(self, edge):
        #input: ((11,22,33,44),(55,66,77,88)) #sg = (1,3) (2) (4, 5, 6) (7)
        #operate (11,33) (22) (44, 55, 66) (77)
        e = edge #self.getEdge(edge)
        newEdge = self.trafEdge(e)
        return min(wDimension[p] for wDimension, p in zip(self.mSketch2D, self.getH(newEdge)))
