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

class mCSketch(object):
    """docstring for ClassName"""
    def __init__(self, maxID, h, w, n):  # 255255255255 255255255255255
        self.maxID = maxID
        self.P = get_Prime(self.maxID)
        self.h = h
        self.n = n
        self.w = w
        self.mCSketch = [[0 for _ in range(self.h**self.n)] for _ in range(self.w)] 
        self.mask = [getTwoRandomNum(self.P) for _ in range(self.w)]

    def getH(self, node):
        i = hash(node)
        for m in self.mask:
            a, b = m[0], m[1]
            yield (i * a + b) % self.P % self.h

    def update(self, edge, f=1):
        #((1,2,3,4),(1,2,3,4))
        s, t = edge #sourceNode, destinationNode
        e = list(s);e.extend(list(t))
        edgeID = generateEdgeID(e,self.maxID)
        for wD, p in zip(range(self.w), self.getH(edgeID)):
            self.mCSketch[wD][p] += f

    def query(self, edge):
        s, t = edge #sourceNode, destinationNode
        e = list(s);e.extend(list(t))
        edgeID = generateEdgeID(e,self.maxID)
        return min(wDimension[p] for wDimension, p in zip(self.mCSketch, self.getH(edgeID)))