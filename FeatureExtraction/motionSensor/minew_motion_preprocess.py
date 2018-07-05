#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 11:20:09 2018
read accelerometery data and save them into differnt csv files
@author: victorzhang
"""

import os
import pandas
import collections 
from sys import argv
import numpy
#load the data, pass it into a list 
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
   
    #clear the bogus sensors
    macAddress = accData['macAddress']
    print (numpy.unique(macAddress))
    print (len (numpy.unique(macAddress)))
    cnt = collections.Counter (macAddress )
    for k, v in cnt.items():
        if v > 500:
            sensors.append (k)
    print ('sensor num: ' + str(len(sensors)))
    print (sensors)
    df = accData.set_index(['macAddress'])  
    #put data of the same node into one list
    try:
        for item in sensors:
            classfiedData.append(df.loc[item])
            
    except ValueError:
        pass
    #done 
    print ("done")
    print ("*************************************************")
    return classfiedData, sensors

    
#save the data into different files
def saveData(outPath, classfiedData, sensors, reference):
    print ("*************************************************")
    print ("saving files")
    counter = 0
    buffer = dict()
    for mac in sensors:
        loc = reference.get(mac)
        if loc is None:
            loc = mac + '_NNNN'
        fileName = loc   + '_features' +'.csv'
        df = pandas.DataFrame(classfiedData[counter])
        if loc in buffer:
            print ("got a repeated location")
            #open the already existed file 
            #append to the end
            fileName = loc + '_1_features' + '.csv'
            df.to_csv(outPath + '/' + fileName, sep = ',')            
        else:
            buffer.update ({loc: 1})
            df.to_csv(outPath + '/' +fileName, sep=',')
        counter += 1
    print (str(counter) + " files are created with locations as file names")
    print ("done")
    print ("*************************************************")
  
def readMap (fileName):
    print ("*************************************************")
    print ("reading the map right now")
    mapData = pandas.read_csv(fileName, sep = ',')
    macAdress = mapData['Address']
    location = mapData['Directory']
    macLocMap = dict(zip(macAdress, location))
    
    print("**************************************************")
    return macLocMap
    #merge into a map
    
    
    
#run the program
def main(fileAddress, mapAddress, outputAddress):
    #fileAddress = '/home/victor/Desktop/TILES/data/light'
    #mapAddress = '/home/victor/Desktop/TILES/data/owl_minew_map'
    #outputAddress = '/home/victor/Desktop/TILES/data/owl_minew_map/light'
    classfiedData = []
    sensors = []
    #save the current path
    #currentAd = os.getcwd()
    #change to the new directory 
    #os.chdir(fileAddress)
    #fileName = 'light.csv'
    #mapFile = 'minews_owl_map_v2.csv'
    classfiedData, sensors = loadData(fileName)
    #os.chdir(mapAddress)
    reference = readMap(mapFile)
    #os.chdir(outputAddress)
    saveData(outputAddress, classfiedData, sensors, reference)
    #go back to the orginal path 
    os.chdir(currentAd)
main()

if __name__ == "__main__":
    if len(argv) < 4:
        print ("please input the directory of the files you want to process:")
    else:
        inPath = argv[1]
        mapPath = argv[2]
        outPath = argv[3]
        main(inPath, mapPath,outPath)


