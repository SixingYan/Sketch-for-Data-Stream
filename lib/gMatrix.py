# -*- coding: utf-8 -*-
from random import randint
from numpy import array
from math import floor,sqrt
from diyTool import get_Prime, getTwoRandomNum

class sketch(object):

    def __init__(self, w, h, N):
        #第一维是hash方程，意思说，对于(i,j)，第w个hash方程给它的位置是表示[w][i][j]
        self.w = w
        self.h = h
        self.N = N
        self.gMatrix = [ [ [0 for z in range(self.h)] for y in range(self.h)] for x in range(self.w)]
        self.P = get_Prime(self.N)
        self.mask = [getTwoRandomNum(self.P) for _ in range(self.w)]

    def get_hash(self, node):
        i = hash(node)
        for m in self.mask:
            a, b = m[0], m[1]
            yield (i * a + b) % self.P % self.h
            
    def update(self, edge, f=1):
        # edge(i,j) = (x, y) a tuple, x is source, y is destination
        source, destination = edge #sourceNode, destinationNode
        for wDimension, p, q in zip(self.gMatrix, self.get_hash(source), self.get_hash(destination)):
            wDimension[p][q] += f

    def edge_frequency_query(self, edge):
        source, destination = edge
        return min(wDimension[p][q] for wDimension, p, q in zip(self.gMatrix, self.get_hash(source), self.get_hash(destination)))
"""
gM = sketch(7, 8, 13)
for i in range(len(a)):
    f = 1 
    gM.update(a[i],f)

for i in range(len(a)):
    value = gM.edge_frequency_query(a[i])
    if not value == 1:
        print('error')

"""






