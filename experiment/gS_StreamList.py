
def getEdge(line, n):
    if n==8:
        parts = line.split(' ')
        freq = float(parts[2])
        sEdge = [int(i) for i in parts[0].strip().split('.')]
        tEdge = [int(i) for i in parts[1].strip().split('.')]
        edge = tuple(sEdge+tEdge)
    else:
        parts = line.split(' ')
        edge = tuple([int(i) for i in parts[:len(parts)-1]])
        freq = float(parts[len(parts)-1])
    return edge, freq

def getSortedStream(dataPath, n):
    # input flat stream
    nfoDict = {}
    with open(dataPath,'r') as f:
        for line in f:
            line = line.strip()
            if not len(line)>0:
                continue

            try:
                edge, freq = getEdge(line, n)
            except:
                continue

            if edge[0] in nfoDict.keys():
                nfoDict[edge[0]][0] += freq
                nfoDict[edge[0]][1].add(tuple(edge[1:]))
            else:
                nfoDict[edge[0]] = [0, set([])]
                nfoDict[edge[0]][0] += freq
                nfoDict[edge[0]][1].add(tuple(edge[1:]))

    for ky in list(nfoDict.keys()):
        nfoDict[ky][1] = len(nfoDict[ky][1])

    streamList = []
    for item in list(nfoDict.items()):
        streamList.append((item[0], round(item[1][0], 2), item[1][1]))
    print('get stream complete!\n')

    streamList.sort(key=lambda x: x[1]/x[2], reverse = True)
    print('stream sorted complete!\n')
    return streamList # nfoList


def getSortedStream_m(dataPath, n):
    # input flat stream
    efoDict_m = []
    for i in range(n):
        efoDict_m.append({})

    with open(dataPath,'r') as f:
        for line in f:
            line = line.strip()
            if not len(line)>0:
                continue
            try:
                edge, freq = getEdge(line, n)
            except:
                continue

            for i in range(len(edge)):
                if edge[i] in efoDict_m[i].keys():
                    efoDict_m[i][edge[i]][0] += freq
                    efoDict_m[i][edge[i]][1].add(tuple(edge[:i] + edge[i+1:]))
                else:
                    efoDict_m[i][edge[i]] = [0, set([])]
                    efoDict_m[i][edge[i]][0] += freq
                    efoDict_m[i][edge[i]][1].add(tuple(edge[:i] + edge[i+1:]))
    
    streamList_m = [[] for _ in range(n)]
    for i in range(n):
        for ky in list(efoDict_m[i].keys()):
            efoDict_m[i][ky][1] = len(efoDict_m[i][ky][1])

        for item in list(efoDict_m[i].items()):
            streamList_m[i].append((item[0], round(item[1][0], 2), item[1][1]))

        streamList_m[i].sort(key=lambda x: x[1]/x[2], reverse = True)
    return streamList_m # efoList_m


def getSortedStream_s(dataPath, samplePath, n):
    # input flat stream
    nfoDict = {}
    with open(dataPath,'r') as f:
        for line in f:
            line = line.strip()
            if not len(line)>0:
                continue
            try:
                edge, freq = getEdge(line, n)
            except:
                continue

            if edge[0] in nfoDict.keys():
                nfoDict[edge[0]][0] += freq
                nfoDict[edge[0]][1].add(tuple(edge[1:]))
            else:
                nfoDict[edge[0]] = [0, set([])]
                nfoDict[edge[0]][0] += freq
                nfoDict[edge[0]][1].add(tuple(edge[1:]))

    for ky in list(nfoDict.keys()):
        nfoDict[ky][1] = len(nfoDict[ky][1])

    streamList = []
    for item in list(nfoDict.items()):
        streamList.append((item[0], round(item[1][0], 2), item[1][1]))
    print('get stream complete!\n')

    streamList.sort(key=lambda x: x[1]/x[2], reverse = True)
    print('stream sorted complete!\n')

    nfoDict_s = {}
    with open(samplePath,'r') as f:
        for line in f:
            line = line.strip()
            if not len(line)>0:
                continue
            try:
                edge, freq = getEdge(line, n)
            except:
                continue

            if edge[0] in nfoDict_s.keys():
                nfoDict_s[edge[0]][0] += freq
                nfoDict_s[edge[0]][1].add(tuple(edge[1:]))
            else:
                nfoDict_s[edge[0]] = [0, set([])]
                nfoDict_s[edge[0]][0] += freq
                nfoDict_s[edge[0]][1].add(tuple(edge[1:]))

    for ky in list(nfoDict_s.keys()):
        nfoDict_s[ky][1] = len(nfoDict_s[ky][1])

    sampleList = []
    for item in streamList:
        if item[0] in nfoDict_s.keys():
            freq, od = nfoDict_s[item[0]]
            sampleList.append((item[0], round(freq, 2), od))
        else:
            sampleList.append((item[0], 1, 1))

    return streamList,sampleList # nfoList


def getSortedStream_m_s(dataPath, samplePath, n):
    # input flat stream
    efoDict_m = []
    for i in range(n):
        efoDict_m.append({})

    with open(dataPath,'r') as f:
        for line in f:
            line = line.strip()
            if not len(line)>0:
                continue
            try:
                edge, freq = getEdge(line, n)
            except:
                continue
            for i in range(len(edge)):
                if edge[i] in efoDict_m[i].keys():
                    efoDict_m[i][edge[i]][0] += freq
                    efoDict_m[i][edge[i]][1].add(tuple(edge[:i] + edge[i+1:]))
                else:
                    efoDict_m[i][edge[i]] = [0, set([])]
                    efoDict_m[i][edge[i]][0] += freq
                    efoDict_m[i][edge[i]][1].add(tuple(edge[:i] + edge[i+1:]))
    
    streamList_m = [[] for _ in range(n)]
    for i in range(n):
        for ky in list(efoDict_m[i].keys()):
            efoDict_m[i][ky][1] = len(efoDict_m[i][ky][1])

        for item in list(efoDict_m[i].items()):
            streamList_m[i].append((item[0], round(item[1][0], 2), item[1][1]))

        print(str(i)+' get stream complete!\n')
        streamList_m[i].sort(key=lambda x: x[1]/x[2], reverse = True)
        print(str(i)+' stream sorted complete!\n')
    
    ###################
    efoDict_m_s = []
    for i in range(n):
        efoDict_m_s.append({})
    with open(samplePath,'r') as f:
        for line in f:
            line = line.strip()
            if not len(line)>0:
                continue
            try:
                edge, freq = getEdge(line, n)
            except:
                continue
            for i in range(len(edge)):
                if edge[i] in efoDict_m_s[i].keys():
                    efoDict_m_s[i][edge[i]][0] += freq
                    efoDict_m_s[i][edge[i]][1].add(tuple(edge[:i] + edge[i+1:]))
                else:
                    efoDict_m_s[i][edge[i]] = [0, set([])]
                    efoDict_m_s[i][edge[i]][0] += freq
                    efoDict_m_s[i][edge[i]][1].add(tuple(edge[:i] + edge[i+1:]))
    
    streamList_m_s = [[] for _ in range(n)]
    for i in range(n):
        for ky in list(efoDict_m_s[i].keys()):
            efoDict_m_s[i][ky][1] = len(efoDict_m_s[i][ky][1])

        for item in list(efoDict_m_s[i].items()):
            streamList_m_s[i].append((item[0], round(item[1][0], 2), item[1][1]))

        #print(str(i)+' get stream complete!\n')
        streamList_m_s[i].sort(key=lambda x: x[1]/x[2], reverse = True)
        #print(str(i)+' stream sorted complete!\n')

    sampleList_m_s = []
    for i in range(n):
        for item in streamList_m[i]:
            if item[0] in efoDict_m_s.keys():
                freq, od = efoDict_m_s[item[0]]
                sampleList_m_s[i].append((item[0], round(freq, 2), od))
            else:
                sampleList_m_s[i].append((item[0], 1, 1))



    return streamList_m, sampleList_m_s # efoList_m