'''
run on bigmachine
'''
import copy
import time
import mSketch2D
#import lib.mSketch as mSketch
tC = []
tG = []
tM = []
maxIDList = [
[255255255255 for _ in range(2)],
[255255 for _ in range(4)],
[255 for _ in range(8)],
]
hSet = [160000,400,20]
dataset = [
    ['tr_1', '/data1/Sixing/tr_1_4ij', '/data1/Sixing/tr_1_2', '/data1/Sixing/tr_1'],
    #['tr_fre', '/tr_fre_4ij', '/tr_fre_2', '/tr_fre',],
]
h = 20
partNum = [2,4,8]
hListM = [[512*10**4,128*10**4],[200,160000,800],[10,400,800,200,40]]
hListC = [20**8 for _ in range(3)]
straM = [(0),(1)],[(0),(1,2),(3)],[(1),(2,3),(4,7),(0,5),(6)]
straC = [(0,1)],[(0,1,2,3)],[(0,1,2,3,4,5,6,7)],
partList = [[0,1],[0,1,2,3],[0,1,2,3,4,5,6,7]]

for i in range(len(partNum)):
    hListG = [hSet[i] for _ in partNum[i]]
    straG = [tuple(j) for j in range(partNum[i])]
    mS = copy.deepcopy(mSketch2D(maxIDList[i],hListM,w,h,straM,partNum[i]));mS.buildSketch()
    mC = copy.deepcopy(mSketch2D(maxIDList[i],hListC,w,h,straC,partNum[i]));mC.buildSketch()
    mG = copy.deepcopy(mSketch2D(maxIDList[i],hListG,w,h,straG,partNum[i]));mG.buildSketch()
    countNum = 0
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
            if countNum > 10:
                break
            parts = line.split(' ')
            #print('line '+line)
            # should be multi-part
            if len(parts) > 5: # for 8 parts
                sNode = [int(i) for i in parts[0].split('.')];
                tNode = [int(i) for i in parts[1].split('.')];
                fre = float(parts[2])
                nodeList = sNode + tNode
                #print('8 parts')
            elif len(parts) > 3 :# for 4 parts
                nodeList = [int(i) for i in parts[:4]]
                #print('4 parts')
            else:
                nodeList = [int(i) for i in parts[:2]]

            fre = float(parts[-1])
            edge = []
            #print('nodeList '+str(nodeList))
            for pID in partList:
                edge.append(nodeList[pID])
            #print(type(edge[0]))
            #print(fre)
            t1 = time.time()
            mS.update(edge,fre)
            tS.append(time.time()-t1)

            t1 = time.time()
            mC.update(edge,fre)
            tC.append(time.time()-t1)

            t1 = time.time()
            mG.update(edge,fre)
            tG.append(time.time()-t1)

    del mS; del mC; del mG; 

    with open('/data1/Sixing/expdata/TXT_'+dataset[0],'a') as f:
        f.write('\n Part num: '+str(partNum[i])+'\n')
        f.write('MOD is '+str(np.mean(tS))+'\n')
        f.write('GMATRIX is '+str(np.mean(tG))+'\n')
        f.write('COUNTMIN is '+str(np.mean(tC))+'\n')

    break
    











