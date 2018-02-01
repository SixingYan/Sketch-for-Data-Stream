"""
Misra-Gries Frequency Counter
"""
from diyTool import getTwoRandomNum as getTRN
from diyTool import get_Prime
import numpy as np

class faCounter(object):
    def __init__(self, rawMaxIDList, hList, w,hw,lw, sg):  # 255255255255 255255255255255
        #
        self.idx = 0
        self.length = l
        self.cKey = [0 for _ in self.length]
        self.cItem = [0 for _ in self.length]



        self.sg = sg # [[1,3],[2,5],[4]...] the parts to be combined start by 0!!!
        self.rawMaxIDList = rawMaxIDList # 255,255,255,255,....
        self.w = w
        self.wList = [lw,hw]
        self.hList = hList # already combine
        self.maxIDList = [] #
        self.PList = []
        self.wAgg = 0
        self.wNum = 0
        self.mSketch = []
        self.mask = []
        self.maskLH = []
        self.totalPrime = 0


    def update(self,item,f=1):
        if counter
        
        self.idx += 1






    def buildSketch(self):
        #
        #1. mSketch
        side = [self.w] # [10, 100*700, 600, 500*300] #the first is w
        for h in self.hList:
            side.append(h)
        self.mSketch = np.zeros(tuple(side))
        #2. mask
        self.mask = [[getTRN(self.PList[i]) for i in range(len(self.PList))] for _ in range(self.w)]
        #3. sg
        for tp in self.sg:
            if not len(tp) > 1:
                self.maxIDList.append(self.rawMaxIDList[tp[0]])
            else:
                total = ''
                for i in tp:
                    total += str(self.rawMaxIDList[i])
                self.maxIDList.append(int(total))
        #4. totalPrime
        totalMax = ''
        for mn in self.rawMaxIDList:
            totalMax += str(mn)
        self.totalPrime = get_Prime(int(totalMax))
        #5. maskLH
        self.maskLH = [getTRN(self.totalPrime) for _ in range(2)]
    
    def getH(self, wIdx, nodeList):
        #
        a, b = self.mask[wIdx][0], self.mask[wIdx][1]
        finalH = []
        for i in range(len(nodeList)):
            node = nodeList[i]
            n = hash(node)
            hv = (a*n + b) % self.PList[i] % self.hList[i]
            finalH.append(hv)
        return finalH

    def combineIDs(self,nodeList, maxIDList):
        number = ''
        for i in range(len):
            newNum = ''
            if len(str(nodeList[i])) < len(str(maxIDList[i])):
                num = len(str(maxIDList[i])) - len(str(nodeList[i]))
                newNum = '0'*num + str(nodeList[i])
            else:
                newNum = str(nodeList[i])
            number += newNum
        return int(number)

    def offsetGap(self, flag, nodeList):
        # offset and gab are determined by node value
        # the front part is similar to getHash
        a,b = self.maskLH[flag][0],self.maskLH[flag][1]
        ident = self.combineIDs(nodeList, self.maxIDList)
        offset = (ident*a + b)% self.totalPrime% self.w
        gap =  (ident*a + b)% self.totalPrime% self.wList[flag] # not longger than h/3
        return offset, gap

    def transfer(self,edge):
        newEdge = []
        for j in range(len(self.sg)):
            tp = self.sg[j]
            if not len(tp) >1:
                eid =  edge[tp[0]]
            else:
                nodeList = []
                maxList = []
                for i in tp:
                    nodeList.append(edge[i])
                    maxList.append(self.rawMaxIDList[i])
                eid = self.combineIDs(nodeList,maxList)
            newEdge.append(eid)
        return newEdge

    def update(self,flag,edge,f=1):
        # flag \in {0,1}, 0 = low, 1 = high
        #1. prepare
        nodeList = self.transfer(edge)
        offset, gap = self.offsetGap(flag,nodeList)
        #2. hash and update
        for i in range(self.wList[flag]):
            wIdx = (offset + gap*i) % self.w # round-robin 
            finalH = self.getH(wIdx, nodeList)
            self.mSketch[wIdx][tuple(finalH)] += f
        #3. track the average w
        self.wAgg += self.wList[flag]
        self.wNum += 1

    def query(self,):
        #
        #1. prepare
        nodeList = self.transfer(edge)
        offset, gap = self.offsetGap(flag,nodeList)
        w = self.wAgg/self.wNum
        #2. search
        resultList = []
        for i in range(self.wList[flag]):
            wIdx = (offset + gap*i) % self.w # round-robin 
            finalH = self.getH(wIdx, nodeList)
            f = self.mSketch[wIdx][tuple(finalH)]
            resultList.append(f)
        return min(resultList)