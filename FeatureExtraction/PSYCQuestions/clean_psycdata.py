#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 12:48:44 2018

@author: victor
"""

#load the entire folder
#split into different files 
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

def main():
    fileName = 'app_surveys.csv'
    directory = '/home/victor/Desktop/TILES/data/INTERPRETATION'
    output = '/home/victor/Desktop/TILES/data/INTERPRETATION/processed'
    myMap = loadData(fileName, directory)
    currentPath = os.getcwd()
    os.chdir(output)
    for key in myMap:
        fileName = key + '_survey_features.csv'
        saveCSV(fileName, myMap[key])
    os.chdir(currentPath)
main()