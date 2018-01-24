# -*- coding: utf-8 -*-
import copy
import random
import mSketch
dataPath = '/data1/Sixing/Stream dataset/ipv4_st_2'

class treenode(object):
    def __init__(self, partID, nodeID, priorID, order):
        self.isLeaf = False # true/false
        self.partID = partID
        self.nodeID = nodeID
        self.priorID = priorID
        self.order = order 
        self.nextNodes = {} # key is node ID

def getCandidate(node,partList):
    pathStr = getPath(node)
    #print('obtaining path '+pathStr)
    pd = getPathDict(pathStr)
    return list(set(partList) - set(pd['partID']))

def getPathDict(pathStr):
    # input a string 
    pathDict = {}
    pathDict['partID'] = []
    pathDict['edgeType'] = []
    preIndex = 0
    for i in range(len(pathStr)):
        if pathStr[i] == 'S' or pathStr[i] == 'C':
            pathDict['partID'].append(int(pathStr[preIndex:i]))
            if pathStr[i] == 'S':
                pathDict['edgeType'].append(0)
            else:
                pathDict['edgeType'].append(1)
            preIndex = i + 1
    pathTem = pathStr[::-1]# reverse string
    idx = 0
    #print(pathTem)
    for i in range(len(pathTem)):
        if pathTem[i] == 'S' or pathTem[i] == 'C':
            idx = i
            break
    pathDict['partID'].append(int(pathStr[-idx:]))
    return pathDict

def getPath(node):
    # return path = {'partID':[0,3,5,7],'edge':[S,C,S,...]}
    if node.priorID == -1:
        #print('getting root')
        return str(node.partID)
    else:
        priorNode = nodeDict[node.priorID]
        edgeType = priorNode.nextNodes[node.nodeID]
        return getPath(priorNode) + edgeType + str(node.partID) 

def getStrategy(pathDict):
    # edge=0 seperate  edge=1 combine 
    j = 0
    strategy = []#[[],...[]]
    for i in range(len(pathDict['partID'])):
        if i == len(pathDict['partID'])-1:
            continue
        if i == 0:
            strategy.append([])
            strategy[j].append(pathDict['partID'][i])
        edge = pathDict['edgeType'][i]
        if edge == 1:
            strategy[j].append(pathDict['partID'][i+1])
        else:
            strategy.append([])
            j += 1
            strategy[j].append(pathDict['partID'][i+1])
    return strategy

def buildTree(node):
    global globalNodeID
    candidate = getCandidate(node,partList) #
    for partID in candidate:
        if partID < node.partID: #
            subnode = treenode(partID, globalNodeID, node.nodeID, node.order+1);
            globalNodeID += 1
            nodeDict[subnode.nodeID] = subnode # store this node
            node.nextNodes[subnode.nodeID] = 'C' #
            if subnode.order < N:# not leaf 
                buildTree(subnode)
            else:
                subnode.isLeaf = True # use for search 
                currentPath = getPath(subnode) # list-type
                leafDict[subnode.nodeID] = currentPath
    #for partID in candidate:
    subnode = treenode(max(candidate), globalNodeID, node.nodeID, node.order+1)
    globalNodeID += 1
    nodeDict[subnode.nodeID] = subnode # store this node
    node.nextNodes[subnode.nodeID] = 'S'
    if subnode.order < N:# not leaf 
        buildTree(subnode)
    else:
        subnode.order  = True #
        currentPath = getPath(subnode) # str-type
        leafDict[subnode.nodeID] = currentPath

def evaluate_top_sum(sketch,topList):
    totalLoss1 = 0;totalFreq1 = 0
    for parts in topList:
        edge = parts[0]; freq = parts[1]
        estiValue = sketch.query(edge)
        totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
    ObservedError = totalLoss1/totalFreq1
    #print('ObservedError is '+str(ObservedError))
    return ObservedError

def evaluate_rad_sum(sketch,radList):
    #
    ObservedError = 0
    for i in range(len(radList)):
        totalLoss1 = 0;totalFreq1 = 0
        for parts in radList[i]:
            edge = parts[0]; freq = parts[1]
            estiValue = sketch.query(edge)
            totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
        ObservedError += totalLoss1/totalFreq1
    #print('ObservedError is '+str(ObservedError/len(radList)))
    return ObservedError/len(radList)    

def getRadList(num,radPool):
    radList = [[] for i in range(5)]
    for i in range(len(radList)):
        while len(radList[i]) < num:
            tem = random.choice(radPool)
            if tem not in radList[i]:
                radList[i].append(tem)
    return radList


w = 10
h = 25
N = 4
maxIDList = [255 for i in range(N)]
hList = [h for i in range(N)]
globalNodeID = 0
partList = [i for i in range(N)]
nodeDict = {}
leafDict = {}

rootID = max(partList) #diyTool.getRoot()
root = treenode(rootID, globalNodeID, -1, 1)
nodeDict[globalNodeID] = root # store this node
globalNodeID += 1
buildTree(root)

print('preparing sketch')
sketchList = []
strategy = []
for ky in list(leafDict.keys()):
    pathStr = leafDict[ky]
    strategy.append(pathStr)
    d = getPathDict(pathStr)
    stra = getStrategy(d)
    sketch = copy.deepcopy(mSketch.mSketch(maxIDList,hList,w,stra))
    sketch.buildSketch()
    sketchList.append(sketch)

countNum = 0
radPool = []
top5000List = []
print('streaming begin')
with open(dataPath,'r') as f:
    #for line in f:
    for line in f.readlines():
        line = line.strip()
        if not len(line)>0:
            continue
        countNum += 1
        if countNum % 1000000 == 0:
            print('now is '+str(countNum))
        
        parts = line.split(' ')
        edge = [int(i) for i in parts[:4]]
        edge = ((edge[0],edge[1]),(edge[2],edge[3]))
        freq = float(parts[4])

        if random.randint(0,1) > 0.9:
            continue
        # get rad and top
        if random.randint(0,1)< 0.3:
            radPool.append([edge,freq])
                
        if len(top5000List)>5000:
            minV = min(top5000List, key=lambda x: x[1])
            if freq>minV[1]:
                indx = top5000List.index(minV);
                top5000List[indx] = [edge,freq]
        else:
            top5000List.append([edge,freq])

        # update 
        for i in range(len(sketchList)):
            sketchList[i].update(edge,freq)

print('========evaluation')# evaluation
topNum = [100,500,1000,2000,5000] 
radNum = [500,1000,2000,5000,10000]
#top5000List = getTopList(ds[2])
topList = []; radList = []
top5000List.sort(key= lambda d : d[1], reverse = True)
for i in range(len(topNum)):
    topList.append(top5000List[:topNum[i]])
    radList.append(getRadList(radNum[i],radPool))
del radPool # clean

print('start top')
# topList
print('----------top')# random
topDict = {}
for j in range(len(topList)): # 5
    top_sum = []
    print('============now is '+str(topNum[j]))
    for i in range(len(sketchList)): #
        ObservedError = evaluate_top_sum(sketchList[i],topList[j]);top_sum.append([strategy[i],int(ObservedError)])
        print()
    top_sum.sort(key= lambda d : d[1], reverse = False)
    print('========the order is '+str(top_sum))
    topDict[topNum[j]] = top_sum
    print()

print('start rad')
# topList
print('----------rad')# random    
radDict = {}    
for j in range(len(radList)): # 5
    rad_sum = []
    print('============now is '+str(topNum[j]))
    for i in range(len(sketchList)): #
        ObservedError = evaluate_rad_sum(sketchList[i],radList[j]);rad_sum.append([strategy[i],ObservedError])
    rad_sum.sort(key= lambda d : d[1], reverse = False)
    print('========the order is '+str(rad_sum))
    radDict[radNum[j]] = rad_sum
    print()

with open('/data1/Sixing/expdata/topGT_st') as f:
    f.write(str(topDict))

with open('/data1/Sixing/expdata/radGT_st') as f:
    f.write(str(radDict))
