"""
"""
import random
percent = [0.001, 0.003, 0.005, 0.01, 0.03, 0.05, 0.1, 0.2]#[ ]
dataset = [ 
    #['D:/google desk PC/graph_freq_comp18.txt',338239,568532,'comp18']#,
    #['D:/google desk PC/graph_freq_comp16.txt',1391333,2815263,'comp16']#,
    #['D:/google desk PC/graph_freq_comp14.txt',7904564,20441831,'comp14'],
    #['C:/Users/alfonso.yan/Documents/ip_graph_refined',4213084,12714850,'ip'],
    #['C:/Users/alfonso.yan/Documents/tweet_stream_hashed_refined',17813281,78508963,'tweet'],
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp12.txt',338239,2,'comp18'], ?
    #['C:/Users/alfonso.yan/Documents/graph_freq_comp10.txt',1372146644,2,'comp1'] ?
]

home = 'D:/google desk PC/sample/'

def getSamplePool(path, samplePool,percent):
    with open(path,'r') as f:
        for line in f:
            if len(line.strip())>0:
                if not random.randint(0,10000) < 10000 * percent:
                    continue # rej
                samplePool.append(line)

for ds in dataset:
    print('=====now is '+ds[3])
    for i in range(len(percent)):
        print('=======percent is '+str(percent[i]))
        samplePool = []
        sampleList = []
        print('======first sampling!')
        while len(samplePool) < ds[2] * percent[i]:
            print('=====get sampling!')
            getSamplePool(ds[0], samplePool, percent[i])
            
        print('======second sampling!')
        if len(samplePool) > ds[2] * percent[i]:
            for _ in range(int(ds[2] * percent[i])):
                idx = random.randint(0,len(samplePool)-1)
                sampleList.append(samplePool[idx])
        print('======saving sampling!')
        with open(home+ds[3]+'_'+str(percent[i])+'.txt','w') as f:
            f.writelines(sampleList)
        del samplePool; del sampleList;