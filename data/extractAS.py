"""
extract AS system ip
"""
#================
from os import listdir
from os.path import isfile, join

#================
from publicTool import savePickle


print('step 1')

# 获得该目录下所有文件名
dataPath = 'D:/点击这里/Nanyang/data/' 
onlyfiles = [ dataPath+f for f in listdir(dataPath) if isfile(join(dataPath,f)) ]


# 维护一个全局mapping dict
mapping = {}

# 构造读取循环
for fileName in onlyfiles:
    with open(fileName,'r') as f:
        for line in f.readlines():
            # 只读取M 开头的line, 记下 monitor key
            if line.startswith('M')
                parts = line.strip().split(' ')
                ip = parts[1]
                number = parts[2]
                key = parts[3]
                if not (number,key) in list(mapping.keys()):
                    mapping[(number,key)] = ip
            if line.startswith('D'):
                break
print()
print(len(list(mapping.keys())))
print()
# 保存一次 pickle
savePickle(dataPath+'mapping',mapping)

print('step 2')

# 维护列表，每当到达1000的时候就追加写一次 txt


dataSet1 = []
dataSet2 = []
dataSet3 = []
dataSet4 = []

# 
mapplingKeys = list(mapping.keys())
# 构造读取循环
for fileName in onlyfiles:
    with open(fileName,'r') as f:
        for line in f.readlines():
            # 只读取M 开头的line, 记下 monitor key
            if line.startswith('D'):
                parts = line.strip().split('\t')
                fromNumber = parts[1]
                toNumber = parts[2]
                
                # from to 都在
                if fromNumber in mapplingKeys and toNumber in mapplingKeys:
                    #单纯数量
                    mapping
                    freq1 = 0
                    freq2 = 0
                    for i in range(3,len(parts)):
                        key = parts[i]
                        freq1 += int(key)
                        freq2 += 1
                    for fromIP, toIP in zip(mapping[fromNumber],mapping[toNumber]):
                        record1 = fromIP+' '+toIP+' '+freq1
                        dataSet1.append(record1)
                        #加入权重
                        record2 = fromIP+' '+toIP+' '+freq2
                        dataSet2.append(record2)

                # 只有from
                elif fromNumber in mapplingKeys:
                    freq1 = 0
                    freq2 = 0
                    for i in range(3,len(parts)):
                        key = parts[i]
                        freq1 += int(key)
                        freq2 += 1
                    for fromIP in zip(mapping[fromNumber]):
                        record3 = fromIP+' '+freq1
                        dataSet3.append(record3)
                        #加入权重
                        record4 = fromIP+' '+freq2
                        dataSet4.append(record4)
                else:
                    pass

            if line.startswith('I'):
                parts = line.strip().split('\t')
                fromNumber = parts[1]
                toNumber = parts[2]

                # from to 都在
                if fromNumber in mapplingKeys and toNumber in mapplingKeys:
                    #单纯数量
                    mapping
                    freq1 = 0
                    freq2 = 0
                    for i in range(4,len(parts)):
                        key = parts[i]
                        freq1 += int(key)
                        freq2 += 1
                    for fromIP, toIP in zip(mapping[fromNumber],mapping[toNumber]):
                        record1 = fromIP+' '+toIP+' '+freq1
                        dataSet1.append(record1)
                        #加入权重
                        record2 = fromIP+' '+toIP+' '+freq2
                        dataSet2.append(record2)

                # 只有from
                elif fromNumber in mapplingKeys:
                    freq1 = 0
                    freq2 = 0
                    for i in range(4,len(parts)):
                        key = parts[i]
                        freq1 += int(key)
                        freq2 += 1
                    for fromIP in zip(mapping[fromNumber]):
                        record3 = fromIP+' '+freq1
                        dataSet3.append(record3)
                        #加入权重
                        record4 = fromIP+' '+freq2
                        dataSet4.append(record4)
                else:
                    pass







