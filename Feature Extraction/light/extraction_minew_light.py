"""
created on May 21 2018
For USC SAIL TILES
light feature extraction 
Aurthor: Victor Zixuan Zhang

"""

import pandas
import collections
from sys import argv
import os

""" 
read the data in the preprocessed file, split the data according to macadresses
parameters:
	fileName: the name of the file you want to open 
return:
	a list of data, each element is the data frame of one mac adress 
"""
def loadData(fileName):
    print ("*************************************************")
    print ("read input")
    #drop the battery percentage
    dropList = ['batteryPercent']
    #unique sensors
    sensors = []
    #data stored in differnt lists according to their mac address
    classfiedData = []
    #read data
    accData = pandas.read_csv(fileName, sep = ',')
    #drop the battery percentage
    accData = accData.drop(columns = dropList)
   
   	#get unique macAddresses
    macAddress = accData['macAddress']
    cnt = collections.Counter (macAddress )
    for k, v in cnt.items():
        if v > 500:
            sensors.append (k)
    print ('sensor num: ' + str(len(sensors)))

    df = accData.set_index(['macAddress'])  
    #put data from the same sensor into one list
    try:
        for item in sensors:
            classfiedData.append(df.loc[item])
            
    except ValueError:
        pass
    #done 
    print (classfiedData)
    print ("done")
    print ("*************************************************")
    return classfiedData, sensors

def main():
	path = '/home/victor/Desktop/TILES/data/light'
	os.chdir(path)
	loadData('light.csv')

main()