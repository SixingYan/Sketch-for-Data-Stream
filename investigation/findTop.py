"""
"""
import random
homePath = '/data1/Sixing/expdata/top5000_'
dataset = [ 
    #['D:/google desk PC/graph_freq_comp18.txt',338239,'comp18', 1],
    #['D:/google desk PC/graph_freq_comp16.txt',1391333,'comp16', 1],
    #['D:/google desk PC/graph_freq_comp14.txt',7904564,'comp14', 1],
    #['D:/google desk PC/ip_graph_refined',4213084,'ip', 1],
    #['/data1/Sixing/stream dataset/tweet_stream_hashed_refined',17813281,'tweet', 1],
    #['/data1/Sixing/stream dataset/graph_freq_comp12.txt',31160379,'comp12', 0.8],
    #['/data1/Sixing/stream dataset/graph_freq_comp1.txt',56175513,'comp1', 0.1]
    #['/data1/Sixing/stream dataset/graph_freq_comp1.txt',56175513,'comp1', 0.1]
    #['/data1/Sixing/stream dataset/graph_freq_comp1.txt',56175513,'comp1', 0.1]
]
for ds in dataset:
    print('now is '+str(ds))
    countNum = 0
    top5000List = []
    with open(ds[0],'r') as f:
        for line in f.readlines():
            line = line.strip()
            if not len(line)>0:
                continue
            countNum += 1
            if countNum % 1000000 == 0:
                print('now is '+str(countNum))
            if random.randint(0,1) > 0.9:
                continue
            parts = line.split(' ')
            s = int(parts[0])
            t = int(parts[1])
            freq = float(parts[2])

            if len(top5000List)>5000:
                minV = min(top5000List, key=lambda x: x[2])
                if freq>minV[2]:
                    indx = top5000List.index(minV);top5000List[indx] = [s,t,freq]
            else:
                top5000List.append([s,t,freq])
    
    top5000List.sort(key= lambda d : d[2], reverse = True)
    with open(homePath+ds[2]+'.txt','a') as f:
        for edge in top5000List:
            line = str(edge[0])+' '+str(edge[1])+' '+str(edge[2])+'\n'
            f.write(line)
    del top5000List