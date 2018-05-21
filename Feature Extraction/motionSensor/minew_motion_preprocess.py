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
    cnt = collections.Counter (macAddress )
    for k, v in cnt.items():
        if v > 500:
            sensors.append (k)
    print ('sensor num: ' + str(len(sensors)))
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
def saveData(classfiedData, sensors, reference):
    print ("*************************************************")
    print ("saving files")
    counter = 0
    buffer = dict()
    for mac in sensors:
        loc = reference.get(mac)
        fileName = loc +'_features' +'.csv'
        df = pandas.DataFrame(classfiedData[counter])
        if loc in buffer:
            print ("got a repeated location")
            #open the already existed file 
            #append to the end 
            with open(fileName, 'a') as f:
                df.to_csv(f, header=False, sep = ',')
                print (loc)             
        else:
            buffer.update ({loc: 1})
            counter += 1
            df.to_csv(fileName, sep=',')
            
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
def main(address):
    classfiedData = []
    sensors = []
    #save the current path
    currentAd = os.getcwd()
    #change to the new directory 
    os.chdir(address)
    fileName = 'motion.csv'
    mapFile = 'minews_owl_map.csv'
    classfiedData, sensors = loadData(fileName)
    reference = readMap(mapFile)
    saveData(classfiedData, sensors, reference)
    #go back to the orginal path 
    os.chdir(currentAd)

if __name__ == "__main__":
    if len(argv) < 2:
        print ("please input the directory of the files you want to process:")
    address = argv[1]
    print ("the address is: " + str(address))
    main(address)


