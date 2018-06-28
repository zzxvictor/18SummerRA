#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 12:48:44 2018

@author: victor
"""


import os
import pandas 
from sys import argv
#load the data, pass it into a list 
def loadData(fileName, directory):
    print ("*************************************************")
    print ("read input")
    #change path 
    currentPath = os.getcwd()
    os.chdir(directory)
    #data stored in differnt lists according to their mac address
    myMap = {}
    #read data
    accData = pandas.read_csv(fileName, sep = ',')
    #drop unnamed column
    #accData = accData.drop(columns = ['Unnamed: 0'])
    #clear the bogus sensors
    temp = accData['participant_id']
    accData = accData.reset_index(drop = True)
    accData = accData.drop (columns = ['participant_id'])
    for participant, counter in zip (temp, range (len(temp))):
        dataFrame = accData.loc[[counter]]
        if participant in myMap:
            tempList = myMap.get(participant)
            myMap.update({participant:tempList.append (dataFrame, ignore_index = True)})
        else: 
            #print (dataFrame)
            myMap.update({participant:dataFrame})
    print ("done")
    print ("*************************************************")
    os.chdir(currentPath)
    return myMap

def saveCSV(fileName, data):   
    print (data)     
    data.to_csv(fileName, sep=',', index = False)

def main(fileName,directory , output):
    
    #fileName = 'app_surveys.csv'
    #directory = '/Users/victorzhang/Desktop/Research/TILES/data/psyc'
    #output = '/Users/victorzhang/Desktop/Research/TILES/data/psyc/processed'
    myMap = loadData(fileName, directory)
    currentPath = os.getcwd()
    os.chdir(output)
    for key in myMap:
        fileName = key + '_survey_features.csv'
        saveCSV(fileName, myMap[key])
    os.chdir(currentPath)

        
if __name__ == '__main__':
    if len(argv) < 4:
        print ('please input parameters in this format: ')
        print ('file you want to clena + path to the files + output path (absolute path, no stuff like ./)')
    else:
        fileName = argv[1]
        fileAddress = argv[2]
        outputAddress =argv[3]
        main (fileName, fileAddress, outputAddress)