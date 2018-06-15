#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 09:21:27 2018

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
    #a list of unique sensors
    sensors = []
    #data stored in differnt lists according to their mac address
    classfiedData = []
    #read data
    accData = pandas.read_csv(fileName, sep = ',')
    #drop the battery percentage
    accData = accData.drop(columns = dropList)
   
    '''
    clear the bogus sensors
    there are 1300 different mac address in the motion file, but only a handful of them are
    real(i.e, has realiable data generated from a real motion sensors)
    the same is true for other two files
    '''
    macAddress = accData['macAddress']
    print (numpy.unique(macAddress))
    print (len (numpy.unique(macAddress)))
    cnt = collections.Counter (macAddress )
    '''
    if the sensors have more than 500 outputs, we consider it as a real sensor
    '''
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
def saveData(classfiedData, sensors, reference):
    print ("*************************************************")
    print ("saving files")
    counter = 0
    buffer = dict()
    for mac in sensors:
        loc = reference.get(mac)
        '''
        sensors without corresponding items in the owl_minew map are named differently
        '''
        if loc is None:
            loc = mac + '_Not_Found'
        fileName = loc   + '_features' +'.csv'
        df = pandas.DataFrame(classfiedData[counter])
        
        '''
        some times we have 2 sensors in one location
        '''
        if loc in buffer:
            print ("got a repeated location")
            #open the already existed file 
            #append to the end
            fileName = loc + '_1_features' + '.csv'
            df.to_csv(fileName, sep = ',')            
        else:
            buffer.update ({loc: 1})
            
            df.to_csv(fileName, sep=',')
        counter += 1
        
    print (str(counter) + " files are created with locations as file names")
    print ("done")
    print ("*************************************************")
  
    
'''
read the owl_minew map 
!!!!
!!!!please use minew_owl_v3.csv
!!!!
'''
def readMap (fileName):
    print ("*************************************************")
    print ("reading the map right now")
    mapData = pandas.read_csv(fileName, sep = ',')
    macAdress = mapData['Address']
    location = mapData['Directory']
    macLocMap = dict(zip(macAdress, location))
    
    print("**************************************************")
    return macLocMap
    
    
    
#run the program
def main(fileName,fileAddress, mapAddress, outputAddress):
    #fileAddress = '/Users/victorzhang/Desktop/Research/TILES/data/minew'
    #mapAddress = '/Users/victorzhang/Desktop/Research/TILES/data/minew'
    #outputAddress = '/Users/victorzhang/Desktop/Research/TILES/data/minew/motion_cleaned'
    classfiedData = []
    sensors = []
    #save the current path
    currentAd = os.getcwd()
    #change to the new directory 
    os.chdir(fileAddress)
    mapFile = 'mines_owl_map_v3.csv'
    classfiedData, sensors = loadData(fileName)
    os.chdir(mapAddress)
    reference = readMap(mapFile)
    os.chdir(outputAddress)
    saveData(classfiedData, sensors, reference)
    #go back to the orginal path 
    os.chdir(currentAd)


if __name__ == "__main__":
    print ('This code can clean all three types of minew data')
    if len(argv) < 5:
        print ('to run this code, you need motion.csv and owl_minew map')
        print ("file address + map address + output folder ")
    fileAddress = argv[1]
    mapAddress = argv[2]
    outputAddress = argv[3]
    fileName = argv[4]
    main(fileName, fileAddress, mapAddress, outputAddress)

