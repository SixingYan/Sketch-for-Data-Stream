import matplotlib.pyplot as plt
import diyTool
homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment/result/'
dataset = [
    ['comp16',homePath+'Q1_percentSketch_set_comp16.pickle'],
    #['comp12',homePath+'Q0_sketch_result_comp1012.pickle'],
    ['comp18',homePath+'Q1_percentSketch_set_comp18.pickle'],
    ['comp14',homePath+'Q1_percentSketch_set_comp14.pickle'],
    ['tweet',homePath+'Q1_percentSketch_set_.pickle'],
    ['ip',homePath+'Q1_percentSketch_set_.pickle'],
]
resultSet = []

h = 1000
sketch = 'cs'
w = 10


plt.figure(1)
Epsilon = [3,5,10]
standard = [1-1/((e**2)**w) for e in Epsilon]
percent = [0.001, 0.003, 0.005, 0.01, 0.03, 0.05, 0.1, 0.2]
nSet = [int(1/percent[i]) for i in range(len(percent))]


for ds in dataset:
    dataName = ds[0]
    result_path = ds[1]

    ratio = []
    for record in loadPickle(result_path):
        if record['ds']==dataName and record['h']==h and record['w']==w and record['sketch']==sketch:
            resultSet.append(record['ratio'])
            break

for i in range(len(percent)):
for e in Epsilon:

    standard = [1-(n/(e**2))**w for n in nSet]
    for 
        diff = [abs(resultSet[k][i]-standard[i])/standard[i] for i in range(10)]
        
        plt.plot(range(2,12),diff,label=dataset[k][0],marker='v',linestyle='--')

#plt.xlabel("Epsilon")
#plt.ylabel("Relative Efficiency")
#plt.title("w=15, h=1000")  
plt.legend()
plt.show()
        




























