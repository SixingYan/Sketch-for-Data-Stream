# -*- coding: utf-8 -*-
from random import randint
import pickle
from math import sqrt



def get_Prime(N):
    # larger than N, the number index of nodes; Ensure N > 2 and N is an integer
    prime = N
    if prime % 2 == 0:
        prime += 1
    while True:
        flag = True
        for num in range(3,int(sqrt(prime))+1):
            if prime%num == 0:
                flag = False
                break
        if flag == False:
            prime += 2
        else:
            break
    return prime

def getTwoRandomNum(P):
    # return tuple (a,b)
    a = randint(1,P-1)
    while True:
        b = randint(1,P-1)
        if not b == a:
            break
    return (a, b)


def savePickle(varName, var):
    varName += '.pickle'
    with open(varName, 'wb') as f:
        pickle.dump(var,f)

def loadPickle(varName):
    with open(varName, 'rb') as f:
        var = pickle.load(f)
    return var