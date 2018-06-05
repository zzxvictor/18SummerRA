#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 14:06:22 2018

@author: victorZixuan Zhang 
"""

import json 
import os
import pandas as pd


def LoadJson(fileName, directory):
    current = os.getcwd()
    os.chdir(directory)
    handle = open (fileName, 'r')
    df = pd.DataFrame([json.loads(line) for line in handle])
    os.chdir(current)
    return df

def splitDataFrameIntoPersonalFiles (dataFrame, outputFolder):
   
    participants = dataFrame['participant_id']
    print ('participants counts: ' + str(len (participants)))
    for counter in range (len (participants)):
        individual = dataFrame.loc[counter,:].to_frame()
        print (type (individual))
        print(individual.iloc ['posts'])
        
def main ():
    fileName = 'facebook.jsonl'
    directory = '/home/victor/Desktop/TILES/data/Facebook'
    outputFolder = '/home/victor/Desktop/TILES/data/Facebook/Processed'
    dataFrame = (LoadJson(fileName, directory))
    splitDataFrameIntoPersonalFiles(dataFrame, outputFolder)
main()