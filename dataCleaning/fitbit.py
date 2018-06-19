#!/usr/bin/env python

import os
import sys
import pdb
import glob
import numpy as np
import shutil
import pandas
from datetime import datetime 

def copyFile(fileName, outputPath):
    shutil.copy(fileName, outputPath)
    
    
def cleanning(heartRate, stepCount, outputPath):
    #open files
    heartDataFrame = pandas.read_csv(heartRate)
    stepCountDataFrame = pandas.read_csv(stepCount)
    #T mins period
    T = 20
    #increment constant
    C = 5
    #iterators
    stepCounter1 = 0
    stepCounter2 =  T
    heartCounter1 = 0
    heartCounter2 = 10*T
    
    print ('processing...')
    #get average heart rate
    avgHR = sum(heartDataFrame['HeartRate'])/len(heartDataFrame['HeartRate'])
    formatt = '%Y-%m-%dT%H:%M:%S.%f'   
    
    #output variables 
    cleanHR = pandas.DataFrame()
    cleanSC = pandas.DataFrame()
    
    while stepCounter2 < len(stepCountDataFrame): 
        endTime  = stepCountDataFrame['Timestamp'][stepCounter2]
        #find corresponding rows in heart rate file
        while heartCounter2 < len(heartDataFrame):
            if  datetime.strptime(heartDataFrame['Timestamp'][heartCounter2], formatt) < datetime.strptime(endTime, formatt) :
                #increment: C rows  
                heartCounter2 += C
            else:
                break

        stepList = stepCountDataFrame['StepCount'][stepCounter1:stepCounter2+1]
        heartList = heartDataFrame['HeartRate'][heartCounter1:heartCounter2+1]
        
        if len(heartList) != 0 and sum(stepList)/len(stepList) == 0 and sum(heartList)/len(heartList) > 2.5*avgHR:
            print ('***error1***')
            print (stepList)
            print ('--------')
            print (heartList)
            print ('********')
        elif  (len(heartList) > T and len(set(heartList)) == 1) or (len(set(stepList)) == 1 and list (set(stepList) )!= [0]):
            print ('***error2***')
            print (stepList)
            print ('--------')
            print (heartList)
            print ('********')
        else:
            cleanHR = cleanHR.append(heartDataFrame.loc[heartCounter1:heartCounter2-1], ignore_index = False)
            cleanSC = cleanSC.append(stepCountDataFrame.loc[stepCounter1:stepCounter2-1], ignore_index = False)
            
        stepCounter1 += T
        stepCounter2 += T
        heartCounter1 = heartCounter2
        heartCounter2 += 10*T
    
    return cleanHR, cleanSC
        
    
def saveFiles (hr, sc, output, id):
    hrFileName = id + '_heartRate.csv'
    scFileName = id + '_stepCount.csv'
    current = os.getcwd()
    os.chdir(output)
    hr.to_csv(hrFileName, sep = ',')
    sc.to_csv(scFileName, sep = ',')
    os.chdir(current)
    
def DoFitbitPreprocess(in_path, out_path):
   # Ensure the output folder exists
   if not os.path.isdir(out_path):
      os.makedirs(out_path)

   files = glob.glob(os.path.join(in_path, '*.csv'))
   #change to input folder
   current = os.getcwd()
   os.chdir(in_path)
   for f in files:
      file_basename = os.path.basename(f)
      out_file_name = os.path.join(out_path, file_basename)
      if file_basename.endswith('dailySummary.csv'):
          copyFile(file_basename, out_file_name)
      elif file_basename.endswith('heartRate.csv'):
          heartRate = file_basename
          stepCount = file_basename.split('_')[0] +  '_stepCount.csv'
          cleanHR, cleanSC = cleanning(heartRate, stepCount, out_file_name)
          saveFiles(cleanHR, cleanSC, out_path, file_basename.split('_')[0])
   os.chdir(current)

if __name__ == '__main__':
   if len(sys.argv) > 2:
      fitbit_csv_folder = sys.argv[1]
      out_fitbit_csv_folder = sys.argv[2]
      DoFitbitPreprocess(fitbit_csv_folder, out_fitbit_csv_folder)
   else:
      print('Please provide the following command line arguments:\n 1) Path to folder containing fitbit CSV files\n 2) Output folder path for preprocessed fitbit CSVs')
