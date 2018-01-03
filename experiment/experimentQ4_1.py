




import hSketch



wSet = [10,15]
num1 = 0
num2 = 100
increase = 100
h = 1000
dataset = [ 
    #['D:/google desk PC/ip_graph_refined',4213084,2,'ip', 80],
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp18.txt',338239,2,'comp18', 0.80],
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp16.txt',1391333,2,'comp16', 0.80],
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp14.txt',7904564,2,'comp14', 0.60],
    ['D:/google desk PC/ip_graph_refined',4213084,2,'ip', 0.70],
    ['C:/Users/alfonso.yan/Documents/tweet_stream_hashed_refined',17813281,2,'tweet', 0.50],
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp12.txt',338239,2,'comp18', 90],
    ['C:/Users/alfonso.yan/Documents/graph_freq_comp10.txt',1372146644,2,'comp1', 0.03]
]

def getH1H2(num1,num2,h):
    h1h2List = []
    for i in range(num1,num2):
        h1 = (i+1)*increase
        h2 = int(h**2/h1)
        h1h2List.append((h1,h2))
    return h1h2List

def getValue(twoDlist):
    result = []
    for i in range(num2-num1):
        valueList = []
        for repeat in range(repeatNumber):
            valueList.append(twoDlist[repeat][i])
        result.append(sum(valueList)/repeatNumber)
    return result

def getRadList(num):
    radList = [[] for i in range(5)]
    for i in range(len(radList)):
        while len(radList[i]) < num:
            tem = choice(radPool)
            if tem not in radList[i]:
                radList[i].append(tem)
    return radList

def evaluate_top_medium(sketch,topList):
    #
    totalLoss1 = 0;totalFreq1 = 0
    for parts in topList:
        s=parts[0]; t=parts[1];freq = parts[2]
        estiValue = sketch.edge_frequency_query((s,t))
        totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
    ObservedError = totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError))
    return ObservedError

def evaluate_top_mean(sketch,topList):
    #
    totalLoss1 = 0;totalFreq1 = 0
    for parts in topList:
        s=parts[0]; t=parts[1];freq = parts[2]
        estiValue = sketch.edge_frequency_query((s,t))
        totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
    ObservedError = totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError))
    return ObservedError

def evaluate_top_sum(sketch,topList):
    totalLoss1 = 0;totalFreq1 = 0
    for parts in topList:
        s=parts[0]; t=parts[1];freq = parts[2]
        estiValue = sketch.edge_frequency_query((s,t))
        totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
    ObservedError = totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError))
    return ObservedError

def evaluate_rad_medium(sketch,radList):
    #
    ObservedError = 0
    for i in range(len(radList)):
        totalLoss1 = 0;totalFreq1 = 0
        for parts in radList[i]:
            s=parts[0]; t=parts[1];freq = parts[2]
            estiValue = sketch.edge_frequency_query((s,t))
            totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
        ObservedError += totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError/len(radList)))
    return ObservedError

def evaluate_rad_mean(sketch,radList):
    #
    ObservedError = 0
    for i in range(len(radList)):
        totalLoss1 = 0;totalFreq1 = 0
        for parts in radList[i]:
            s=parts[0]; t=parts[1];freq = parts[2]
            estiValue = sketch.edge_frequency_query((s,t))
            totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
        ObservedError += totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError/len(radList)))
    return ObservedError

def evaluate_rad_sum(sketch,radList):
    #
    ObservedError = 0
    for i in range(len(radList)):
        totalLoss1 = 0;totalFreq1 = 0
        for parts in radList[i]:
            s=parts[0]; t=parts[1];freq = parts[2]
            estiValue = sketch.edge_frequency_query((s,t))
            totalLoss1 += abs(estiValue-freq);totalFreq1 += freq
        ObservedError += totalLoss1/totalFreq1
    print('ObservedError is '+str(ObservedError/len(radList)))
    return ObservedError


for ds in dataset:
    oeListTop100Dict=[];oeListRad100Dict=[]
    oeListTop500Dict=[];oeListRad500Dict=[]
    oeListTop1000Dict=[];oeListRad1000Dict=[]
    for repeat in range(repeatNumber):

        h1h2List = getH1H2(num1,num2,h)#h=500
        sketchList = []
        for i in range(len(h1h2List)):
            h1,h2 = h1h2List[i]
            print('for %d, h1 is %d   h2 is %d'%(i,h1,h2))
            hS = deepcopy(hSketch.sketch(w,h1,h2,maxNodeID))
            sketchList.append(hS)

        radPool = []

        # start stream
        with open() as f:
            for line in f:
                line = line.strip()
            if not len(line)>0:
                continue
            countNum += 1

            parts = line.split(' ')
            edge = parts[:len(parts)-1]
            for num in range(len(edge)):
                edge[num] = int(edge[num])
            freq = int(float(parts[len(parts)-1]))

            if randint(0,1000)>1000* ds[5]:
                continue

            # get rad and top

            if randint(0,10000)<10000* ds[5] * 0.1:
                radPool.append([s,t,freq])
                
            if len(top1000List)>1000:
                minV = min(top1000List, key=lambda x: x[2])
                if freq>minV[2]:
                    indx = top1000List.index(minV);top1000List[indx] = [s,t,freq]
            else:
                top1000List.append([s,t,freq])


        top1000List.sort(reverse = False)
        top100List = top1000List[:100]
        top500List = top1000List[:500]
        rad100List = getRadList(100)
        rad500List = getRadList(500)
        rad1000List = getRadList(1000)

        oeListTop100=[];oeListRad100=[]
        oeListTop500=[];oeListRad500=[]
        oeListTop1000=[];oeListRad1000=[]

        for i in range(len(sketchList)):
            print('for %d'%i)
            ObservedError = evaluate_top_mean(sketchList[i],top100List);oeListTop100.append(ObservedError)
            ObservedError = evaluate_top_mean(sketchList[i],top500List);oeListTop500.append(ObservedError)
            ObservedError = evaluate_top_mean(sketchList[i],top1000List);oeListTop1000.append(ObservedError)
            print()
        

        # evaluation

        oeListTop100Dict.append(oeListTop100)
        oeListRad100Dict.append(oeListRad100)
        oeListTop500Dict.append(oeListTop500)
        oeListRad500Dict.append(oeListRad500)
        oeListTop1000Dict.append(oeListTop1000)
        oeListRad1000Dict.append(oeListRad1000)


        # delete
        del sketchList;

    oeRad100 = getValue(oeListRad100Dict)
    oeTop100 = getValue(oeListTop100Dict)
    oeRad500 = getValue(oeListRad500Dict)
    oeTop500 = getValue(oeListTop500Dict)
    oeRad1000 = getValue(oeListRad1000Dict)
    oeTop1000 = getValue(oeListTop1000Dict)




