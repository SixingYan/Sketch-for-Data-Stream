from diyTool import getTwoRandomNum
import numpy as np
class modSketch_parti(object):
    '''add a edge transfer before update'''
    def __init__(self, w, hList, hOutList, PList, nrDict_m):
        self.w = w
        self.hList = hList
        self.hOutList = hOutList # the same for each
        self.hTotal = [self.hList[i]+self.hOutList[i] for i in range(len(self.hList))]
        self.PList = PList
        self.nrDict_m = nrDict_m
        self.modSketch_p = np.zeros(tuple([self.w] + self.hTotal))
        self.mask = [getTwoRandomNum(max(self.PList)) for _ in range(self.w)]

    def getHParti(self, nodeID, hd, rg, wd):
        nodeID = hash(nodeID)
        return (nodeID*self.mask[wd][0] + self.mask[wd][1])% self.PList[hd]% (rg[1]-rg[0]) + rg[0]

    def getH(self, nodeID, hd, wd):
        nodeID = hash(nodeID)
        return (nodeID*self.mask[wd][0] + self.mask[wd][1])% self.PList[hd]% self.hOutList[hd] + self.hList[hd]

    def getHash(self, edge):
        hashValue = [[] for _ in range(self.w)]
        for i in range(len(edge)):
            if edge[i] in self.nrDict_m[i].keys():
                rg = self.nrDict_m[i][edge[i]]
                for wd in range(self.w):
                    hv = self.getHParti(edge[i], i, rg, wd)
                    hashValue[wd].append(hv)
            else:
                for wd in range(self.w):
                    hv = self.getH(edge[i], i, wd)
                    hashValue[wd].append(hv)
        return hashValue
    
    def update(self, edge, freq=1):
        hashValue = self.getHash(edge)
        for wDimension, hashList in zip(self.modSketch_p, hashValue):
            wDimension[tuple(hashList)] += freq
        
    def query(self, edge):
        hashValue = self.getHash(edge)
        return min(wDimension[tuple(hashList)] for wDimension, hashList in zip(self.modSketch_p, hashValue))