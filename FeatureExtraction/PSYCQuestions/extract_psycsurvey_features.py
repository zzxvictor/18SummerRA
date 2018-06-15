#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 09:10:12 2018

@author: victor
"""
import pandas
import os
import pytz
import dateutil.parser
import ast
from datetime import datetime 
from sys import argv

from_zone = pytz.utc
to_zone = pytz.timezone("America/Los_Angeles")

'''
get names of the files with '_features.csv' and return them in a list
the folder should only contain pscy data processed by clean_pscydata.py
parameter:
    path: path to the files
return 
    fileList: a list of file names
'''
def getFileNames (path):
    os.chdir(path)
    fileList = [x for x in os.listdir(path) if x.endswith("_features.csv")]
    print ('%d files in total' %len(fileList))
    return fileList

'''
load one single file and return the data as a pandas dataframe
parameter:
    fileName: the name of the file
return:
    accData: the dataframe contains all the data in the given file
'''
def loadData(fileName):
    #read data
    accData = pandas.read_csv(fileName, sep = ',')
    return accData

'''
convert the answers to features 
the column names are stored in headerFormat, activityFormat, pfFormat, and engageFormat
logistics: read one file, process one survey at a time and then append the result to the data frame
parameter:
    dataFrame
return:
    newDataFrame
'''
def featureExtractions(dataFrame):
    headerFormat = ['Timestamp', 'surveyType','durationInSeconds']
    activityFormat = ['workBeforeSurvey', 'onPhoneBeforeSurvey', 'interactWithPeopleBeforeSurvey', 'sportBeforeSurvey', 'shoppingBeforeSurvey', 'diningBeforeSurvey', 'householingBeforeSurvey', 'familyBeforeSurvey', 'personalActivityBeforeSurvey', 'educationBeforeSurvey', 'transportBeforeSurvey', 'orgActivityBeforeSurvey', 'unKnownBeforeSurvey']
    pfFormat = ['psycFlexPositiveEmotionasBeforeSurvey', 'psycFlexNegativeEmotionasBeforeSurvey','psycFlexScore']
    environmentFormat = ['surveyAtHome', 'surveyAtWork', 'surveyInDoors', 'SurveyInAVehicle', 'surveyAtOtherPlaces']
    engageFormat = [ 'psycCapWorkEngagementScore', 'psycCapPSYCAPScore', 'pyscCapInterpersonalSupportSCore', 'psycCapChallengeStressorScore', 'psycCapHindranceStressorScore']
    
    overallFormat = headerFormat+ activityFormat + pfFormat + environmentFormat + engageFormat
    newDataFrame = pandas.DataFrame(columns = overallFormat)
    #each survey
    newDataFrame = pandas.DataFrame()
    for counter in range (len(dataFrame)):
        surveyType = dataFrame['survey_type'][counter]
        dictString = dataFrame['results'][counter]
        results = ast.literal_eval(dictString)
        startedTime = convertToLocalTime(dataFrame['started_ts_utc'][counter])
        completedTime = convertToLocalTime(dataFrame['completed_ts_utc'][counter])
        duration = getDuration (startedTime, completedTime)
        defaultPFAnswer, defaultENGANswer,activity= convertSurveyResultsToNumbers(results, surveyType, engageFormat, pfFormat,activityFormat , environmentFormat)
        head = [startedTime,surveyType, duration] 
        #convet to dataframe
        suum = head + activity + defaultPFAnswer + defaultENGANswer

        row = pandas.Series(suum, index = overallFormat)
        #create new Dataframe
        newDataFrame = newDataFrame.append (row , ignore_index= True )
    
    newDataFrame = newDataFrame[overallFormat]
    return newDataFrame

'''
calculate the duration of the survey
parameter: 
    startTime, stopTime
return:
    duration: in minutes
'''
def getDuration(startTime, stopTime):
    strFormat = '%Y-%m-%dT%H:%M:%S.%f'
    start = datetime.strptime(startTime, strFormat)
    stop = datetime.strptime(stopTime, strFormat)
    td =  (stop - start).seconds
    return td
'''
convert utc time to local time (Los Angeles)(defined above near the import statements)
parameter:
    utc: utc timestamp like 2018-12-12 10:10:10+00:00
return:
    a string in local time with format (2018-12-12T11:22:33.856)
'''
def convertToLocalTime(utc):
        #utc = utc.split('+')[0]
    timeObj = dateutil.parser.parse(utc)
    #utc = utc.replace(tzinfo=from_zone)
    local = timeObj.astimezone(to_zone)
    return (local.strftime('%Y-%m-%dT%H:%M:%S.%f'))

'''
convert participants' response regarding the activities they did before the survey to machine learning features
if participant worked before the survey, the result would be [1,0,0,0,...]
parameter:
    option: users' response
    acformat: the format we want to use for activities
return 
    defaultAnswer
'''
def convertActivity (option, acformat):
    defaultAnswer = [None for item in range (len(acformat))]
    try:
        number = int (option)
        defaultAnswer[number] = 1
    except:
        if option != None:
            if option.find('watch') != -1 or option.find('hiking') != -1 or option.find('riding') != -1 or option.find('gym') != -1:
                defaultAnswer[4] = 1
        else:
            defaultAnswer[-1] = 1
    
    return defaultAnswer

'''
convert question 2 in psy flex questionnaire to two useable features: positive emotions and negative emotions
schema: count the number of positive and negative answers and divided by total number of positive and negative questions
parameter:
    participant's answer
return:
    [positive emotions, negative emotions]
'''
def convertEmotions(option):
    negative = 0
    positve = 0
    if option == None:
        return [None, None]
    elif type(option) is int:
        option = [option]
    
    for choice in option:
        if choice in [1,3,5,7]:
            positve += 1
        else:
            negative += 1
    return [positve/4, negative/10]

def convertLocations(option, format):
    defaultAnswer = [None for i in range (len(format)) ]
    if option in [0,1,2,3,4]:
        defaultAnswer[option] = 1
    else:
        defaultAnswer[-1] = None 
    
    return defaultAnswer
        
'''
conver other results to features
parameter:
    result: a list contains user's response
    surveyType: what type of  survey the result corresponds to 
    engageFormat, pfFormat, activityFormat: formats of the output

return:
    features in a list
'''
def convertSurveyResultsToNumbers(result, surveyType, engageFormat, pfFormat, activityFormat, environmentFormat):
    if surveyType == 'psych_flex':
        
        activity = convertActivity (result.get('1'), activityFormat)
        emotions = convertEmotions(result.get('2'))
        flex = []
        for keys in result:
            if keys != '1' and keys != '2':
                flex.append(result.get(keys))
        return emotions + [sum(flex)/len(flex)],[None for x in range (len(environmentFormat + engageFormat))],activity
    elif surveyType == 'engage_psycap':
        locations = convertLocations (result.get('1'), environmentFormat)
        activity = convertActivity (result.get('1'), activityFormat)
        engagement = []
        for keys in ['3','4','5']:
            if result.get(keys) != None:
                engagement.append(result.get(keys))
        try:
            engagement = sum(engagement)/len(engagement)
        except:
            engagement = None 
        cap = []
        for keys in ['6','7','8', '9','10', '11', '12','13','14','15','16','17']:
            if result.get(keys) != None:
                cap.append(result.get(keys)) 
        try:
            cap = sum(cap)/len(cap)
        except:
            cap = None
            
        personalsupport = []
        for keys in ['18','19','20']:
            if result.get(keys) != None:
                personalsupport.append(result.get(keys))        
        try:
            personalsupport = sum(personalsupport)/len(personalsupport)
        except:
            personalsupport = None
        challenge = []
        for keys in ['21','22','23','24','25']:
            if result.get(keys) != None:
                challenge.append(result.get(keys))
        try:
            challenge = sum(challenge)/len(challenge)
        except:
            challenge = None
        hindrance = []
        for keys in ['26','27','28','29']:
            if result.get(keys) != None:
                hindrance.append(result.get(keys))
        try:
            hindrance = sum(hindrance)/len(hindrance)
        except:
            hindrance = None 
            
        return [None for x in range (len(pfFormat))],locations+ [engagement, cap, personalsupport, challenge, hindrance],activity
    else:
        print ('error')
        

'''
save the file
'''
def saveFile(data, fileName, output):
    current = os.getcwd()
    os.chdir(output)
    data.to_csv(fileName, sep=',', index = False)
    os.chdir(current)
    
def main (fileAddress, outputAddress):
    
    #fileAddress = '/Users/victorzhang/Desktop/Research/TILES/data/psyc/processed'
    #outputAddress = '/Users/victorzhang/Desktop/Research/TILES/data/psyc/complete'
    fileList = getFileNames(fileAddress)
    for file in fileList:
        dataFrame = loadData(file)
        newDataFrame = featureExtractions(dataFrame)
        saveFile(newDataFrame, file ,outputAddress)
        
if __name__ == '__main__':
    if len(argv) < 3:
        print ('please input parameters in this format: ')
        print ('path to the files + output path (absolute path, no stuff like ./)')
    else:
        fileAddress = argv[1]
        outputAddress =argv[2]
        main (fileAddress, outputAddress)
