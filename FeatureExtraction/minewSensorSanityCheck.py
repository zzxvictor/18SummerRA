#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 12:46:55 2018

@author: victorzhang
"""
import glob
import os
import pandas 
from datetime import datetime 

def scanFolder ():
    filesList = []
    filesList =  glob.glob('*.csv')
    return filesList
def loadCSV(fileName):
    #print ('File name : %s has been opened' %fileName)
    dataFrame = pandas.read_csv(fileName, sep = ',')
    return (dataFrame)
    
def checkLength (dataFrame):
    
    return len (dataFrame)

def checkContinuity (dataFrame):
    timeStamps = dataFrame['Timestamp']
    startTime = datetime.strptime(timeStamps[0], '%Y-%m-%dT%H:%M:%S.%f')
    endTime = datetime.strptime(timeStamps[len(timeStamps) - 1], '%Y-%m-%dT%H:%M:%S.%f')
    previous = startTime
    log = []
    for point in timeStamps:
        timeObj = datetime.strptime(point, '%Y-%m-%dT%H:%M:%S.%f')
        if (timeObj - previous).days > 1:
            log.append((timeObj.strftime('%Y-%m-%dT%H:%M:%S.%f'), previous.strftime('%Y-%m-%dT%H:%M:%S.%f')))
        previous = timeObj
    
    return startTime, endTime, log

def createReport (length, start, stop, log, fileName):
    print ('**********report**********')
    print ('file name: %s' %(fileName))
    print ('data start date: ', end = '')
    print (start)
    print ('data end date: ', end = '')
    print (stop)
    print ('days missing ', end = '')
    for pair in log:
        print (pair)
    print ('length: ' + str(length))
    print ('***********end***********')
    print ('')
def main():
    tempHumFolder = '/Users/victorzhang/Desktop/Research/TILES/data/minew/minew-processed/temHumFeature'
    lightFolder = '/Users/victorzhang/Desktop/Research/TILES/data/minew/minew-processed/lightFeature'
    #for the tempHum sensors
    os.chdir (tempHumFolder)
    filesList = scanFolder ()
    for file in filesList:
        dataFrame = loadCSV(file)
        length = checkLength(dataFrame)
        start, stop, log = checkContinuity(dataFrame)
        #plots 
        if len(log) > 3:
            createReport (length, start, stop, log, file)
        #print ('**********done*************')
    #for the light sensors 
    os.chdir(lightFolder)
    filesList = scanFolder()
    
main()