


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
    if not i == 1: # only for 4-parts
        continue
    hListG = [hSet[i] for _ in range(partNum[i])]
    straG = [[j,] for j in range(partNum[i])]
    #mS = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListM[i],w,hSet[i],straM[i],partNum[i]));mS.buildSketch()
    mC = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListC[i],w,hSet[i],straC[i],partNum[i]));mC.buildSketch()
    mG = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListG,w,hSet[i],straG,partNum[i]));mG.buildSketch()
    
    for path in strList:
        












