#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last modified on Fri May 18 08:40:11 2018
For TILES accelerometry data 
@author: victor zixuan zhang
"""
#import header files 
import os
import pandas
import math
import matplotlib.pyplot as plt
from statistics import mode
import numpy
from sys import argv

"""
    read filenames in the given folder and store them in a list 
    Parameter: N/A
    Return: fileNameSet (list)
        e.g., [fileName1, fileName2, fileName3, ...]
"""
def readNamesOfAllFiles(path):
    if path == "ls":
        path = os.getcwd()
    else:
        os.chdir(path)
    print ("folder:" + path)
    #currentPath = os.getcwd()
    #print ("Current path: " + currentPath)
    #only .csv files remains
    fileNames = [x for x in os.listdir(path) if x.endswith("features.csv")]
    print("All .csv files under this path: ")
    print(fileNames)
    #drop files (i.e. temp_hum.csv)
    dropList = ['light.csv','motion.csv','temperature_humidity.csv']
    fileNameSet = set(fileNames) - set(dropList)
    
    #return the filenames 
    return list(fileNameSet) 

"""
    read the files according to the fileNames and openFile
    e.g., openFile = [1,2,3,4]. the First, second, third 
    and fourth file in the fileNameList will be opened 
    
    parameter: 
        openFile (user's option of which files to open)
        fileNameList (list contains all filenames in the given folder)
    
    return: 
        a list of data read from files
        e.g., [data in file1, data in file2, ...]
"""
def readFiles(openFile, fileNameList, path):
    dataList = []
    for item in openFile:
        tempData = pandas.read_csv(fileNameList[item], index_col = False ,sep = ',')
        dataList.append(tempData)
    
    return dataList


"""
    data analysis
    
    parameter:
        accData: the accelerometry data retrieved bey the previous two functions.
        an item in the accData list is a dataFrame, which has several columns like accelerationX, timeStamp,...
        
    return:
        accData: the processed data with a new column called "status"
"""
def dataAnalysis(accData):
    #a for loop, go through all items in the list
    for data in accData:
        #load the features
        aX = data['accelerationX']
        aY = data['accelerationY']
        aZ = data['accelerationZ']
        # create two empty lists for data storage
        thetaList = []#store the angle
        thresh = [] # store the threshold
        
        #find the most frequently appeared value
        #the rationale behind this is that the doors should be static in most of times
        #ideally speaking, there should be no component on Y and Z axis (the g is vertical)
        #however, the sensors were not perfectly mounted so that the X axis is not aligned with the g
        
        typicalX = mode (aX) #static acceleration on X axis
        typicalY = mode (aY) #static acceleration on Y axis
        typicalZ = mode (aZ) #static acceleration on Z axis
        
        #calculate the mode of the static a vector
        typicalMode = math.sqrt(typicalX*typicalX + typicalY*typicalY + typicalZ * typicalZ)
            
        #calculate angle between the instant a and static a 
        for i in range (len (aX)):
            # the mode of the instant a, which varies from time to time depends on the motion of the doors
            instanceMode = math.sqrt( aX[i]*aX[i] + aY[i]*aY[i] + aZ[i]*aZ[i] )
            #calculate the dot multiplication of two vectors 
            dotMultiplication = typicalX*aX[i] + typicalY*aY[i] + typicalZ*aZ[i]
            #calculate the angle between two vectors (should always be greater than 0 and smaller than 90 degrees)
            cosTheta = dotMultiplication / (typicalMode * instanceMode )
            #threshold, due to the inaccuracy of the binary format, sometimes cosTheta is greater than 1 or smaller than -1
            #which is why we need to restrict the value, otherwise arccos () will fail
            if cosTheta > 1:
                cosTheta = 1
            if cosTheta < -1:
                cosTheta = -1
            #calculate the actual angle in degress
            theta = numpy.arccos(cosTheta) * 180 /3.1415
            #store the angle in the list
            thetaList.append(theta)

        #calculate the derivatives of the angle deviation(d(angle)/dt )
        deriThetaList = []
        label = []
        for i in range (len (aX)):
            if i == 0:
                #head, d(theta)/dt is considered 0 
                deriThetaList.append (0)
                label.append(0)
            elif i == len(thetaList) - 1:
                #tail, d(theta)/dt is considered 0 
                deriThetaList.append (0)
                label.append(0)
            else:
                #body 
                deriThetaList.append(thetaList[i+1] - thetaList[i])
                
        #show the histgram         
        n,b,p = plt.hist(deriThetaList, bins = 51, range = (-1.5,1.5))
        #plt.ylabel("Time Appears")
        #plt.xlabel("d(theta)/dt")
        #plt.title("histogram ")
        #plt.show()
        #decide the appropriate threshold for this file
        threshold = dynamicThreshold(n,b)
        print (threshold)

        #check the status based on the threshold         
        for i in range (len(deriThetaList)):
            if i != 0 and i != len(deriThetaList) -1:
                if deriThetaList[i]>threshold:
                    label.append(1)
                elif deriThetaList[i]<-1*threshold:
                    label.append(-1)
                else:
                    label.append(0)
            thresh.append (threshold)
                
        data['status'] = label 
        
        #show a small portion of the data 
        #plt.plot(deriThetaList[5200:5400])
        #plt.plot(thresh[5200:5400])
        #plt.xlabel("samples")
        #plt.ylabel("d(theta)/dt")
        #plt.legend(("angle deriv","threshold"),loc='upper right')
        #plt.title("sample of angle derivatives ")
        #plt.show()
        print ('*********************************')
        
            
    return accData

"""
    dynamically decide the threshold based on the distribution of the angle data(histgrams)
    
    parameter:
        n: the height of the bins 
        b: the values of the bins 
    return:
        the absolute value of the threshold
"""
def dynamicThreshold(n,b):
    #start from the second highest bin since the 0bin is always the highest
    i = 2
    defaulT = 0.3
    while True:
        #find two bins with similar heights
        n1 = findKthBin(n,i)
        n2 = findKthBin(n,i+1)
        if n1 == None or n2 == None:
            return defaulT
        index1 = n.tolist().index (n1)
        index2 = n.tolist().index (n2)
        
        #check the heights 
        if b[index1]+b[index2] < 0.1 and b[index1]+ b[index2] > -0.1:
            #sanity check 
            if (abs(b[index1]) - 0.07) < 0.03:
                #too close to 0, the method fails, return the default threshold
                return defaulT
            
            else:
                return abs(b[index1]) - 0.07
            
        #increase the iterator
        else:
            i = i+1
            if i > 5:
                return defaulT

"""
    find the Kth heights bin
    parameter:
        arr: the heights of the bins
        k: 
    return:
        return the heights

"""
def findKthBin(arr, k):
    if k == 1:
        try:
            return max(arr)
        except ValueError:
            return None 
    try:
        m = max(arr)
    except ValueError:
        return None
    new_arr = list(filter(lambda a: a != m, arr))
    return(findKthBin( new_arr, k-1))


"""
   write new data into the files
   parameter:
       labledData: the processed data with labels
       openFile: files opened 
       accDataFile: the list contains all fileNames
   return:
       N/A
"""
def addLabelToFiles(labledData, openFile, accDataFile, currentPath):
    i = 0
    for index in openFile:
        #open the corresponding file:
        fileName = accDataFile[index]
        labledData[i].to_csv(fileName, sep = ',',index = False)
        #print (labledData[i])
        i = i+1
    os.chdir(currentPath)
        
"""
    main function
"""
def main(path):
    currentPath = os.getcwd()
    accDataFile = readNamesOfAllFiles(path)
    openFile = range(len(accDataFile))
    accData = readFiles(openFile, accDataFile, path)
    labledData = dataAnalysis(accData)
    addLabelToFiles(labledData, openFile, accDataFile, currentPath)
    
    
if __name__ == "__main__":
    if len(argv) < 2:
        print ("please input the directory of the files you want to process:")
    address = argv[1]
    print ("the address is: " + str(address))
    main(address)

    
    
    