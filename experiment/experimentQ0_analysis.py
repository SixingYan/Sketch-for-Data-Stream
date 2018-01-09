
loadPickle()
expectProb = []
def getRecord(sketchDict,h,w,sName,dsName):
    #
    meanRatio = []
    stdRatio = []
    for ky in list(sketchDict.keys()):
        if sketchDict[key]['h']==h and sketchDict[key]['w']==w and sketchDict[key]['sketch']==sName and sketchDict[key]['dataset']==dsName:
            meanRatio = sketchDict[key]['MEANratio']
            stdRatio = sketchDict[key]['STDratio']
    return meanRatio, stdRatio

def evaluate(meanRatio):
    #
    evaluateResult = []
    for i in range(len(meanRatio)):
        value = abs(meanRatio[i]-expectProb[i])/expectProb[i]
        evaluateResult.append(value)
    return evaluateResult

def getExpectProb():
    #
    ep = []
    return ep

def drawStackingDiagram():

    pass

expectProb = getExpectProb()

wSet = [10,15]
hSet = [300,500,1000]
sketchName = ['cs','gm']
figNum = 1
for w in wSet:
    for h in hSet:
        plt.figure(figNum)
        figNum += 1d
        for sName in sketchName:
            []

            break
        break
    break





