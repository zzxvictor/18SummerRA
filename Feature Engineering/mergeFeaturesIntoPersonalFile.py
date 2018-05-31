#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 26 11:25:28 2018

@author: victorzhang
"""
#libraries 
import os
import pandas
import datetime 
import numpy
from sys import argv
"""
scan .csv files and return the names of the files in a list
parameter:
    directory: which folder you want to scan
return
    nameList: file names in a list
"""
def scanCSVNames(directory):
    print ("scanning")
    fileNames = [x for x in os.listdir(directory) if x.endswith(".csv")]
    return fileNames 

"""
read an individual file, drop the unnecessary features, and return the dataFrame
parameter:
    fileName: the name of the file
    directory: where the files are 
return:
    dataFrame: the dataFrame contains the information stored in the file (some features may be dropped)
"""
def readAnIndividualFile (fileName, directory):
    print("reading an individual file rn")
    #get the current path
    currentPath = os.getcwd()
    #change to the target folder 
    os.chdir(directory)
    #read the data
    dataFrame = pandas.read_csv(fileName, sep = ',')
    #features that we don't want to keep 
    dropList = ['ProximityCertainty','AtNursingStation', 'AtPatientRoom', 'AtLounge', 'AtMedicineRoom','AtLabRoom', 'AtReceivingRoom' ]
    dataFrame = dataFrame.drop (columns = dropList)
    #change back to the original folder
    os.chdir(currentPath)
    return dataFrame
    
"""
read all the temp-hum files and create a map which uses locations as keys
parameter:
    directory: where the files are 
return:
    tempHumMap: a map in which nurseID are keys and each key corresponds to a chunk of dataFrame(different timestamps)
"""
def readAllTempHumFiles(directory):
    print ("read the tempHum files and creating the map rn")
    currentPath = os.getcwd()
    #change to the new directory
    os.chdir(directory)
    tempHumFiles = scanCSVNames(directory)
    tempHumMap = {}
    for files in tempHumFiles:
        nurseID = files.split('_')[0]
        dataFrame = pandas.read_csv(files, sep = ',')
        if nurseID in tempHumMap:
            #add
            tempDataFrame = tempHumMap.get(nurseID)
            tempDataFrame = tempDataFrame.append(dataFrame)
            #update
            tempHumMap.update({nurseID: tempDataFrame})
        else:
            #create a new key
             tempHumMap.update({nurseID: dataFrame})
            
    #change back to the original path
    os.chdir(currentPath)
    return tempHumMap
"""
read all the motion files and create a map which uses locations as keys
parameter:
    directory: where the files are 
return:
    motionMap: a map in which locations are keys and each key corresponds to a chunk of dataFrame(different timestamps)
"""
def readAllMotionFiles(directory):
    print ("read the motion files and creating the map rn")
    currentPath = os.getcwd()
    #change to the new directory
    os.chdir(directory)
    motionFiles = scanCSVNames(directory)
    motionMap = {}
    for fileName in motionFiles:
        #make sure they are all motion files 
        location = fileName.split('_')[0]
        if location.split(':')[0] =='keck':
            #open a file, add the data frame to the dictionary 
            dataFrame =  pandas.read_csv(fileName, sep = ',')
            if location in motionMap:
                #add new row 
                tempDataFrame = motionMap.get(location)
                tempDataFrame = tempDataFrame.append(dataFrame)
                #update 
                motionMap.update({location: tempDataFrame})
                #else add the rowData to the dataFrame location corresponds to 
            else:
                #create a new key:
                motionMap.update({location: dataFrame})
    
    #change back to the original path
    os.chdir(currentPath)
    return motionMap
    

"""
read all the motion files and create a map which uses locations as keys
parameter:
    directory: where the files are 
return:
    lightMap: a map in which locations are keys and each key corresponds to a chunk of dataFrame(different timestamps)
"""
def readAllLightFiles(directory):
    print ("read the light files and creating the map rn")
    fileName = 'light_features.csv'
    currentPath = os.getcwd()
    os.chdir(directory)
    #read the file
    dataFrame =  pandas.read_csv(fileName, sep = ',')
    locaList = dataFrame['sensorLocation']
    timeSeries = dataFrame['timeStamp']
    quietHour = dataFrame['quietHour']
    #delete the dataFrame,save some memory 
    del dataFrame
    lightMap = {}
    counter = 0
    for loc, time, light in zip (locaList, timeSeries, quietHour):
        
        if loc in lightMap:
            #update the infor 
            tempList = lightMap.get(loc)
            #timeStamp
            tempList[0].append(time)
            tempList[1].append(light)
            #update
            lightMap.update({loc: tempList})
            del tempList
        else:
            timeList = [time]
            lightList = [light]
            tempList = [timeList, lightList]
            lightMap.update({loc: tempList})
        counter += 1
            
    """
    for row in range (len (dataFrame)):
        if row%200 == 0:
            print(str(row/len(dataFrame) * 100) + ' %percent ')
        rowData = dataFrame.loc[row, :]
        location = locaList[row]    
        #if location is not in the map, then add a new key    
        if location in lightMap:
            #add new row 
            #tempDataFrame = lightMap.get(location).append (rowData)
            
            #tempDataFrame = tempDataFrame.append(rowData)
            #update 
            lightMap.update({location: lightMap.get(location).append (rowData)})
            #print (tempDataFrame)
        #else add the rowData to the dataFrame location corresponds to 
        else:
            #create a new key:
            rowData = rowData.to_frame()
            lightMap.update({location: rowData})
    """
    #change back to the current path 
    
    os.chdir(currentPath)
    return lightMap
"""
find the temp-hum value, motion sensor status and light sensors outputs of a givin location and time
parameter:
    timePoint: the specific time we want to check
    location: the specific location where the nurse was
    tempHumMap: temp-hum map, which is used to check the surronding temp-hum value
    motionMap: motion Map, whic is used to evaluate how croweded/busy/distracting the environment was at a given time
    lightMap: light map, which is used to check the brightness of the environment
    
return: 
    temValue:the temp value of the environment corresponds to the time and location
    humValue: the humitity value of the environment corresponds to the time and location
    distractPara:the distraction of the environment corresponds to the time and location
    brightness:the brightness of the environment corresponds to the time and location
"""
def obtainRelevantFeatures(timePoint, location, nurseID, tempHumMap, motionMap, lightMap, window):
    #use timePoint, location and nurseID to find the temp and humidity values 
    
    temp, hum = getTemHumValue(timePoint, location, nurseID, tempHumMap)
    #use timePoint, location to find the brightness of the environment 
    brightness = getLightValue (timePoint, location, lightMap)
    #use timePoint, location to find the distraction level of the environment
    distraction = getDistractionValue(timePoint, location, motionMap, window)
    #return the values 
    
    return temp, hum, distraction, brightness

"""
look up the map, find the information needed
parameter: 
    timePoint:  when 
    location: where
    nurseID: key 
    iMap: the dictionary 
return 
    temp, hum 
"""
def getTemHumValue(timePoint, location, nurseID, iMap):
    #get the dataFrame using keys
    dataFrame = iMap.get(nurseID)
    if dataFrame is None:
         return numpy.nan
    #search the dataFrame using binary search 
    first = 0
    last = int (len(dataFrame))
    targetTime = datetime.datetime.strptime(timePoint, '%Y-%m-%dT%H:%M:%S.%f')
    while(1):
        mid = int ((first + last)/2)
        time1 = datetime.datetime.strptime(dataFrame['Timestamp'][mid], '%Y-%m-%dT%H:%M:%S.%f')
        if time1 < targetTime - datetime.timedelta(seconds = 1):
            first = mid + 1
        elif time1 > targetTime + datetime.timedelta(minutes = 1):
            last = mid - 1   
        else:
            break
        if last - first <=1:
            break
    temp = dataFrame['Temperature'][mid]
    hum = dataFrame['Humidity'][mid] 
    return temp, hum

"""
look up the map, find the information needed
parameter: 
    timePoint:  when 
    location: where 
    iMap: the dictionary 
return 
    light
"""
def getLightValue (timePoint, location, iMap):
    #get the dataFrame using keys
    dataFrame = iMap.get(location)
    if dataFrame is None:
        #print ('*****'+location + '*****')
        return numpy.nan
    timeList = dataFrame[0]
    lightList = dataFrame[1]
    del dataFrame
    
    #search the dataFrame using binary search 
    first = 0
    last = int (len(timeList))
    targetTime = datetime.datetime.strptime(timePoint, '%Y-%m-%dT%H:%M:%S.%f')
    while(1):
        mid = int ((first + last)/2)
      
        time1 = datetime.datetime.strptime(timeList[mid], '%Y-%m-%dT%H:%M:%S.%f')
        
        if time1 < targetTime - datetime.timedelta(seconds = 1):
            first = mid + 1
        elif time1 > targetTime + datetime.timedelta(minutes = 1):
            last = mid - 1   
        else:
            break
        if last - first <=1:
            break
    light = lightList[mid]
    return light

"""
look up the map, find the information needed
parameter: 
    timePoint:  when 
    location: where
    iMap: the dictionary 
return 
    motion
"""

def getDistractionValue(timePoint, location, iMap, window):
    #get the dataFrame using keys
    dataFrame = iMap.get(location)
    if dataFrame is None :
        #print ('----'+location + '----')
         return numpy.nan
    #search the dataFrame using binary search 
    first = 0
    last = int (len(dataFrame))
    targetTime = datetime.datetime.strptime(timePoint, '%Y-%m-%dT%H:%M:%S.%f')
    while(1):
        mid = int ((first + last)/2)
        time1 = datetime.datetime.strptime(dataFrame['Timestamp'][mid], '%Y-%m-%dT%H:%M:%S.%f')
        if time1 < targetTime:
            first = mid + 1
        elif time1 > targetTime:
            last = mid - 1
        else:
            break
        if last - first <=1:
            break 
    motion = dataFrame['doorStatus'][mid]
    i = 0
    window = int (window)
    while (1):
        time1 = datetime.datetime.strptime(dataFrame['Timestamp'][max (mid-i,0)], '%Y-%m-%dT%H:%M:%S.%f')
        #time2 = datetime.datetime.strptime(dataFrame['Timestamp'][min (mid+i,len (dataFrame)-1)], '%Y-%m-%dT%H:%M:%S.%f')
        #if (time1>targetTime-datetime.timedelta(minutes = window)):
         #   motion +=  dataFrame['doorStatus'][max (mid-i,0)]
        #if (time2<targetTime+datetime.timedelta(minutes = window)):
        #    motion +=  dataFrame['doorStatus'][min (mid+i,len (dataFrame)-1)] 
        i+=1 
        if time1<targetTime-datetime.timedelta(minutes = window)  or i > 2000:
            break

    return motion

"""
add features to the original dataFrame and save it into a new file in a given folder
parameter:
    dataFrame: the personal data we need to process
    fileName: the file contains the dataFrame
    directory: where do you want to store the newly-generated file
return:
    N/A
"""
def addNewFeaturesToFile(dataFrame, directory, fileName, tempHumMap, motionMap,lightMap, window):
    print ("going throught a file rn")
    #get time
    timeStamp = dataFrame['Timestamp']
    #get location
    location = dataFrame['NearestProximity']
    #environmental features 
    tempList = []
    humList = []
    distractionList = []
    brightnessList = []
    #get nurseID 
    nurseID = fileName.split('_')[0]
    #go through each row
    counter = 0
    for timePoint, currentSpot in zip(timeStamp, location):
        if counter %1000 == 0:
            print ("*", end = '')
        tempCo, humCo, distractionCo, brightnessCo = obtainRelevantFeatures(timePoint, currentSpot, nurseID, tempHumMap, motionMap, lightMap, window)
        tempList.append(tempCo)
        humList.append(humCo)
        distractionList.append(distractionCo)
        brightnessList.append(brightnessCo)
        counter += 1
    
    #add to the dataFrame
    dataFrame['tempValue'] = tempList
    dataFrame['humValue'] = humList
    dataFrame['distraction'] = distractionList
    dataFrame['brightness'] = brightnessList
    
    newFileName = nurseID + '_environmentalFeatures.csv'
    print ('*')
    print ("saving the file ")
    saveAFile (newFileName,dataFrame, directory)
"""
save the data into the given folder with a new name passed into the function
parameter:
    dataFrame: the personal data we need to save
    newName: the new name of the file
    directory: where do you want to store the newly-generated file
return:
    1: saving successeed
    -1: failed
"""
def saveAFile(newName, dataFrame, directory):
    print ("fliename:" + newName)
    print ("directory:" + directory)
    currentPath = os.getcwd()
    os.chdir(directory)
    dataFrame.to_csv(newName, sep = ',', index = False )
    os.chdir(currentPath)
    
"""
main file, process controlling
"""
def main(tempHumDirectory, motionDirectory, lightDirectory, nurseDirectory, storageDirectory, window):
    """
    #default setting for  computer
    tempHumDirectory = '/Users/victorzhang/Desktop/Research/TILES/data/minew/minew/temHumFeature'
    motionDirectory = '/Users/victorzhang/Desktop/Research/TILES/data/minew/minew/motionFeature'
    lightDirectory = '/Users/victorzhang/Desktop/Research/TILES/data/minew/minew/lightFeature'
    nurseDirectory = '/Users/victorzhang/Desktop/Research/TILES/data/owl_in_one'
    storageDirectory = '/Users/victorzhang/Desktop/Research/TILES/data/processedOWL'
    """
    #get the maps
    tempHumMap = readAllTempHumFiles(tempHumDirectory)
    motionMap = readAllMotionFiles(motionDirectory)
    lightMap = readAllLightFiles(lightDirectory)
    #scan for the individual data files
    nurseNameList = scanCSVNames(nurseDirectory)
    #for loop, one file at a time
    counter = 0
    for nurse in nurseNameList:
        counter += 1
        print (str(counter/len(nurseNameList) * 100) + '% of the files has been processed')
        dataFrame = readAnIndividualFile(nurse, nurseDirectory)
        addNewFeaturesToFile(dataFrame, storageDirectory, nurse, tempHumMap, motionMap,lightMap, window)
    
    print ("done")
    
if __name__ == "__main__":
    if len(argv) < 7:
        print ("input format(no comma, just whitespace): ")
        print ("absolute path to the temperature and humidity data file, ", end = '')
        print ("the motionFeature file, ", end = '')
        print ("the lightFeature file, ", end = '')
        print ("the nurse files, the folder you want to store the results, and the length of the window(used for generating the distraction feautre)")

    
    tempHumDirectory = argv[1]
    motionDirectory = argv[2]
    lightDirectory = argv[3]
    nurseDirectory = argv[4]
    storageDirectory = argv[5]
    window = argv[6]
    main(tempHumDirectory, motionDirectory, lightDirectory, nurseDirectory, storageDirectory, window)