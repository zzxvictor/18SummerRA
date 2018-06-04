#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 12:07:11 2018

@author: victorzhang
"""
import pandas
import os 
import json 
import numpy
from datetime import datetime 
import sys
"""
get one user's features and convert it into csv file
parameter:
    dictObj: the json dictionary object for one person
    targetFolder: where do you want to save the files
return:
    N/A
"""
def getOneGuysFeature(dictObj, targetFolder):
    #user infor
    userID = dictObj['participant_id']
    media = dictObj['user']['counts']['media']
    follows = dictObj['user']['counts']['follows']
    followedBy = dictObj['user']['counts']['followed_by']
    bio = dictObj['user']['bio']
    profilePic = dictObj['user']['profile_picture']
    
    
    #post info
    postList = dictObj['posts']
    TimeList = []#created time
    likesCountList = [] #likes
    typeList = [] #type
    attribution = [] #attribution
    longitudeList = [] #location
    latitudeList = []
    placeList = []
    
    comments = [] #comments
    insFilter = [] #filters
    links = [] #links
    tags = [] #tags
    userHasLiked = []
    imagesWidth = []
    imageHeight = []
    imageURL = []
    usersInPhotoName1 = []
    usersInphotoID1 = []
    usersInphotoProfile1 = []
    
    usersInPhotoName2 = []
    usersInphotoID2 = []
    usersInphotoProfile2 = []
    
    usersInPhotoName3 = []
    usersInphotoID3 = []
    usersInphotoProfile3 = []
    #redundant information
    followers = [] 
    following = []
    mediaList = []
    bioList = []
    profilePicList = []
    userInPhotoNum = []
    #create a new dataframe to store the features
    newDataFrame = pandas.DataFrame()
    
    
    for eachPost in postList: 
        #timestamp conversion
        unix_timestamp = float(eachPost['created_time'])
        #local_timezone = tzlocal.get_localzone() # get pytz timezone
        local_time = datetime.fromtimestamp(unix_timestamp)         
        TimeList.append (local_time.strftime("%Y-%m-%dT%H:%M:%S:%f"))
        #likes
        likesCountList.append (eachPost['likes']['count'])
        #type of the posts
        typeList.append(eachPost['type'])
        #attributions
        attribution.append(eachPost['attribution'])
        #get locations
        try:
            longitudeList.append(eachPost['location']['longitude'])
            latitudeList.append (eachPost['location']['latitude'])
            placeList.append (eachPost['location']['name'])
        except:
            longitudeList.append(None)
            latitudeList.append (None)
            placeList.append (None)
        #get comments    
        comments.append(eachPost['comments']['count'])
        #get links to the post
        links.append(eachPost['link'])
        #filters used to process the images
        insFilter.append(eachPost['filter'])
        #tags the user included
        tags.append(eachPost['tags'])
        #count how many users are in the photo
        userInPhotoNum.append (len (eachPost))
        try:
            usersInPhotoName1.append(eachPost['users_in_photo'][0]['user']['username'])
        except:
            usersInPhotoName1.append(None)
        try:
            usersInphotoID1.append (eachPost['users_in_photo'][0]['user']['id'])
        except:
            usersInphotoID1.append (None)
        try:
            usersInphotoProfile1.append (eachPost['users_in_photo'][0]['user']['profile_picture'])
        except:
            usersInphotoProfile1.append (None)
            
            
        try:    
            usersInPhotoName2.append(eachPost['users_in_photo'][1]['user']['username'])
        except:
            usersInPhotoName2.append(None)
        try:
            usersInphotoID2.append (eachPost['users_in_photo'][1]['user']['id'])
        except:
            usersInphotoID2.append(None)
        try:
            usersInphotoProfile2.append (eachPost['users_in_photo'][1]['user']['profile_picture'])
        except:
            usersInphotoProfile2.append (None)
            
        try:    
            usersInPhotoName3.append(eachPost['users_in_photo'][2]['user']['username'])
        except:
            usersInPhotoName3.append(None)
        try:
            usersInphotoID3.append (eachPost['users_in_photo'][2]['user']['id'])
        except:
            usersInphotoID3.append(None)
        try:
            usersInphotoProfile3.append (eachPost['users_in_photo'][2]['user']['profile_picture'])
        except:
            usersInphotoProfile3.append (None)
        
        
        userHasLiked.append(eachPost['user_has_liked'])
        #get the information of the images
        imagesWidth.append(eachPost['images']['standard_resolution']['width'])
        imageHeight.append(eachPost['images']['standard_resolution']['height'])
        imageURL.append (eachPost['images']['standard_resolution']['url'])
        #redundant information
        followers.append(followedBy)
        following.append(follows)
        mediaList .append (media)
        bioList.append(bio)
        profilePicList.append(profilePic)
        

    
    newDataFrame ['Timestamp'] = TimeList
    newDataFrame ['instagramLikesCount'] = likesCountList
    newDataFrame ['instagramPostType'] = typeList
    newDataFrame ['instagramAttribution'] = attribution
    
    newDataFrame ['instagramLongitude'] = longitudeList
    newDataFrame ['instagramLatitude'] = latitudeList
    newDataFrame ['instagramLocation'] = placeList
    
    newDataFrame ['instagramCommentsNum'] = comments
    newDataFrame ['instagramPostLinks'] = links
    newDataFrame ['instagramFilter'] = insFilter
    newDataFrame ['instagramTagsInPost'] = tags
    
    newDataFrame ['instagramUsersInPhotoName1'] = usersInPhotoName1
    newDataFrame ['instagramUsersInPhotoName2'] = usersInPhotoName2
    newDataFrame ['instagramUsersInPhotoName3'] = usersInPhotoName3
    newDataFrame ['instagramUsersInPhotoID1'] = usersInphotoID1
    newDataFrame ['instagramUsersInPhotoID2'] = usersInphotoID2
    newDataFrame ['instagramUsersInPhotoID3'] = usersInphotoID3
    newDataFrame ['instagramUsersInPhotoProfile1'] = usersInphotoID1
    newDataFrame ['instagramUsersInPhotoProfile2'] = usersInphotoID2
    newDataFrame ['instagramUsersInPhotoProfile3'] = usersInphotoID3
    
    newDataFrame ['instagramUsersHasLiked'] = userHasLiked
    newDataFrame ['instagramImageWidth'] = imagesWidth
    newDataFrame ['instagramImageHeight'] = imageHeight
    newDataFrame ['instagramImageURL'] = imageURL
    
    newDataFrame ['instagramFollowersNum'] = followers
    newDataFrame ['instagramFollowingNum'] = following
    newDataFrame ['instagramMediaNum'] = media
    newDataFrame ['instagramUserBio'] = bioList
    newDataFrame ['instagramProfilePic'] =profilePicList
    
    newName = userID + '_instagram' +'.csv'
    saveToCSV(newDataFrame, newName, targetFolder)
    
    
"""
open the instagram json file
parameter:
    fileName:the name of the json file
    directory:where the json is
return:
    jsonDictList: a list of dictionaries
"""
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

"""
save a json file
parameter:
    dataFrame: the data you want to save
    newName: the name the new file should use
    newDirectory: where you want to store the file
return:
    N/A
    
"""
def saveToCSV(dataFrame, newName, newDirectory):
    currentPath = os.getcwd()
    #change to the new directory
    os.chdir(newDirectory)
    dataFrame.to_csv(newName, sep =',' , index = False)
    #go back 
    os.chdir(currentPath)

"""
conver the entire json into many smaller csv 
parameter:
    jsonDictList: a list of json dictionaries
    targetFolder: where you want to save the files 
return:
    N/A
"""
def convertJSONToDataFrame(jsonDictList, targetFolder):
    for oneGuy in jsonDictList:
        getOneGuysFeature(oneGuy, targetFolder)


 
def main (fileDirectory,fileName,targetFolder ):
    """
    fileDirectory = '/home/victor/Desktop/TILES/data/Instagram '
    fileName = 'instagram.jsonl'
    targetFolder = '/home/victor/Desktop/TILES/data/Instagram /processed'
    """

    dictList = openJSON(fileName, fileDirectory)
    convertJSONToDataFrame(dictList, targetFolder)
    
    
if __name__ == '__main__':
    if len(sys.argv) > 3:
        
        fileName = sys.argv[1]
        targetFolder = sys.argv[2]
        currentFolder = sys.argv[3]
        main(currentFolder, fileName, targetFolder)
    else:
        print ("Please provide the following command line arguments:")
        print ("name of the json file + where do you want to store the results + the path to the json file ")
