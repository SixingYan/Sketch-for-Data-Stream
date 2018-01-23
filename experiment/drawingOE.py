'''

'''

import diyTool
homepath = '/data1/Sixing/expdata/'
dataset = [
    # cs, gm, hsketch 
    #['D:/google desk PC/graph_freq_comp18.txt',338239,'comp18', 0.80],
    #['D:/google desk PC/graph_freq_comp16.txt',1391333,'comp16', 0.80],
    #['D:/google desk PC/graph_freq_comp14.txt',7904564,'comp14', 0.60],
    #['D:/google desk PC/ip_graph_refined',4213084,'ip', 0.70],
    #['D:/google desk PC/tweet_stream_hashed_refined',17813281,'tweet']#
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp12.txt',31160379,'comp12', 90],
    [homepath+'Q4_TopCG_',homepath+'Q4_RadCG_','Top','Rad','tweet']
]
sampleP = '/data1/Sixing/expdata/sample/'
w = 10
increase = 10
h = 1000
topNum = [100,500,1000,2000,5000] 
radNum = [500,1000,2000,5000,10000]
percent = [0.05, 0.1, 0.2]
def getAlpha(dsname):
    AlphaDict = {}
    for i in range(len(percent)):
        dictKeyList = set([])
        nodeDict = {}
        path = sampleP+dsname+'_'+str(percent[i])+'.txt'
        print('get sample ==== '+path)
        countNum = 0
        with open(path,'r') as f:
            # out degree
            for line in f:
                line = line.strip()
                if not len(line) > 0:
                    continue
                countNum += 1
                parts = line.split(' ')
                s = int(parts[0]);t = int(parts[1]);freq = float(parts[2])
                # out degree
                if s in dictKeyList:
                    nodeDict[s][1] += freq
                else:
                    nodeDict[s] = [0,0];nodeDict[s][1] += freq
                    dictKeyList.add(s)
                # in degree
                if t in dictKeyList:
                    nodeDict[t][0] += freq
                else:
                    nodeDict[t] = [0,0];nodeDict[t][0] += freq
                    dictKeyList.add(t)
        aList = []
        with open(path,'r') as f:
            for line in f:
                line = line.strip()
                if not len(line) > 0:
                    continue
                parts = line.split(' ')
                s = int(parts[0]);t = int(parts[1])
                # alpha = (i,*)/(*,j)
                a = nodeDict[s][1]/nodeDict[t][0] # * freq
                aList.append(a)
        aList.sort()
        #alphaMAX = max(aList);alphaMEAN = np.mean(aList);
        alphaMEDIUM = getMedium(aList)
        AlphaDict[percent[i]] = alphaMEDIUM #.append([alphaMEAN,alphaMEDIUM,alphaMAX])
    return AlphaDict

# get range of sqrt beta
def getH1Range(a):
    #
    sqrtBeta = (a+1)/(2*a)
    optH1 = int(h * sqrtBeta)
    return optH1

def getPredict(oeDict,numList,optH1,ty):
    # ty 'top_medium'
    preOEdict = {}
    for num in numList:
        oeList = oeDict[ty][num]
        h1OE = oeList[:100]
        h2OE = oeList[100:]
        h2OE.reverse()
        h1OE.extend(h2OE)

        h1List = [(i+1)*increase for i in range(0,100)]
        h1h2List = [int(h**2/((i+1)*increase)) for i in range(99,-1,-1)]
        h1List.extend(h1h2List)
        for i in range(len(h1List)):
            if h1List[i] > optH1:
                preValue = h1OE[i]
                break
        preOEdict[num] = preValue
    return preOEdict

def getMedium(valueList):
    return (valueList[int(len(valueList)/2)] + valueList[~int(len(valueList)/2)])/ 2

def getRecord(address,h,dname,sName,numList):
    # tem1 = {'h':h,'w':w,'ds':ds[2],'sketch':'hSketch',5000:[],2000:[],1000:[]...}
    # return dict-type record 
    resultDict = diyTool.loadPickle(address)
    obDict = {} # {5000:[],2000:[],1000:[]...}
    for rd in resultDict:
        if rd['h']==h and rd['ds']==dname and rd['sketch']==sName:
            for num in numList:
                obDict[num] = rd[num]
            break
    return obDict

# find the least error from 
for ds in dataset:
    dataName = ds[4]
    print('ds ====== ')
    # (3,3)
    plt.figure(figureID)
    tPlot_top, axes_top = plt.subplots(nrows=3, ncols=3,figsize=(15,12))
    tPlot.tight_layout(renderer=None, pad=2, h_pad=2, w_pad=2, rect=None)
    x = range(1,5)
    # (3,3)

    for j in range(len(hSet)):   #3 
        h = hSet[j]
        print('h ========= ')
        #Q4_TopCG_ 500_tweet.pickle
        gmDS_Top = getRecord(ds[0] + str(h)+'_'+dataName+'.pickle') # 100,500,1000....
        csDS_Top = getRecord(ds[0] + str(h)+'_'+dataName+'.pickle') # 100,500,1000....
        hsDS_Top = getRecord(ds[2] + str(h)+'_'+dataName+'.pickle') # 100,500,1000....
        AlphaDict = getAlpha(dataName)

        #predicting
        for i in range(len(percent)): # 3
            print('now getting sample '+str(percent[i]))
            alpha = AlphaDict[percent[i]]
            opt = getH1Range(alpha)
            preValue = getPredict(hsDS_Top,topNum,opt,'top_medium') # 100,500,1000....

            cVList = []
            gVList = []
            hVList = []
            pVList = [] 
            for n in topNum: #4
                cSBase = csDS_Top[n]
                gmBase = gmDS_Top[n]
                hBase = (hsDS_Top[n][99]+ hsDS_Top[n][199])/2
                cSBase = hBase/gmBase * cSBase
                cVList.append(cSBase)
                gVList.append(gmBase)
                hVList.append(min(hsDS_Top[n]))
                pVList.append(min(preValue[n]))

            #drawing vary h and sample size %

            axes[i][j].plot(x,cVList,label='Count-Min',marker=markerList[i],markersize=7, linestyle='--',lw=2)
            axes[i][j].plot(x,gVList,label='gMatrix',marker=markerList[i],markersize=7, linestyle='--',lw=2)
            axes[i][j].plot(x,hVList,label='Baseline',marker=markerList[i],markersize=7, linestyle='--',lw=2)
            axes[i][j].plot(x,pVList,label='MOD Sketch',marker=markerList[i],markersize=7, linestyle='--',lw=2)
            axes[i][j].set_xlabel('# of random queries with h='+str(h)+ ' and %.2f %% sample'% (percent[k]*100))
            axes[i][j].set_ylabel('Observed Error')
            axes[i][j].set_xticks(x)
            axes[i][j].set_xticklabels(topNum)

    plt.legend(prop={'size':14})
    plt.show()

def function():
    # X: h  Y: ob
    pass

def function():
    # X:  Y: 
    pass

