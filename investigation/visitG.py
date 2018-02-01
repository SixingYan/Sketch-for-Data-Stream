filename = '/data1/Sixing/sanus_fre_4ij'
#maxID = 0
#num = 0
maxFre = 0
total = 0
with open(filename, 'r') as f:
    for line in f:
        line = line.strip()
        #print(line)
        if len(line)>0:
            parts = line.split(' ');
            s = int(parts[0]); t = int(parts[1]); freq = float(parts[2])
            if maxFre < freq:
                maxFre = freq
            total += freq
            #nodeList = parts[:4]
            #idList = [int(p) for p in nodeList]
            #num += 1
            #if max([s,t])>maxID:
            #if max(nodeList) > maxID:
            #    maxID = max(nodeList)
#print(maxID)
#print(num)
with open('/data1/Sixing/txt_sanus_fre_4ij','w') as f:
    f.write(str(maxFre)+'   '+str(total))