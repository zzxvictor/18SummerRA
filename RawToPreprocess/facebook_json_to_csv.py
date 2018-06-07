#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 14:06:22 2018

@author: victorZixuan Zhang 
"""

import json 
import os
import pandas 
import sys
import pytz
from datetime  import datetime
import glob

from_zone = pytz.utc
to_zone = pytz.timezone("America/Los_Angeles")

"""
laod Json File 
parameter:
    fileName: the file you want to open
    directory: where is the file
return:
    jsonDictList: a list of dictionaries converted from json objects
"""
def LoadJson(fileName, directory):
    current = os.getcwd()
    os.chdir(directory)
    handle = open (fileName, 'r')
    jsonDictList = []
    for oneGuy in handle:
        jsonData = json.loads(oneGuy)
        jsonDictList.append(jsonData)
    print (str(len(jsonDictList)) + ' objects have been detected')
    os.chdir(current)
    return jsonDictList

"""
split the list into individual files 
parameter:
    dictList: the jsonDictList returned from loadJson ()
    outputFolder: the folder where you want to store the outputs
return:
    N/A
"""
def splitDataFrameIntoPersonalFiles (dictList, outputFolder ):
    for obj in dictList:
        #get ID
        participantID = obj ['participant_id']
       #get online ID
        onlineID = str(obj['id'])
        try:
            likes = len(obj['likes'])
        except:
            likes = None    
        try:
            friends = len(obj['friends'])
        except:
            friends = None 
        #get timezone
        try:
            timeZone = obj['timezone']
        except:
            timeZone = None 
       #get gender
        try:
            gender = obj['gender']
        except:
            gender = None
       #get age/birthday
        try:
            dob = obj['birthday']
        except:
            dob = None
       #get picture 
        try:
            picture = obj['picture']['data']['url']
        except:
            picture = None 
       #get education
        try:
            eduList = obj['education']
            
            edu = []
            for school in eduList:
                schoolType = school['type']
                edu.append(schoolType)
        except:
            edu = []
       #get location 
        try:
            location = obj['locale']
        except:
            location = None 
       #get verification status 
        try:
            isVerified = obj['verified']
        except:
            isVerified = None
       #get info in the post
        postList = obj['posts']
           #when
           #content
       #events
        eventList = obj['events']
           #when
           #where
           #content
           #rsvp status 
        print ('---------------------------------------')
        print ('ID num:' + participantID)
        print ('online ID: ' + onlineID)
        print ('gender: ' + str(gender))
        print ('DOB: ' + str(dob))
        print ('profile pic: ' + str(picture))
        print ('education: ' + str(edu))
        print ('locale: ' + str(location ))
        print ('number of posts: ' + str(len(postList)))
        print ('number of events: ' + str(len(eventList)))
        print ('---------------------------------------')
        
        dataFrame = createDataFrame(participantID,onlineID, timeZone, gender, dob, picture, edu, location, isVerified, postList, eventList, likes, friends)
        fileName = participantID+'_Facebook.csv'
        saveCSV(fileName, dataFrame,outputFolder )

"""
create a dataFrame for each person
parameter:
    participantID: user's ID
    onlineID: user's facebook ID
    gender: male/female
    dob: data of birth
    picture: link to user's profile picture
    edu: a list of school types the user went to
    location:user's region
    isVerified: if the account is verified
    postList: a list of posts
    eventList: a list of events
    
return:
    personalDataFrame: a personal file contains different features, ready to stored as csv files
"""
def createDataFrame(participantID,onlineID, timeZone,gender, dob, picture, edu, location, isVerified, postList, eventList, likes, friends):
    personalInfor = [ 'facebookID', 'facebookTimeZone','facebookUserGender', 'facebookLikesCount', 'facebookFriendsNumber','facebookUserBirthday', 'facebookProfilePicture', 'facebookEducationList', 'facebookAcountIsVerified']
    post = [ 'facebookPostMessage', 'facebookPostStory']
    event = ['facebookEventName', 'facebookEventLocation', 'facebookEventRSVPStatus', 'facebookEventLongitude', 'facebookEventLatitude']
    instant = ['Timestamp', 'facebookActivityType']
    featureList = instant + personalInfor + post + event 
    personalData = [ onlineID, timeZone,gender, likes, friends,dob, picture, edu, isVerified]
    blankPostData = [None, None]
    blankEventData = [None, None, None, None, None]
    #blank dataframe
    personalDataFrame = pandas.DataFrame(columns = featureList)
    #load posts 
    for eachPost in postList:
        Type = 'post'
        time = convertUTCtoLocal(eachPost['created_time'])
        try:
            message = eachPost['message']
        except:
            message = None
        try:
            story = eachPost['story']
        except:
            story = None
        row = [time, Type] + personalData + [message, story] + blankEventData
        dataList = pandas.Series(row, index = featureList)
        #print(dataList)
        personalDataFrame = personalDataFrame.append (dataList, ignore_index= True )
    
    for eachEvent in eventList:
        Type = 'event'
        time = convertUTCtoLocal(eachEvent['start_time'])
        rsvp = eachEvent['rsvp_status']
        eventName = eachEvent['name']
        try:
            eventLongitude = eachEvent['place']['location']['longitude']
            eventLatitude = eachEvent['place']['location']['latitude']
            placeName = eachEvent['place']['location']['name']
        except:
            eventLongitude = None
            eventLatitude = None
            placeName = None
        
        
        row = [time, Type] + personalData + blankPostData + [eventName, placeName, rsvp, eventLongitude, eventLatitude]
        dataList = pandas.Series(row, index = featureList)
        #print(dataList)
        personalDataFrame = personalDataFrame.append (dataList, ignore_index= True )
        
    return personalDataFrame

"""
save the dataframe
parameter:
    fileName: the name you want to use to name the file
    data: the exact data you want ot store
    outputFolder: the folder you want to put the files
return :
    N/A
"""
def saveCSV(fileName, data, outputFolder):
    current = os.getcwd()
    os.chdir(outputFolder)
    data.to_csv(fileName, sep = ',', index = False)
    os.chdir(current)
    
"""
convert xx time to local time 
parameter:
    utc: a time string with format: '%Y-%m-%dT%H:%M:%S.%f'
return:
    local time with the same format
"""

def convertUTCtoLocal(timeInOtherZone):
    #utc = utc.split('+')[0]
    timeObj = datetime.strptime(timeInOtherZone, '%Y-%m-%dT%H:%M:%S%z')
    #utc = utc.replace(tzinfo=from_zone)
    local = timeObj.astimezone(to_zone)
    return (local.strftime('%Y-%m-%dT%H:%M:%S.%f'))

def main (fileName, directory, outputFolder):
    """
    fileName = 'facebook.jsonl'
    directory = '/home/victor/Desktop/TILES/data/Facebook'
    outputFolder = '/home/victor/Desktop/TILES/data/Facebook/Processed'
    """
    dictList = (LoadJson(fileName, directory))
    splitDataFrameIntoPersonalFiles(dictList, outputFolder)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        
        fileName = sys.argv[1]
        directory = sys.argv[2]
        outputFolder = sys.argv[3]
        main(fileName, directory, outputFolder)
    else:
        print ("Please provide the following command line arguments:")
        print ("name of the json file + the path to the json file + where do you want to store the results")
