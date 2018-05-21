#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python file for TILE 
Functionality: 
    read different files and merge them into one big file
    add timestamp 
@author: victor zhang
@Time: 3/28 2018 
"""
import os
import pandas
import csv
import re
import time
"""
this functon read all csv files and store them into different lists according to the number of feauters
"""
def readInputInOneFile(fileNameList, environmentList = [],speechList1 = [], speechList2 = [],environFile = [], config1File = [], config2File = []):
    config1 = 135
    config2 = 128
    environment = 41
    for item in fileNameList:
        print ("*************************************************")
        print ("readInputInOneFile")
        print ("now read file: " + item + "...")
        #tempData = pandas.read_csv(item, sep = ';', header = None)
        with open(item) as csvfile:
            tempData = csv.DictReader(csvfile, delimiter = ';')
            header = tempData.fieldnames
        print ("done")
       # print (header)
        featureNum = len(header)
        print ("features of this file is: " + str(featureNum))
        
        if featureNum == config1:
            speechList1.append(tempData)
            print ("it has config1 format")
            config1File.append(item)
        elif featureNum == config2:
            speechList2.append(tempData)
            print ("it has config2 format")
            config2File.append(item)
        elif featureNum == environment:
            environmentList.append(tempData)
            print ("it has environment format")
            environFile.append(item)
        else:
            print("error! Has no corresponding configuration ")
        
        print ("*************************************************")
        
    print ("environment files: " + str(environFile))
    print ("config1 files: " + str(config1File))
    print ("config2 files: " + str(config2File))

            
"""
this function records all the names of files in the foler in which the code is run
"""
def readNamesOfAllFiles():
    currentPath = os.getcwd()
    print ("Current path: " + currentPath)
    #only .csv files remains
    fileNameList = [x for x in os.listdir(currentPath) if x.endswith(".csv")]
    print("All .csv files under this path: ")
    print(fileNameList)
    print("All files are stored! Ready for reading data")
    return fileNameList

"""
this function merges all the dataframes in one list and returns a new, bigger chunk of dataframe
"""
def mergeAllData(containerList):  
    print ("*************************************************")
    print ("mergeAllData")
    print ("cancatenating all dataframes in the list...")
    newContainer = pandas.concat (containerList)
    print ("done")
    print ("new dataframe has size: " + str(newContainer.shape))
    print ("*************************************************")
    return newContainer

"""
this function adds timestamp to a dataframe
"""
def addTimeStamp(containerList,fileTypeList):
    print ("*************************************************")
    print ("addTimeStamp")
    for i in range (len(containerList)):
        fileName = re.split('[_ .]',fileTypeList[i])
        linuxTime = fileName[2]
        realTime = time.strftime("%y-%m-%d %H:%M:%S",time.gmtime(int(linuxTime))).split(' ')
        print (str(realTime))
        temp = containerList[i]
        print (temp)
    print ("*************************************************")
        

def writeCSV(container,folderName):
    print ("*************************************************")
    print ("writing data into new CSV files")
    with open(folderName,'wb') as fou:
        dw = csv.DictWriter(fou, delimiter=';', fieldnames=container.fieldnames)
        for row in container:
            dw.writerow(row)
            

    print ("*************************************************")
    
    

def main():
    folderName = 'tester.csv'
    fileNameList = []
    environmentList = []
    configList1 = []
    configList2 = []
    environFile = []
    config1File = []
    config2File = []
    
    fileNameList = readNamesOfAllFiles()
    # read all data, classify them into differnt lists
    readInputInOneFile(fileNameList,environmentList,configList1,configList2, environFile, config1File,config2File)
    # add time stampe
    addTimeStamp(environmentList, environFile)
    addTimeStamp(configList1, config1File)
    addTimeStamp(configList2, config2File)
    
    #merge data together 
    #newSpeechList1 = mergeAllData(configList1)
    #newSpeechList2 = mergeAllData(configList2)
    #newEnvironment = mergeAllData(environmentList)

    writeCSV(environmentList[0],folderName)
main()

