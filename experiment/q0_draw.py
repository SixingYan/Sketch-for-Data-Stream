homePath = 'C:/Users/alfonso.yan/Downloads/'
dataset = [
    ['comp16',homePath+'Q0_sketch_result_comp1012.pickle'],
    ['comp12',homePath+'Q0_sketch_result_comp1012.pickle'],
    ['comp1',homePath+'Q0_sketch_result_comp1012.pickle'],
]
resultSet = []

h = 500
sketch = 'cs'
w = 10
#prepare data
for ds in dataset:
    dataName = ds[0]
    result_path = ds[1]

    ratio = []
    for record in loadPickle(result_path):
        if record['ds']==dataName and record['h']==h and record['w']==w and record['sketch']==sketch:
            resultSet.append(record['ratio'])
            break

plt.figure(1)
Epsilon = [i+2 for i in range(10)]
standard = [1-1/((e**2)**w) for e in Epsilon]

for k in range(len(dataset)):
    diff = [abs(resultSet[k][i]-standard[i])/standard[i] for i in range(10)]
    plt.plot(range(2,12),diff,label=dataset[k][0],marker='v',linestyle='--')















diff = []
for i in range(10):
    if i == 0:
        continue
    diff.append(abs(comp18[i]-standard[i])/standard[i])
plt.plot(range(2,11),diff,label='comp18-cs',c='red',marker='v',linestyle='--')
diff = []
for i in range(10):
    if i == 0:
        continue
    diff.append(abs(comp16[i]-standard[i])/standard[i])
plt.plot(range(2,11),diff,label='comp16-cs',c='blue',marker='<',linestyle='--')






'''
diff = []
for i in range(10):
    if i == 0:
        continue
    diff.append(abs(comp1[i]-standard[i])/standard[i])
plt.plot(range(2,11),diff,label='comp1-cs',c='green',marker='*',linestyle='--')
'''
comp18=[0.99986242000000014,
  0.9999158600000001,
  0.9999351666666666,
  0.99994606666666674,
  0.99995376000000014,
  0.99995959333333317,
  0.99996354666666654,
  0.99996656666666672,
  0.99996932000000016,
  0.99997177333333342]
comp16 = [0.99991848666666672,
  0.99994713999999996,
  0.99996004000000005,
  0.99996659333333326,
  0.99997110666666666,
  0.99997410666666675,
  0.99997665333333341,
  0.99997900666666661,
  0.99998046666666662,
  0.99998181333333336]
comp1 = [0.99875762666666668,
  0.99943439999999995,
  0.99964429333333327,
  0.99973791999999995,
  0.99979287999999988,
  0.99983392000000004,
  0.99985847999999999,
  0.99987402666666658,
  0.99988877333333315,
  0.99989970666666661]
standard = [1-1/((e**2)**10) for e in Epsilon]

diff = []
for i in range(10):
    if i == 0:
        continue
    diff.append(abs(comp18[i]-standard[i])/standard[i])
plt.plot(range(2,11),diff,label='comp18-gm',c='red',marker='o',linestyle='-')

diff = []
for i in range(10):
    if i == 0:
        continue
    diff.append(abs(comp16[i]-standard[i])/standard[i])
plt.plot(range(2,11),diff,label='comp16-gm',c='blue',marker='*',linestyle='-')
'''
diff = []
for i in range(10):
    if i == 0:
        continue
    diff.append(abs(comp1[i]-standard[i])/standard[i])
plt.plot(range(2,11),diff,label='comp1-gm',c='green',marker='h',linestyle='-')
'''
plt.xlabel("Epsilon")
plt.ylabel("Relative Efficiency")
plt.title("w=15, h=1000")  
plt.legend()
plt.show()
