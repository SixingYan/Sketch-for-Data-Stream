# -*- coding: utf-8 -*-
#---private
import hSketch
import gMatrix
import cSketch
from publicTool import savePickle
#---public 
from numpy import std,array
from copy import deepcopy
num = 50
w = 10
h = 500
#maxNodeID = 338239
maxNodeID = 1391333
#maxNodeID = 4213084 
edgeMax = int(str(maxNodeID)+str(maxNodeID))
cS = cSketch.sketch(w,h**2,edgeMax)
gM = gMatrix.sketch(w,h,maxNodeID)
cS1 = deepcopy(cS)
gM1 = deepcopy(gM)
stdList = []

def varCS(sketch):
    #
    total = 0
    for i in range(10):
        var =std(array(sketch[i]))
        total += var
    return total/10

def varGH(sketch):
    total = 0
    for i in range(10):
        temp = []
        for j in range(len(sketch[i])):
            temp.extend(sketch[i][j])
        var = std(array(temp))
        total += var
    return total/10

def getH1H2_(num1,num2,h):
    h1h2List = []
    for i in range(num1,num2):
        h1 = (i+1)
        h2 = int(h**2/h1)
        h1h2List.append((h1,h2))
    return h1h2List

def getH1H2(num,h):
    h1h2List = []
    for i in range(num):
        h1 = (i+1)*20
        h2 = int(h**2/h1)
        h1h2List.append((h1,h2))
    return h1h2List

def experiment1(filename,sketchList,sketchList1):
    countNum = 0;stdList = [];stdList1 = []
    with open(filename, 'r') as f:
        print('-----prepare and update-----')
        for line in f:
            line = line.strip()
            if len(line)>0:
                countNum += 1
                parts = line.split(' ')
                s = int(parts[0]);t = int(parts[1]);freq = float(parts[2])

                cS.update((s,t),freq)
                gM.update((s,t),freq)
                for i in range(len(sketchList)):
                    sketchList[i].update((s,t),freq)

                cS1.update((s,t),1)
                gM1.update((s,t),1)
                for i in range(len(sketchList1)):
                    sketchList1[i].update((s,t),1)
    print()
    print('cs');std = varCS(cS.cSketch)
    print(std)
    result['cS']['value'] = std
    print('gm');std = varGH(gM.gMatrix)
    result['gM']['value'] = std
    print(std)
    for i in range(len(sketchList)):
        print('for %d'%i);std = varGH(sketchList[i].hSketch)
        print(std)
        stdList.append(std)
        
    print()
    print('cs');std = varCS(cS1.cSketch)
    print(std)
    result['cS']['point'] = std
    print('gm');std = varGH(gM1.gMatrix)
    result['gM']['point'] = std
    print(std)
    for i in range(len(sketchList1)):
        print('for %d'%i);std = varGH(sketchList1[i].hSketch)
        print(std)
        stdList1.append(std)
    return stdList,stdList1
    
def expSketch(filename,maxNodeID):
    w = 10;
    h1h2List = getH1H2(num,500)#h=500
    sketchList = []
    for i in range(len(h1h2List)):
        h1,h2 = h1h2List[i]
        print('for %d, h1 is %d   h2 is %d'%(i,h1,h2))
        hS = deepcopy(hSketch.sketch(w,h1,h2,maxNodeID))
        sketchList.append(hS)
    
    sketchList1 = []
    for i in range(len(h1h2List)):
        h1,h2 = h1h2List[i]
        print('for %d, h1 is %d   h2 is %d'%(i,h1,h2))
        hS = deepcopy(hSketch.sketch(w,h1,h2,maxNodeID))
        sketchList1.append(hS)
    stdList,stdList1 = experiment1(filename,sketchList,sketchList1)

    return stdList,stdList1

print('now begin')
result = {'cS':{'value':0,'point':0},'gM':{'value':0,'point':0}}
data = expSketch('D:/google desk PC/graph_freq_comp14.txt',1391333)
savePickle('D:/google desk PC/pickle/stdList_value_comp16',data[0])
savePickle('D:/google desk PC/pickle/stdList_point_comp16',data[1])
savePickle('D:/google desk PC/pickle/result_comp16_std',result)
print(result)