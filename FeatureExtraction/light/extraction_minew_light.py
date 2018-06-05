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
import re

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
        if v > 8000:
            sensors.append (k)
    print ('sensor num: ' + str(len(sensors)))

    df = accData.set_index(['macAddress'])  
    #put data from the same sensor into one list
    try:
        for item in sensors:
            classfiedData.append(df.loc[item])
            
    except ValueError:
        pass
    
    #zip into one single dict
    sensorData = dict(zip(sensors, classfiedData))
    #done 
    print ("done")
    print ("*************************************************")
    return sensorData

"""
read the reference file which indicates the locations of the sensors 
parameters:
    fileName: the name of the file you want to open
    sensorName: the mac addresses of the light sensors 
return:
    a map which correpsonds the location and the mac addresses
"""
def loadReference (fileName):
    print ("*************************************************")
    print ("reading the map right now")
    mapData = pandas.read_csv(fileName, sep = ',')
    lightData = mapData.loc[mapData['Type']== 'light' ]
    macAdress = lightData['Address']
    location = lightData['Directory']
    macLocMap = dict(zip(macAdress, location))
            
    print("**************************************************")
    return macLocMap
    #merge into a map


"""
append the ideal light status according to the quiet hour
parameter:
    dataList: the dictionary contains macAddress and correspionding data
    macLocMap: the dictionary corresponds macAddress with locations in the hospital
return:
    processedData: the new data with a new column called "quietHourPeriod"
"""

def checkQuietHour(dataList, macLocMap):
    for key in dataList:
        #for each mac address in the dataList, check its location
        loc = macLocMap.get(key)
        #in case there are some bogus mac address that do not appear in the macLocMap
        if loc == None:
            continue 
        #split the name of the location
        location = loc.split(':')
        #add quiet hour feature
        #get the sensor data
        dataFrame = dataList.get(key)
        #get the time series 
        time = dataFrame['Timestamp']
        sensorOut = dataFrame['visibleLight']
        quietHour = []
        dayCounter = 0
        correctDayCounter = 0
        nightCounter = 0
        correctNightCounter = 0
            
        if (location[1] == 'floor9' and location[2] == 'east'):
            print (key)
            print (location)
            for timePoint, sensorStatus in zip (time, sensorOut):
            #for each time point
            #get the hour
                hour = re.split('[-T:.]', timePoint)[3]
                #if it's quiet hour
                if int(hour) >= 23 or int(hour) <4:
                    quietHour.append(True)
                    nightCounter += 1
                    if sensorStatus == False:
                        correctNightCounter += 1
                else:
                    quietHour.append(False)
                    dayCounter += 1
                    if sensorStatus == True:
                        correctDayCounter += 1
            dataFrame['quietHour'] = quietHour                  
            print ("day time Accuracy: " + str(correctDayCounter/dayCounter))
            print ("night time Accuracy: " + str(correctNightCounter/nightCounter))
            fileName = loc + '_feature' + '.csv'
            dataFrame.to_csv(fileName, sep = ',')
        elif location[1] == 'floor7' and location[2] == 'south':
            print (key)
            print (location)
            for timePoint, sensorStatus in zip (time, sensorOut):
            #for each time point
            #get the hour
                hour = re.split('[-T:.]', timePoint)[3]
                #if it's quiet hour
                if (int(hour) >= 2 and int(hour) <4) or (int(hour) >= 14 and int(hour) <16):
                    quietHour.append(True)
                    nightCounter += 1
                    if sensorStatus == False:
                        correctNightCounter += 1
                else:
                    quietHour.append(False)
                    dayCounter += 1
                    if sensorStatus == True:
                        correctDayCounter += 1
            dataFrame['quietHour'] = quietHour                       
            print ("day time Accuracy: " + str(correctDayCounter/dayCounter))
            print ("night time Accuracy: " + str(correctNightCounter/nightCounter))
            fileName = loc + '_feature' + '.csv'
            dataFrame.to_csv(fileName, sep = ',')
        elif location[1] == 'floor6' and (location[2] == 'east' or location[2] == 'west'):
            print (key)
            print (location)
            for timePoint, sensorStatus in zip (time, sensorOut):
            #for each time point
            #get the hour
                hour = re.split('[-T:.]', timePoint)[3]
                #if it's quiet hour
                if int(hour) >= 23 or int(hour) <4:
                    quietHour.append(True)
                    nightCounter += 1
                    if sensorStatus == False:
                        correctNightCounter += 1
                else:
                    quietHour.append(False)
                    dayCounter += 1
                    if sensorStatus == True:
                        correctDayCounter += 1
            dataFrame['quietHour'] = quietHour                       
            print ("day time Accuracy: " + str(correctDayCounter/dayCounter))
            print ("night time Accuracy: " + str(correctNightCounter/nightCounter))
            fileName = loc + '_feature' + '.csv'
            dataFrame.to_csv(fileName, sep = ',')


            
def saveFiles (dataList, reference, sensors, lightData):
    """
    print ("*************************************************")
    print ("saving files")
    counter = 0
    buffer = dict()
    overlap = []
    onlyLight = []
    
    for mac in sensors:
        loc = reference.get(mac)
        if (loc != None):
            overlap.append(loc)
        else:
            onlyLight.append(mac)
            loc = "404NotFound"
        
        fileName = loc +'_lightfeatures' +'.csv'
        
        df = pandas.DataFrame(dataList[counter])
        if loc in buffer:
            print ("got a repeated location")
            #open the already existed file 
            #append to the end 
            with open(fileName, 'a') as f:
                df.to_csv(f, header=False, sep = ',')

        else:
            buffer.update ({loc: 1})
            #df.to_csv(fileName, sep=',')
            
        counter += 1
    
    
    referenceMac = lightData['Directory']
    print (set(referenceMac) - set(overlap))
    print (str(counter) + " files are created with locations as file names")
    """
    print ("done")
    print ("*************************************************")

        
        
        
def main():
    path = '/Users/victorzhang/Desktop/Research/TILES/minew'
    lightFile = 'light.csv'
    reference = 'minews_owl_map.csv'
    os.chdir(path)
    dataDict= loadData(lightFile)
    macLocMap = loadReference (reference)
    checkQuietHour(dataDict, macLocMap)
    #saveFiles(dataDict, macLocMap)

main()