"""

"""
keyDict_2 = {} # (i,j): 1 
keyDict_4 = {} # (i,j,k,l): 1 combine 4 parts as 1 part
keyList_2 = set([])
keyList_4 = set([])

homePath = '/data1/Sixing/'
originalPath = homePath + 'ipv4sr_cleared'
part2Path = homePath + 'ipv4_sr_2'
part4Path = homePath + 'ipv4_sr_4'

with open(originalPath,'r') as f:
    id2 = 1
    id4 = 1
    for line in f:
        if not len(line.strip()) > 0:
            continue
        try:    
            parts = line.strip().split(' ') # ip ip freq
            sParts = parts[0].split('.') #
            tParts = parts[1].split('.') #
            sP4 = [int(s) for s in sParts]
            tP4 = [int(t) for t in tParts]

        # ===================> 4 parts
            sk4 = tuple(sP4)
            if sk4 not in keyList_4:
                idx4_s = id4
                keyList_4.add(sk4)
                keyDict_4[sk4] = idx4_s
                id4 += 1
            else:
                idx4_s = keyDict_4[sk4]
        
            tk4 = tuple(tP4)
            if tk4 not in keyList_4:
                idx4_t = id4
                keyList_4.add(tk4)
                keyDict_4[tk4] = idx4_t
                id4 += 1
            else:
                idx4_t = keyDict_4[tk4]

        # put in 
            with open(part4Path,'a') as ft:
                ft.write(str(idx4_s)+' '+str(idx4_t)+' '+parts[2]+'\n')        
        # 4 parts <===================

            sP1 = tuple(sP4[:2])
            sP2 = tuple(sP4[2:])
        
            if sP1 not in keyList_2:
                idx1_s = id2
                keyList_2.add(sP1)
                keyDict_2[sP1] = idx1_s
                id2 += 1
            else:
                idx1_s = keyDict_2[sP1]

            if sP2 not in keyList_2:
                idx2_s = id2
                keyList_2.add(sP2)
                keyDict_2[sP2] = idx2_s
                id2 += 1
            else:
                idx2_s = keyDict_2[sP2] 

            tP1 = tuple(tP4[:2])
            tP2 = tuple(tP4[2:])
            if tP1 not in keyList_2:
                idx1_t = id2
                keyList_2.add(tP1)
                keyDict_2[tP1] = idx1_t
                id2 += 1
            else:
                idx1_t = keyDict_2[tP1]

            if tP2 not in keyList_2:
                idx2_t = id2
                keyList_2.add(tP2)
                keyDict_2[tP2] = idx2_t
                id2 += 1
            else:
                idx2_t = keyDict_2[tP2] 

            nLine = str(idx1_s)+' '+str(idx2_s)+' '+str(idx1_t)+' '+str(idx2_t)+' '+parts[2]+'\n'
            with open(part2Path,'a') as ft:
                ft.write(nLine)
        except:
            pass
        #break
