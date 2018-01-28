from scipy.special import comb

#comb(3, 2)

combDict = {}
combDict[0] = 1
combDict[1] = 1

for n in range(2,3):
    total = 0
    for i in range(0,n):
        total += comb((n-1),i) * combDict[n-1-i]
    combDict[n] = total




#1,2,5,15,52,203,877,4140,21147,115975,678570