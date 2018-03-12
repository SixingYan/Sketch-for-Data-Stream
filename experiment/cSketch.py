# -*- coding: utf-8 -*-
from diyTool import getTwoRandomNum

def generateEdgeID(s, t, P):
    if len(str(t)) < len(str(P))/2:
        num = int(len(str(P))/2)-len(str(t))
        tStr = '0' * num + str(t)
        return str(s)+tStr
    else:
        return int(str(s)+str(t))

class sketch(object):
    def __init__(self, w, H, P):
        self.w = w
        self.H = H
        self.cSketch = [ [0 for y in range(self.H)] for x in range(self.w) ]
        self.P = P
        self.mask = [getTwoRandomNum(self.P) for _ in range(self.w)]

    def get_hash(self, edge):
        i = hash(edge)
        for m in self.mask:
            a, b = m[0], m[1]
            yield (i * a + b) % self.P % (self.H)

    def update(self, edge, f=1):
        # edge(i,j) = (x, y) a tuple, x is source, y is destination
        source, destination = edge #sourceNode, destinationNode
        edgeID = generateEdgeID(source,destination,self.P)
        for wD, p in zip(range(self.w), self.get_hash(edgeID)):
            self.cSketch[wD][p] += f

    def query(self, edge):
        source, destination = edge
        edgeID = generateEdgeID(source,destination,self.P)
        return min(wDimension[p] for wDimension, p in zip(self.cSketch, self.get_hash(edgeID)))

