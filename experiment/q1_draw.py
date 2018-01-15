




plt.figure(1)
Epsilon = [3,5,10]
standard = [1-1/((e**2)**w) for e in Epsilon]
percent = [,0.1,0.2]


for ds in dataset:
    dataName = ds[0]
    result_path = ds[1]

    ratio = []
    for record in loadPickle(result_path):
        if record['ds']==dataName and record['h']==h and record['w']==w and record['sketch']==sketch:
            resultSet.append(record['ratio'])
            break




























