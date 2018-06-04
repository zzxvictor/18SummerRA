#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 12:07:11 2018

@author: victorzhang
"""
import pandas
import os 
import sys 
import json 


def getFeature(index, dictObj):
    lastObj = dictObj
    if type(index) is not list:
        index = [index]
    for level, counter in zip (index, range (len(index))):
        try:
            currentObj = lastObj.get(level)
        except TypeError:
            return getFeature(index[counter:], )
        lastObj = currentObj
        print ('*********')
        print (level)
        print ('*********')
        print (currentObj)
        print ('*********')


def getOneGuysFeature(dictObj, featuresWanted):
    userID = dictObj['participant_id']
    #create a new dataframe to store the features
    newDataFrame = pandas.DataFrame()
    for features in featuresWanted:
        #for each feature 
        path = features[0]
        columnName = features[1]
        lastObj = dictObj
        #for level in path:
        #    if 

def openJSON(fileName, directory):
    currentPath = os.getcwd()
    #change to the target path 
    os.chdir(directory)
    #open JSON
    handle = open(fileName,'r')
    jsonDictList = []
    counter = 0
    for oneGuy in handle:
        jsonData = json.loads(oneGuy)
        jsonDictList.append(jsonData)
        counter += 1
    print (str(counter) + ' objects have been detected')
    #go back to the original folder
    os.chdir(currentPath)
    return jsonDictList


def convertJSONToDataFrame(jsonDictList, featuresWanted):
    for oneGuy in jsonDictList:
        getOneGuysFeature(oneGuy, featuresWanted)

def process():
    fileDirectory = '/Users/victorzhang/Desktop/Research/TILES/data/Instagram'
    fileName = 'instagram.jsonl'
    #IMPORTANT!!!!!
    #format for featureExtraction
    #for each feature, please input a pair:
    #(a list indicates where is the feature(for each posts, there are many dicts and subdicts)
    # , corresponding feature name you want to display in the .csv file)
    featuresWanted = [(['posts', 'created_time'], 'timePosted'), (['posts', 'likes'], 'likesCount')]
    dictList = openJSON(fileName, fileDirectory)
    convertJSONToDataFrame(dictList, featuresWanted)
def main ():
    process()
    
    
main()