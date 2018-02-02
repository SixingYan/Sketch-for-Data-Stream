"""
Misra-Gries Frequency Counter
"""

class faCounter(object):
    def __init__(self, l):  
        #
        self.idx = 0 # index in the window
        self.k = 1 # no. of window
        self.length = l
        self.cKey = ['' for _ in self.length]
        self.cFreq = [0 for _ in self.length]

    def update(self,item,f=1):
        # counter is full or not
        key = self.cKey.find(item)
        if key > -1:
            self.cKey[key] += f
        else:
            updateIdx = self.cKey.find('') # find the first empty place
            if updateIdx > -1:
                self.cFreq[updateIdx] = self.k
                self.cKey[updateIdx] = item

        self.idx += 1

        if self.idx == self.length:
            #clean
            if i in range(self.length):
                if self.cFreq[i] < (self.k + 1):
                    self.cFreq[i] = 0
                    self.cKey[i] = ''

            self.k += 1
            self.idx = 0
    
    def query(self,item):
        #
        if self.cKey.find(item) > -1:
            return True
        else:
            return False