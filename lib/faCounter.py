"""
Misra-Gries Frequency Counter work for flat stream
"""
class faCounter(object):
    def __init__(self, l):  
        #
        self.idx = 0 # index in the window
        self.k = 1 # no. of window
        self.length = l
        self.cKey = ['' for _ in range(self.length)]
        self.cFreq = [0 for _ in range(self.length)]

    def update(self, item, f=1):
        # counter is full or not
        if item in self.cKey:
            key = self.cKey.index(item)
            self.cFreq[key] += f
        else:
            if '' in self.cKey:
                updateIdx = self.cKey.index('')
                self.cFreq[updateIdx] = self.k
                self.cKey[updateIdx] = item
            else:
                if f > min(self.cFreq):
                    minIdx = self.cFreq.index(min(self.cFreq))
                    self.cFreq[minIdx] = f
                    self.cKey[minIdx] = item

        self.idx += 1

        if self.idx == self.length:
            #clean
            for i in range(self.length):
                if self.cFreq[i] < (self.k + 1):
                    self.cFreq[i] = 0
                    self.cKey[i] = ''

            self.k += 1
            self.idx = 0
    
    def query(self,item):
        #
        if itme in self.cKey:
            return True
        else:
            return False