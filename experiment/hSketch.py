# -*- coding: utf-8 -*-
from diyTool import getTwoRandomNum

class sketch(object):
	def __init__(self, w, h1, h2, P):
		self.w = w
		self.h1 = h1
		self.h2 = h2
		self.hSketch = [[ [0 for z in range(self.h2)] for y in range(self.h1) ] for x in range(self.w)]
		self.P = P
		self.mask = [getTwoRandomNum(self.P) for _ in range(self.w)]

	def get_hash(self, node, h):
		i = hash(node)
		for m in self.mask:
			a, b = m[0], m[1]
			yield (i * a + b) % self.P % h
		
	def update(self, edge, f=1):
		s, t = edge
		for wDimension, p, q in zip(self.hSketch, self.get_hash(s,self.h1), self.get_hash(t,self.h2)):
			wDimension[p][q] += f

	def query(self, edge):
		s, t = edge
		return min(wDimension[p][q] for wDimension, p, q in zip(self.hSketch, self.get_hash(s,self.h1), self.get_hash(t,self.h2)))
