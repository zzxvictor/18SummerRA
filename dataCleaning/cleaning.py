#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 13:12:22 2018

@author: victorzhang
"""

import shutil
from sys import argv
import os

def dataCleaning(path, outputPath):
    '''
    this data does not need cleaning
    this code simply copies and copy the orginal files to another folder with new names
    '''
    os.chdir(path)
    filesList = getAllFileNames ()
    for file in filesList:
        copyFiles(file, outputPath)
        
        
def getAllFileNames():
    path = os.getcwd()
    fileList = [x for x in os.listdir(path) if x.endswith(".csv")]
    print ('%d files in total' %len(fileList))
    return fileList

def copyFiles(fileName, outputFolder):
    shutil.copy(fileName, outputFolder)

def main (inPath, outPath):
    dataCleaning(inPath, outPath)
    
if __name__ == '__main__':
    if len(argv) < 3:
        print ('please input parameters in this format: ')
        print ('path to the files + output path (absolute path, no stuff like ./)')
    else:
        fileAddress = argv[1]
        outputAddress =argv[2]
        main (fileAddress, outputAddress)