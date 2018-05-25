#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on May 25 2018
For USC SAIL TILES
light feature extraction 
Aurthor: Victor Zixuan Zhang

"""
import os
import pandas 
import re

def loadFile(dataDirectory, dataFile):
    print ("*************************************************")
    print ("reading input")
    #save the current directory
    currentDirectory = os.getcwd()
    #change to the target folder 
    os.chdir(dataDirectory)
    #read the file
    dataFrame = pandas.read_csv(dataFile, sep = ',')
    #drop the the useless column
    #dropList = ['batteryPercent']
    #dataFrame = dataFrame.drop(columns = dropList)
    #change back to the previous folder
    os.chdir(currentDirectory)
    #return the dataFrame
    return dataFrame
    
    
def loadMap(mapDirectory, mapFile):
    print ("*************************************************")
    print ("reading map")
    #save the current directory
    currentDirectory = os.getcwd()
    #change to the target folder 
    os.chdir(mapDirectory)
    #read the file
    mapFrame = pandas.read_csv(mapFile, sep = ',')
    #change back to the previous folder
    os.chdir(currentDirectory)
    #zip 
    lightData = mapFrame.loc[mapFrame['Type']== 'light' ]
    macAdress = lightData['Address']
    location = lightData['Directory']
    macLocMap = dict(zip(macAdress, location))
    #return the dataFrame
    return macLocMap
    
def checkQuietHour(time,loc):
    location = loc.split(':')
    hour = re.split('[-T:.]', time)[3]
    hour = int (hour)
    if location[1] == 'floor9' and location[2] == 'east' and (hour>=23 or hour<4):
        return 1
    elif location[1] == 'floor7' and location[2] == 'south' and ((hour>=2 and hour<4) or (hour >= 14 and hour < 16) ):
        return 1
    elif location[1] == 'floor6' and (location[2] == 'east' or location[2] == 'west') and (hour>=23 or hour<4):
        return 1
    else:
        return 0
    
def checkLoc(macAddress, mapFrame):
    location = mapFrame.get(macAddress)
    if location == None:
        return 'keck:mac:not:found'
    else:
        return location

def process(dataFrame, mapFrame, newDirectory):
    print ("*************************************************")
    print ("processing")
    #go through the dataFrame row by row
    size = len(dataFrame)
    timeStamp = []
    location = []
    quietHour = []
    macAddress = dataFrame['macAddress']
    time = dataFrame['Timestamp']
    for row in range (len (dataFrame)):
        #replace the macAddress with its physical location
        loc = checkLoc( macAddress[row],mapFrame)
        if loc == 'keck:mac:not:found':
            continue 
        else:
            location.append(loc)
            quietHour.append( checkQuietHour(time[row],location[-1]))
            timeStamp.append(time[row])
        if row%1000 == 0:
            print ('.', end = '')
        if (row%50000 == 0):
            print('')
            print (str(row/size *100) + '% done')

    d = {'quietHour': quietHour ,'timeStamp':timeStamp, 'sensorLocation':location}
    newDataFrame= pandas.DataFrame(data = d)
    saveFiles(newDataFrame, newDirectory)
    
def saveFiles(data, directory):
    print ("*************************************************")
    print ("saving files")
    #save the current directory
    currentDirectory = os.getcwd()
    #change to the target folder 
    os.chdir(directory)
    #read the file
    header = ['timeStamp','sensorLocation','quietHour']
    data.to_csv('light_features.csv', sep = ',', index = False , columns = header)
    os.chdir(currentDirectory)
    print ("done")
    
def main():
    dataDirectory = '/Users/victorzhang/Desktop/Research/TILES/minew'
    dataFile = 'keck:floor6:north:ns01_feature.csv'
    mapDirectory = '/Users/victorzhang/Desktop/Research/TILES/minew'
    mapFile = 'minews_owl_map.csv'
    dataFrame = loadFile(dataDirectory, dataFile)
    mapFrame = loadMap(mapDirectory, mapFile)
    process(dataFrame, mapFrame, dataDirectory)

main()
    
    
    