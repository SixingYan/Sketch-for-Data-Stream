import numpy as np
from lib.diyTool import get_Prime, getTwoRandomNum
'''
Given m parts stream
'''
class mGMatrix(object):
    """docstring for ClassName"""
    def __init__(self, maxID, h, w, n):
        self.maxIDList = maxIDList
        self.PList = [get_Prime(mx) for mx in self.maxIDList]
        self.h = h
        self.n = n
        self.w = w
        self.mGMatrix = np.zeros(tuple([self.w]+[h for _ in range(self.n)]))
        self.mask = [getTwoRandomNum(self.P) for _ in range(self.w)]

    def getH(self, node, idx, wd):
        i = hash(node)
        #for m in self.mask:
        a, b = self.mask[wd][0], self.mask[wd][1]
        return (i * a + b) % self.PList[idx] % self.h

    def update(self, edge, f=1):
        #((1,2,3,4),(1,2,3,4))
        #s, t = edge #sourceNode, destinationNode
        for wd in range(self.w):
            hv = []
            for idx in range(len(edge)):
                hv.append(self.getH(edge[idx], idx, wd))
            self.mGMatrix[wd][tuple(hv)] += f
        #for wDimension,s1,s2,s3,s4,t1,t2,t3,t4 in zip(self.mGMatrix,self.getH(s[0]),self.getH(s[1]),self.getH(s[2]),self.getH(s[3]),self.getH(t[0]),self.getH(t[1]),self.getH(t[2]),self.getH(t[3])):
        #    wDimension[s1][s2][s3][s4][t1][t2][t3][t4] += f

    def query(self, edge):
        #s, t = edge #sourceNode, destinationNode
        candidate = []
        for wd in range(self.w):
            hv = []
            for idx in range(len(edge)):
                hv.append(self.getH(edge[idx], idx, wd))
            candidate.append(self.mGMatrix[wd][tuple(hv)])
        return min(candidate)
        #return min(wDimension[s1][s2][s3][s4][t1][t2][t3][t4] for wDimension,s1,s2,s3,s4,t1,t2,t3,t4 in zip(self.mGMatrix,self.getH(s[0]),self.getH(s[1]),self.getH(s[2]),self.getH(s[3]),self.getH(t[0]),self.getH(t[1]),self.getH(t[2]),self.getH(t[3])))