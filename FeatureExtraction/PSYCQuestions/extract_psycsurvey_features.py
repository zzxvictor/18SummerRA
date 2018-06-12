#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 09:10:12 2018

@author: victor
"""
import pandas
import os
import pytz
from datetime  import datetime
import dateutil.parser
import ast

from_zone = pytz.utc
to_zone = pytz.timezone("America/Los_Angeles")


def getFileNames (path):
    os.chdir(path)
    fileList = [x for x in os.listdir(path) if x.endswith("_features.csv")]
    print ('%d files in total' %len(fileList))
    return fileList
#read data individually 
def loadData(fileName):
    print ("*************************************************")
    print ("read input")
    #read data
    accData = pandas.read_csv(fileName, sep = ',')
    print ("done")
    print ("*************************************************")
    return accData

#feature extractions
    #survey type
    #activity before PF survey [1,2,3...]
    #PF part two [list of int]
    #PF part three [list of int], average
    
    #E/PC survey
    #location [1,2,3] 
    #activity before the survey
    #part three average
    #part four average
    #part five, average of two sections
def featureExtractions(dataFrame):
    headerFormat = ['surveyType','surveyID', 'testDelieveredLocalTime','testStartedLocalTime','testCompletedLocalTime', 'testIngestedLocalTime','activityBeforeSurvey']
    pfFormat = ['psycFlexEmotionasBeforeSurvey', 'psycFlexScore']
    engageFormat = ['psycCapSurveyEnvironment', 'psycCapWorkEngagementScore', 'psycCapPSYCAPScore', 'pyscCapInterpersonalSupportSCore', 'psycCapChallengeStressorScore', 'psycCapHindranceStressorScore']
    overallFormat = headerFormat + pfFormat + engageFormat
    defaultPFAnswer = [None for x in range (len(pfFormat))]
    defaultENGANswer = [None for x in range (len(engageFormat))]
    #each survey
    newDataFrame = pandas.DataFrame()
    for counter in range (len(dataFrame)):
        surveyType = dataFrame['survey_type'][counter]
        surveyID = dataFrame['survey_id'][counter]
        dictString = dataFrame['results'][counter]
        results = ast.literal_eval(dictString)
        delieveredTime = convertToLocalTime(dataFrame['delivered_ts_utc'][counter])
        startedTime = convertToLocalTime(dataFrame['started_ts_utc'][counter])
        completedTime = convertToLocalTime(dataFrame['completed_ts_utc'][counter])
        ingestedTime = convertToLocalTime(dataFrame['ingested_ts_utc'][counter])
        defaultPFAnswer, defaultENGANswer,activity= convertSurveyResultsToNumbers(results, surveyType, engageFormat, pfFormat)
        head = [surveyType, surveyID, delieveredTime, startedTime, completedTime, ingestedTime, activity]
        #convet to dataframe
        row = pandas.Series(head + defaultPFAnswer + defaultENGANswer, index = overallFormat)
        #create new Dataframe
        newDataFrame = newDataFrame.append (row, ignore_index= True )
    
    print (newDataFrame)
    return newDataFrame
def convertToLocalTime(utc):
        #utc = utc.split('+')[0]
    timeObj = dateutil.parser.parse(utc)
    #utc = utc.replace(tzinfo=from_zone)
    local = timeObj.astimezone(to_zone)
    return (local.strftime('%Y-%m-%dT%H:%M:%S.%f'))
    
def convertSurveyResultsToNumbers(result, surveyType, engageFormat, pfFormat):
    if surveyType == 'psych_flex':
        activity = result.get('1')
        emotions = result.get('2')
        flex = []
        for keys in result:
            if keys != '1' and keys != '2':
                flex.append(result.get(keys))
        return [emotions, sum(flex)/len(flex)],[None for x in range (len(engageFormat))],activity
    elif surveyType == 'engage_psycap':
        locations = result.get('1')
        activity = result.get('2')
        engagement = []
        for keys in ['3','4','5']:
            engagement.append(result.get(keys))
        engagement = sum(engagement)/len(engagement)
        cap = []
        for keys in ['6','7','8', '9','10', '11', '12','13','14','15','16','17']:
            cap.append(result.get(keys))
        cap = sum(cap)/len(cap)
        personalsupport = []
        for keys in ['18','19','20']:
            personalsupport.append(result.get(keys))        
        personalsupport = sum(personalsupport)/len(personalsupport)
        challenge = []
        for keys in ['21','22','23','24','25']:
             challenge.append(result.get(keys))
        challenge = sum(challenge)/len(challenge)
        hindrance = []
        for keys in ['26','27','28','29']:
             hindrance.append(result.get(keys))
        hindrance = sum(hindrance)/len(hindrance)
        return [None for x in range (len(pfFormat))],[locations,engagement, cap, personalsupport, challenge, hindrance],activity
    else:
        print ('error')
def saveFile(data, fileName, output):
    print ('10')
    
def main ():
    fileAddress = '/home/victor/Desktop/TILES/data/INTERPRETATION/processed'
    outputAddress = '/home/victor/Desktop/TILES/data/INTERPRETATION/processed/finished'
    fileList = getFileNames(fileAddress)
    for file in fileList:
        dataFrame = loadData(file)
        newDataFrame = featureExtractions(dataFrame)
        saveFile(newDataFrame, file ,outputAddress)
        
main()