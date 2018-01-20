# -*- coding: utf-8 -*-
import lib
import lib.mSketch as mSketch
import lib.sketchTreeNode as tn

def buildTree(node):
    global globalNodeID
    candidate = tn.getCandidate(node) # 没出现在path上的partID
    for partID in candidate:
        if partID < node.partID: # MIND!!!! here should be part.order < part.order 
            subnode = tn.treenode(partID, globalNodeID, node.nodeID, node.order+1);
            globalNodeID += 1
            nodeDict[subnode.nodeID] = subnode # store this node
            node.nextNodes[subnode.nodeID] = 'C' # 因为part ID 不唯一
            if subnode.order < N:# not leaf 
                buildTree(subnode)
            else:
                subnode.isLeaf = True # use for search 
                currentPath = tn.getPath(subnode) # list-type
                leafDict[subnode.nodeID] = currentPath
    #for partID in candidate:
    subnode = tn.treenode(max(candidate), globalNodeID, node.nodeID, node.order+1)
    globalNodeID += 1
    nodeDict[subnode.nodeID] = subnode # store this node
    node.nextNodes[subnode.nodeID] = 'S'
    if subnode.order < N:# not leaf 
        buildTree(subnode)
    else:
        subnode.order  = True #
        currentPath = tn.getPath(subnode) # str-type
        leafDict[subnode.nodeID] = currentPath



w = 10
h = 50
N = 4
maxIDList = [255 for i in range(n)]
hList = [h for i in range(n)]
globalNodeID = 0
partList = [i for i in range(N)]
nodeDict = {}
leafDict = {}

rootID = max(partList) #diyTool.getRoot()
root = tn.treenode(rootID, globalNodeID, -1, 1)
nodeDict[globalNodeID] = root # store this node
globalNodeID += 1
buildTree(root)

sketchList = []
strategy = []
for ky in list(leafDict.keys()):
    pathStr = leafDict[ky]
    strategy.append(pathStr)
    d = tn.getPathDict(pathStr)
    stra = tn.getStrategy(d)
    sketch = copy.deepcopy(mSketch.mSketch(maxID,hList,w,stra))
    sketchList.append(sketch)


with open(ds[0],'r') as f:
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

        if random.randint(0,10000)>10000 * 0.9:
            continue
        # get rad and top
        if random.randint(0,10000)<10000 * 0.4:
            radPool.append([edge,freq])
                
        if len(top5000List)>5000:
            minV = min(top5000List, key=lambda x: x[1])
            if freq>minV[2]:
                indx = top5000List.index(minV);top5000List[indx] = [edge,freq]
        else:
            top5000List.append([edge,freq])        
        # update 
        for i in range(len(sketchList)):
            sketchList[i].update(edge,freq)


print('========evaluation')# evaluation
#top5000List = getTopList(ds[2])
topList = []; radList = []
top5000List.sort(key= lambda d : d[1], reverse = False)
for i in range(len(topNum)):
    topList.append(top5000List[:topNum[i]])
    radList.append(getRadList(radNum[i],radPool))
del radPool # clean




print('start top')
    #sketchOE = {'h':h,'w':w,'ds':ds[2]}
    tem = {'h':h,'w':w,'ds':ds[2]}
    # topList
    print('----------top')# random
    for j in range(len(topList)): # 5
        tem[topNum[j]] = {}
        top_mean = []
        top_medium = []
        top_sum = []
        print('====now is '+str(topNum[j]))
        for i in range(len(sketchList)): #150?
            ObservedError = evaluate_top_mean(sketchList[i],topList[j]);top_mean.append(ObservedError)
            print()
            ObservedError = evaluate_top_medium(sketchList[i],topList[j]);top_medium.append(ObservedError)
            print()
            ObservedError = evaluate_top_sum(sketchList[i],topList[j]);top_sum.append(ObservedError)
            print()
        tem[topNum[j]]['top_mean'] = top_mean
        tem[topNum[j]]['top_medium'] = top_medium
        tem[topNum[j]]['top_sum'] = top_sum
    datasetTop.append(tem)
















