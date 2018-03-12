import random
import math
#dicPath = 'C:/Users/alfonso.yan/Documents/'
dicPath = '/data1/Sixing/'
dataset = [
    #[dicPath+'stream_dataset/tweet_stream_hashed_refined', dicPath+'expdata/tweet_new_',2,146039643,],
    #[dicPath+'stream_dataset/tr_fre_4ij_refined', dicPath+'expdata/tr4ij_new1000_',2,23914951790,],
    [dicPath+'stream_dataset/sanusfre4ij_refined', dicPath+'expdata/sanus4ij_new1000_',2,56829446592,],
]

sliceNum = 1000
dataPath = dataset[0][0]
samplePath = dataset[0][1]
partNum = dataset[0][2]
totalSize = int(dataset[0][3]/sliceNum)
percDict = [0.003,0.005,0.01,0.02,0.05,0.1,0.2]
sizeDict = [int(totalSize * perc) for perc in percDict]
radPoolDict = [[] for _ in range(len(percDict))]
m = 0

def pushRad(item):
    global radPoolDict
    global m
    for i in range(len(percDict)):
        if len(radPoolDict[i]) < sizeDict[i]:
            radPoolDict[i].append(item)
        else:
            if random.random() < m/(m+1):
                idx = random.randint(0, sizeDict[i]-1)
                radPoolDict[i][idx] = item
    m += 1

def sampling():
    global m
    global size
    # count = 0
    with open(dataPath, 'r') as f:
        for line in f:
            line = line.strip()
            if not len(line)>0:
                continue
            # (a,b,c,d) freq
            # count += 1
            if partNum == 8:
                parts = line.split(' ')
                edge = tuple([int(i) for i in parts[:len(parts)-1]])
                freq = float(parts[len(parts)-1])
            else:
                parts = line.split(' ')
                edge = tuple([int(i) for i in parts[:len(parts)-1]])
                freq = float(parts[len(parts)-1])

            if freq > sliceNum:
                num = int(math.ceil(freq/sliceNum))
                for i in range(1, num):
                    flatFreq = i*sliceNum
                    pushRad((edge, flatFreq))
                flatFreq = freq - (num-1) * sliceNum
                pushRad((edge, flatFreq))
            else:
                pushRad((edge, freq))

def outputSample():
    #a b c d freq
    global radPoolDict
    for i in range(len(percDict)):
        with open(samplePath + str(percDict[i])+'.txt', 'a') as f:
            for item in radPoolDict[i]:
                line = ''
                for node in item[0]:
                    line = line + str(node) + ' '
                line = line + str(item[1]) +'\n'
                f.write(line)

def getSample():
    sampling()
    print('complete')
    outputSample()

getSample()