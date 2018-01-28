'''

'''
#----------------
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
    for i in range(len(pathTem)):
        if pathTem[i] == 'S' or pathTem[i] == 'C':
            idx = i
            break
    pathDict['partID'].append(int(pathStr[-idx:]))
    return pathDict   
#----------------
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

dataset = ['tr_1', '/data1/Sixing/tr_1_4ij', '/data1/Sixing/tr_1_2', '/data1/Sixing/tr_1']


hSet = [1000,100,10]
stra = [[0, 1]]
hList =  [400]
maxIDList = [255255]
w = 10
h = 20
edge = [60764, 32817]

h = 10
partNum = [2,4,8]
hListM = [[800,1250],[4,10000,25],[4,100,50,200,25]]
hListC = [[10**6,],[10**8,],[10**8,]]
straM = [[0,],[1,]],[(0,),(1,2),(3,)],[(1,),(2,3),(4,7),(0,5),(6,)]
straC = [[0,1,]],[(0,1,2,3)],[(0,1,2,3,4,5,6,7)],
partList = [[0,1],[0,1,2,3],[0,1,2,3,4,5,6,7]]
w = 10

strList = []

for i in range(len(partNum)):
    sketchList = []
    if not i == 1: # only for 4-parts
        continue
    hListG = [hSet[i] for _ in range(partNum[i])]
    straG = [[j,] for j in range(partNum[i])]
    #mS = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListM[i],w,hSet[i],straM[i],partNum[i]));mS.buildSketch()
    mC = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListC[i],w,hSet[i],straC[i],partNum[i]));mC.buildSketch()
    mG = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListG,w,hSet[i],straG,partNum[i]));mG.buildSketch()
    
    for path in strList:
        d = getPathDict(path)
        stra = getStrategy(d)
        mS = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListM[i],w,hSet[i],stra,partNum[i]));mS.buildSketch()
        sketchList.append(mS)

    with open(dataset[i+1],'r') as f:
        # input structure of sketch 
        # open a sample of stream partList, e.g., 5,6,7
        pool = []
        print('getting stream ==========> ')
        for line in f:
            line = line.strip()
            if not len(line) > 0:
                continue
            countNum += 1
            if countNum > 1000000:
                break
            parts = line.split(' ')
            #print('line '+line)
            # should be multi-part
            if partNum[i]> 5: # for 8 parts
                try:
                    sNode = [int(k) for k in parts[0].split('.')];
                    tNode = [int(k) for k in parts[1].split('.')];
                except:
                    continue
                fre = float(parts[2])
                nodeList = sNode + tNode
                #print('8 parts')
            elif partNum[i]> 3 :# for 4 parts
                nodeList = [int(k) for k in parts[:4]]
                #print('4 parts')
            else:
                nodeList = [int(k) for k in parts[:2]]

            fre = float(parts[-1])
            edge = []
            #print('nodeList '+str(nodeList))
            for pID in partList[i]:
                edge.append(nodeList[pID])
            #print(edge)
            #print(fre)

            for num in sketchList:
                sketchList[num].update(edge,fre)

            mC.update(edge,fre)

            mG.update(edge,fre)












