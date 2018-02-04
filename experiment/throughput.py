'''
run on bigmachine
'''
import copy
import time
import mSketch2D
#import lib.mSketch as mSketch
import numpy as np 


maxIDList = [
[255255255255 for _ in range(2)],
[255255 for _ in range(4)],
[255 for _ in range(8)],
]

hSet = [1000,100,10]
dataset = ['tr_1', '/data1/Sixing/tr_1_4ij', '/data1/Sixing/tr_1_2', '/data1/Sixing/tr_1']#  ['tr_fre', '/data1/Sixing/tr_fre_4ij', '/data1/Sixing/tr_fre_2', '/data1/Sixing/tr_fre',]
#['tr_fre', '/tr_fre_4ij', '/tr_fre_2', '/tr_fre',],

#h = 10
partNum = [2,4,8]
hListM = [[800,int(10**6*4/800)],[33,480,250],[8,8,30,100,20]]
hListC = [10**6*4]
straM = [[0,],[1,]],[(0,),(1,2),(3,)],[(1,),(2,3),(4,7),(0,5),(6,)]
straC = [[0,1,]],[(0,1,2,3)],[(0,1,2,3,4,5,6,7)],
partList = [[0,1],[0,1,2,3],[0,1,2,3,4,5,6,7]]
w = 10
for i in range(len(partNum)):
    #hListG = [hSet[i] for _ in range(partNum[i])]
    hListG = [pow(10**6*4,1/partNum[i]) for pn in range(partNum[i])]
    straG = [[j,] for j in range(partNum[i])]
    mS = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListM[i],w,hSet[i],straM[i],partNum[i]));mS.buildSketch()
    mC = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListC,w,hSet[i],straC[i],partNum[i]));mC.buildSketch()
    mG = copy.deepcopy(mSketch2D.mSketch2D(maxIDList[i],hListG,w,hSet[i],straG,partNum[i]));mG.buildSketch()
    countNum = 0
    tC = [];tG = [];tM = []
    with open(dataset[i+1],'r') as f:
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
            t1 = time.time()
            mS.update(edge,fre)
            tM.append(time.time()-t1)

            t1 = time.time()
            mC.update(edge,fre)
            tC.append(time.time()-t1)
            
            t1 = time.time()
            mG.update(edge,fre)
            tG.append(time.time()-t1)

    del mS; del mC; del mG; 

    with open('/data1/Sixing/expdata/TXT_w'+str(w)+'_'+dataset[0],'a') as f:
        f.write('\n Part num: '+str(partNum[i])+'\n')
        f.write('MOD is '+str(np.mean(tM))+'\n')
        f.write('GMATRIX is '+str(np.mean(tG))+'\n')
        f.write('COUNTMIN is '+str(np.mean(tC))+'\n')