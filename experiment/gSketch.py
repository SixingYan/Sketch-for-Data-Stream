# -*- coding: utf-8 -*-
from diyTool import getTwoRandomNum

class gSketch(object):
    def __init__(self, w, t, h, hOut, P, nrDict):
        self.w = w
        self.h = h
        self.hOut = hOut
        self.P = P
        self.Ptotal = int(str(P)*t)
        self.nrDict = nrDict
        self.gSketch = [[0 for _ in range(self.h)] for _ in range(self.w)] 
        self.outLier = [[0 for _ in range(self.hOut)] for _ in range(self.w)]
        self.mask = [getTwoRandomNum(self.Ptotal) for _ in range(self.w)]
    
    def getHParti(self, edgeID, rg):
        edgeID = hash(edgeID)
        for m in self.mask:
            a, b = m[0], m[1]
            try:
                if (rg[1]-rg[0]) == 0:
                    print('error!')
                    print(nrDict)
            except:
                print('error!!!!')
                print(rg)
            yield (edgeID * a + b) % self.Ptotal % (rg[1]-rg[0]) + rg[0]

    def getH(self, edgeID):
        edgeID = hash(edgeID)
        for m in self.mask:
            a, b = m[0], m[1]
            yield (edgeID * a + b) % self.Ptotal % self.hOut

    def genrEdgeID(self, edge):
        # combine
        edgeID = ''
        pStrLen = len(str(self.P))
        for e in edge:
            eStr = str(e)
            if len(eStr) < pStrLen:
                num = pStrLen-len(eStr)
                eStr = '0' * num + eStr
            edgeID += eStr
        return int(edgeID)

    def query(self, edge):
        edgeID = self.genrEdgeID(edge)
        if edge[0] in self.nrDict.keys():
            rg = self.nrDict[edge[0]]
            return min(wDem[p] for wDem, p in zip(self.gSketch, self.getHParti(edgeID, rg)))
        else:
            return min(wDem[p] for wDem,p in zip(self.outLier, self.getH(edgeID)))
    
    def update(self, edge, freq=1):
        edgeID = self.genrEdgeID(edge)
        if edge[0] in self.nrDict.keys():
            rg = self.nrDict[edge[0]]
            for wDem, p in zip(self.gSketch, self.getHParti(edgeID, rg)):
                wDem[p] += freq
        else:
            for wDem,p in zip(self.outLier, self.getH(edgeID)):
                wDem[p] += freq