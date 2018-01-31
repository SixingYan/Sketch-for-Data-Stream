#filename = '/data1/Sixing/tr_1_2'
filename = '/data1/Sixing/stream dataset/ipv4fre4ij_refined'
maxID = 0
num = 0
total = 0
maxFre = 0
sKey = set([])
tKey = set([])
sDict = {}
tDict = {}

with open(filename, 'r') as f:
    for line in f:
        line = line.strip()
        if len(line)>0:
            parts = line.split(' ');
            s = int(parts[0]); t = int(parts[1]); freq = parts[2]
            if s in sKey:
                sDict[s] += freq
            else:
                sKey.add(s)
                sDict[s] = 0
                sDict[s] += freq
            
            if t in tKey:
                tDict[t] += freq
            else:
                tKey.add(t)
                tDict[t] = 0
                tDict[t] += freq
            #nodeList = parts[:4]
            #idList = [int(p) for p in nodeList]
            num += 1
            total += freq
            
            if maxFre < freq:
                maxFre = freq

            if max([s,t])>maxID:
                maxID = max([s,t])
            #if max(nodeList) > maxID:
            #    maxID = max(nodeList)
sMax = 0
tMax = 0
for k in list(sKey):
    if sMax< sDict[k]:
        sMax = sDict[k]
for k in list(tKey):
    if tMax< tDict[k]:
        tMax = tDict[k]
#print(maxID)
#print(num)
with open('/data1/Sixing/expdata/txt_fre_info','w') as f:
    #f.write(str(maxID)+'   '+str(num))
    f.write('maxID is '+' '+str(maxID)+'\n')
    f.write('num is '+' '+str(num)+'\n')
    f.write('total is '+' '+str(total)+'\n')
    f.write('maxFre is '+' '+str(maxFre)+'\n')
    f.write('s len is '+' '+str(len(sKey))+'\n')
    f.write('t len is '+' '+str(len(tKey))+'\n')
    f.write('sMax is '+' '+str(sMax)+'\n')
    f.write('tMax is '+' '+str(tMax)+'\n')