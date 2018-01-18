import numpy as np
from lib.diyTool import get_Prime, getTwoRandomNum
'''
Given m parts stream
'''
class mGMatrix(object):
    """docstring for ClassName"""
    def __init__(self, maxID, h, w, n):
        self.maxID = maxID
        self.P = get_Prime(self.maxID)
        self.h = h
        self.n = n
        self.w = w
        self.mGMatrix = np.zeros(tuple([h for i in range(self.h)]+[self.w]))
        self.mask = [getTwoRandomNum(self.P) for _ in range(self.w)]

    def getH(self, node):
        i = hash(node)
        for m in self.mask:
            a, b = m[0], m[1]
            yield (i * a + b) % self.P % self.h

    def update(self, edge, f=1):
        #((1,2,3,4),(1,2,3,4))
        s, t = edge #sourceNode, destinationNode
        for wDimension,s1,s2,s3,s4,t1,t2,t3,t4 in zip(self.mGMatrix,self.getH(s[0]),self.getH(s[1]),self.getH(s[2]),self.getH(s[3]),self.getH(t[0]),self.getH(t[1]),self.getH(t[2]),self.getH(t[3])):
            wDimension[s1][s2][s3][s4][t1][t2][t3][t4] += f

    def query(self, edge):

        return min(wDimension[p][q] for wDimension,s1,s2,s3,s4,t1,t2,t3,t4 in zip(self.mGMatrix,self.getH(s[0]),self.getH(s[1]),self.getH(s[2]),self.getH(s[3]),self.getH(t[0]),self.getH(t[1]),self.getH(t[2]),self.getH(t[3])))