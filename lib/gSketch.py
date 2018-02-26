class gSketch(object):
    """docstring for gSketch"""
    def __init__(self, arg):
        #super(gSketch, self).__init__()
        self.arg = arg

    def hashPartition(node):
        val = hash(node)
        hw = hwDict[val]
        hv = i % P % hw

        idx = hv
        for i in range(hwList.find(hw)):
            idx += hwList[i]
        return idx

    def query(self, edge):
        for i in range(len(edge)):
            if edge[i] in edge.keys():
                
        return

    def update(self, edge, freq=1):
        # all hash partition
        for i in range(len(edge)):
            edge[i]

            if edge[i] in edge.keys():
                for node in edge[i]:
                    hashPartition(node)
            else:
