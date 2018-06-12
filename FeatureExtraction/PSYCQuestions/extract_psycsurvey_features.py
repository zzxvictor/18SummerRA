#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 09:10:12 2018

@author: victor
"""
import pandas
import os

#read data individually 
def loadData(fileName, directory):
    print ("*************************************************")
    print ("read input")
    #change path 
    currentPath = os.getcwd()
    os.chdir(directory)
    #read data
    accData = pandas.read_csv(fileName, sep = ',')
    print ("done")
    print ("*************************************************")
    os.chdir(currentPath)
    return accData

#feature extractions
def featureExtractions(dataFrame):
    headerFormat = ['surveyType','surveyID', 'testDelieveredLocalTime','testStartedLocalTime','testCompletedLocalTime', 'testIngestedLocalTime','activityBeforeSurvey']
    pfFormat = ['psycFlexEmotionasBeforeSurvey', 'psycFlexScore']
    engageFormat = ['psycCapSurveyEnvironment', 'psycCapWorkEngagementScore', 'psycCapPSYCAPScore', 'pyscCapInterpersonalSupportSCore', 'psycCapChallengeStressorScore', 'psycCapHindranceStressorScore']
    overallFormat = headerFormat + pfFormat + engageFormat
    
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
