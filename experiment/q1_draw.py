import matplotlib.pyplot as plt
import diyTool
homePath = 'D:/Alfonso Ngan/Documents/Github Project/Sketch-for-Data-Stream/experiment/result/'
dataset = [
    #['comp12',homePath+'Q0_sketch_result_comp1012.pickle'],
    ['comp18',homePath+'Q1_percentSketch_set_comp18.pickle'],
    ['comp16',homePath+'Q1_percentSketch_set_comp16.pickle'],
    ['comp14',homePath+'Q1_percentSketch_set_comp14.pickle'],
    ['tweet',homePath+'Q1_percentSketch_set_.pickle'],
    ['ip',homePath+'Q1_percentSketch_set_.pickle'],
]
resultSet = []

h = 1000
sketch = 'cs'
w = 10
figureID = 1

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
        if record['dataset']==dataName and record['h']==h and record['w']==w and record['sketch']==sketch:
            resultSet.append(record['medium_ratio'])
            break

#for i in range(len(percent)):

ax = [(0,0),(0,1),(1,0),(1,1)]
markerList = ['|','o','*','p','d','>','v','+','x']
#wholeName = ["Rad Query: Coverage percent","Top Query: Coverage percent","Rad Query: Relaive-bias percent","Top Query: Relaive-bias percent"]
plt.figure(figureID); figureID += 1
tPlot, axes = plt.subplots(nrows=1, ncols=3,figsize=(15,4))
tPlot.tight_layout(renderer=None, pad=2, h_pad=2, w_pad=2, rect=None)   

for k in range(len(Epsilon)):
    e = Epsilon[k]
    standard = [1-(n/(e**2))**w for n in nSet]
    for j in range(len(dataset)):
        diff = [abs(resultSet[j][i]-standard[i])/standard[i] for i in range(len(standard))]
        axes[k].plot(percent,diff,label=dataset[k][0],marker=markerList[n],markersize=9, linestyle='--',lw=4)
        axes[k].set_xlabel('query size')
        axes[k].set_ylabel('ratio value')
        axes[k].set_xticks(percent)
        axes[k].set_xticklabels(percent)

plt.xlabel("Epsilon")
plt.ylabel("Relative Efficiency")
plt.title("w=15, h=1000")  
plt.legend()
plt.show()
        




























