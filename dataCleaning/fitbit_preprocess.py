#!/usr/bin/env python

import os
import sys
import glob
import shutil
import pandas

def copyFile(fileName, outputPath):
    shutil.copy(fileName, outputPath)
    
    
def cleanHR(heartRateFile):
    heartDataFrame = pandas.read_csv(heartRateFile)
    timeCleaned = []
    heartrateCleaned = []
    window = 50
    for counter in range(len(heartDataFrame) - window):
        heartRate = list (heartDataFrame['HeartRate'][counter:counter+window])
        if len(set(heartRate)) == 1:
            counter += window
            while (heartDataFrame['HeartRate'][counter] == heartRate[0]):
                counter += 2
        else:
            timeCleaned.append(heartDataFrame['Timestamp'][counter])
            heartrateCleaned.append(heartDataFrame['HeartRate'][counter])
    
    heartRate = list (heartDataFrame['HeartRate'][-1*window:])
    if len(set(heartRate)) != 1:
        timeCleaned.append(heartDataFrame['Timestamp'][-1*window:])
        heartrateCleaned.append(heartDataFrame['HeartRate'][-1*window:])
    
    cleanedDataFrame = pandas.DataFrame()
    cleanedDataFrame['Timestamp'] = timeCleaned
    cleanedDataFrame['HeartRate'] = heartrateCleaned
    return cleanedDataFrame
    
def saveFiles (hr, output):
    hr.to_csv(output, sep = ',', index = False)
    
def DoFitbitPreprocess(in_path, out_path):
   # Ensure the output folder exists
   if not os.path.isdir(out_path):
      os.makedirs(out_path)

   files = glob.glob(os.path.join(in_path, '*.csv'))
   #change to input folder
   current = os.getcwd()
   os.chdir(in_path)
   for f in files:
      print ('processing')
      file_basename = os.path.basename(f)
      out_file_name = os.path.join(out_path, file_basename)
      if file_basename.endswith('dailySummary.csv'):
          copyFile(file_basename, out_file_name)
      elif file_basename.endswith('heartRate.csv'):
          cleanedFile = cleanHR(file_basename)
          saveFiles(cleanedFile, out_file_name)
   os.chdir(current)

if __name__ == '__main__':
   if len(sys.argv) > 2:
      fitbit_csv_folder = sys.argv[1]
      out_fitbit_csv_folder = sys.argv[2]
      DoFitbitPreprocess(fitbit_csv_folder, out_fitbit_csv_folder)
   else:
      print('Please provide the following command line arguments:\n 1) Path to folder containing fitbit CSV files\n 2) Output folder path for preprocessed fitbit CSVs')
