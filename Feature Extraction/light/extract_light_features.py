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
from sys import argv

"""
load the light.csv file and return the dataframe
parameters:
    dataDirectory: the path to the file
    dataFile: the file's name(it should be light.csv)
return:
    dataFrame: the data in the dataFile
"""
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
    
"""
load the minew-owl map file, creates a map (macAddress as keys and locations as values) and return the map
parameters:
    mapDirectory: the path to the file
    mapFile: the file's name(it should be minews_owl_map.csv)
return:
    macLocMap: the mac-location dictionary
"""
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

"""
check the quiet hour according to them light out information provided by nurses
parameters:
    time: the timePoint you want to check
    loc: the location you want to check 
return:
    0: light on
    1: light off
"""
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

"""
check the physical location of a sensor using its macAddress and the mac-loc map 
parameter:
    macAddress: the macAddress of the sensor 
    mapFrame: the mac-loc dictionary 
return:
    location: the location of the sensor
    if not found, return 'keck:mac:not:found' (sometimes it does happen...)
"""
def checkLoc(macAddress, mapFrame):
    location = mapFrame.get(macAddress)
    if location == None:
        return 'keck:mac:not:found'
    else:
        return location
    
"""
control the code flow, connect each functions together
parameter:
    dataFrame: the raw data read from the original light.csv file
    mapFrame: the map created by the loadMap function 
return :
    N/A

"""
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
            #print (macAddress[row])
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

"""
save the modified light.csv files
parameters:
    data: the data you want to save
    directory: where do you want to put the file
return:
    N/A
"""  
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
    
def main(fileName, dataDirectory, mapName, mapDirectory, newDirectory):
    dataFrame = loadFile(dataDirectory, fileName)
    mapFrame = loadMap(mapDirectory, mapName)
    process(dataFrame, mapFrame, newDirectory)

if __name__ == '__main__':
    if len(argv) < 6:
        print ('please input parameters in this format: ')
        print ('the name of the file that contains light sensors data + its directory(absolute path) + minew-owl-maps name + its path + the folder in which you out the new results ')
    else:
        fileName = argv[1]
        dataDirectory =argv[2]
        mapName = argv[3]
        mapDirectory = argv[4]
        newDirectory = argv[5]
        main (fileName, dataDirectory, mapName, mapDirectory, newDirectory)