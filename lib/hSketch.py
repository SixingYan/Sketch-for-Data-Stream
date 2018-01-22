# -*- coding: utf-8 -*-
#import lib
from diyTool import get_Prime, getTwoRandomNum

class sketch(object):
	def __init__(self, w, h1, h2, N):
		self.w = w
		self.h1 = h1
		self.h2 = h2
		self.N = N
		self.hSketch = [[ [0 for z in range(self.h2)] for y in range(self.h1) ] for x in range(self.w)]
		self.P = get_Prime(self.N)
		self.mask = [getTwoRandomNum(self.P) for _ in range(self.w)]

	def get_hash(self, node, h):
		i = hash(node)
		for m in self.mask:
			a, b = m[0], m[1]
			yield (i * a + b) % self.P % h
		
	def update(self, edge, f=1):
		# edge(i,j) = (x, y) a tuple, x is source, y is destination
		source, destination = edge #sourceNode, destinationNode
		for wDimension, p, q in zip(self.hSketch, self.get_hash(source,self.h1), self.get_hash(destination,self.h2)):
			wDimension[p][q] += f

	def edge_frequency_query(self, edge):
		source, destination = edge
		return min(wDimension[p][q] for wDimension, p, q in zip(self.hSketch, self.get_hash(source,self.h1), self.get_hash(destination,self.h2)))
			

	









