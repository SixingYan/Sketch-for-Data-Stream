"""
extract ipv4
"""
"""
Data example
T   192.172.226.37  32.158.127.63   1   1   1166139697  N   0   0   0   U   1   I   192.172.226.1,0.743,1   198.17.46.8,8.463,1 137.164.24.205,5.067,1  4.71.128.5,5.020,1  4.68.102.172,5.498,1    192.205.33.225,17.990,1 12.127.3.214,79.596,1   12.122.10.13,79.547,1   12.122.9.141,79.718,1   
"""

#===================  Import ->
# system
from os import listdir
from os.path import isfile, join
# DIY
#import tool
#===================  <- Import

#===================  path area ->
#homePath = ''
sourcePath = 'D:/点击这里/Nanyang/dataIPv4/t1_warts/' # use '/' as ending
destinationPath = ''
ds1Path = 'D:/点击这里/Nanyang/dataIPv4/t1/dataset1'
ds2Path = 'D:/点击这里/Nanyang/dataIPv4/t1/dataset2'
#===================  <- path area

# get the file name list
onlyfiles = [ f for f in listdir(sourcePath) if isfile(join(sourcePath,f))]
totalNum = len(onlyfiles)
print('Total number of files is '+str(totalNum))

percent = 0.1

print('start extracting...')
for k in range(totalNum):
    fileName = onlyfiles[k]

    if k/total> percent:
        print('now is '+str(int(100*percent))+'%')
        percent += 0.1

    dataset1 = []
    dataset2 = []
    try:
        with open(sourcePath+fileName,'r') as f:
            for line in f.readlines():
                # read line starts with T
                if line.startswith('T'):
                    parts = line.strip().split('\t')

                    # first type 
                    sourceIP = parts[1]
                    destiIP = parts[2]
                    freq = len(parts)-14
                    record1 = sourceIP+' '+destiIP+' '+str(freq)
                    dataset1.append(record1)

                    # second type
                    for i in range(13,len(parts)): 
                        respondIP = parts[i]
                        record2 = sourceIP +' '+ respondIP+' '+'1' #as default
                        dataset2.append(record2)
    #except IOError, error:
    except:
        print('reading fails: '+fileName)
        #print('Error is: '+str(error))
    else:
        pass
    
    # saving .... dataset 1
    try:
        ds1Path+'TXT_'+fileName
        with open(ds1Path,'a',encoding="utf-8") as f:
            for line in dataset1:
                f.write(line+'\n')
    #except IOError, error:
    except:
        print('writing fails: '+fileName)
        #print('Error is: '+str(error))
    else:
        pass

    # saving .... dataset 2
    try:
        with open(ds2Path,'a',encoding="utf-8") as f:
            for line in dataset2:
                f.write(line+'\n')
    #except IOError, error:
    except:
        print('writing fails: '+fileName)
        #print('Error is: '+str(error))
    else:
        pass
                    
    print('completed: '+fileName)












































































































