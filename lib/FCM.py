"""
input:
    1. strategy: decide which part to be combine, use for update and query 
    2. hList: lenght to compress each part (group)

process:
    1. build the structure following he strategy
    2. maxIDlist: generate new maxIDlist based on maxID of each part and the strategy 
    3. PList: follow the new maxIDList to generate the prime number set
"""


getTwoRandomNum as getTRN



def combineIDs(nodeList,maxVList):
    # 
    newEdgeID = ''
    for i in range(len(nodeList)):
        if len(str(nodeList[i])) < int(len(str(maxValue))/len(nodeList)):
            num = int(len(str(maxValue))/len(nodeList))-len(str(nodeList[i]))
            newID = '0'*num + str(nodeList[i])
        else:
            newID = str(nodeList[i])
        newEdgeID += newID
    return int(newEdgeID) #int

class fMODsketch(object):
    def __init__(self, rawMaxIDList, hList, w,hw,lw, sg):  # 255255255255 255255255255255
        #
        self.sg = sg # [(1,3),(2,5),(4)...] the parts to be combined start by 0!!!
        self.rawMaxIDList = rawMaxIDList # 255,255,255,255,....
        self.maxIDList = []
        self.PList = []#[get_Prime(i) for i in self.maxIDList]
        self.hList = hList
        self.w = w
        self.wAvg = []
        self.wList = [lw,hw]
        self.mSketch = [] #[[0 for _ in range(self.h**self.n)] for _ in range(self.w)] 
        self.mask = []
        self.totalPrime = 0
    def buildSketch(self):
        #
        self.mSketch = np.zeros(tuple(side))
        self.mask = [[getTRN(self.PList[i]) for i in range(len(self.PList))] for _ in range(self.w)]
        self.totalPrime = 

    def function(self, mIdx, nodeList, idx):
        #
        a, b = self.mask[mIdx][0], self.mask[mIdx][1]
        finalH = 0
        for i in range(len(nodeList)):
            tID = nodeList[i]
            itemH = (a * tID + b) % self.PList[i] % self.hList[i]
            if not i == len(nodeList)-1: # if it is not the last one
                for j in range(i+1,len(self.hList)):
                    itemH *= self.hList[j]
            finalH += itemH
        return finalH

    def offsetGap(self, nodeList, idx):
        # offset and gab are determined by node value
        # 
        #i = hash(node)
        # the front part is similar to getHash

        a = self.mask[w][idx][0]
        b = self.mask[w][idx][1]
        (i*a + b) % self.PList[idx]

        ident = self.combineIDs(nodeList)

        offset = (ident * a + b)% self.totalPrime% self.w
        gap =  (ident * a + b)% self.totalPrime% self.wList[flag] # not longger than h/3
        
        return offset, gap
    
    def update(self,flag,edge,f=1):
        # flag \in {0,1}, 0 = low, 1 = high
        
        e = transfer
        offset, gap = self.offsetGap()
        for i in range(self.wList[flag]):

            hv = self.getH(e)
            hIdx
            


            [(offset + gap*i) % self.w][tuple(hIdx)] += f

    def query():

        pass

