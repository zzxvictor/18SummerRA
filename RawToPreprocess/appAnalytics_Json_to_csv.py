#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 11:39:58 2018

@author: victorzhang
"""


import pandas as pd
import sys 
import os

def extractions(path, name, path_save):
    os.chdir(path)
    df_aa = pd.read_json(name,lines=True)
    df_aa = df_aa.sort_values(['participant_id','event']).reset_index(drop=True)
    uid_list = list(set(df_aa['participant_id']))
    uid_list.sort()
    event_list = list(set(df_aa['event']))
    event_list.sort()
    
    uid_dic = {}
    for uid in uid_list:
        value_dic = {}
        for event in event_list:
            value_dic[event] = 0
        uid_dic[uid] = value_dic
    
    for uid in uid_list:
        temp = df_aa[df_aa['participant_id'] == uid]['event'].value_counts()
        for i in range(len(temp)):
            uid_dic[uid][temp.index[i]] = temp[i]
            
    result = []
    for uid in uid_list:
        temp = [uid]
        for event in event_list:
            temp.append(uid_dic[uid][event])
        result.append(temp)
        
    df_result = pd.DataFrame(result,columns=['uid']+event_list)
    df_result.to_csv(path_save+'App_Analytics.csv',index=False)
    
if __name__ == '__main__':
   if len(sys.argv) > 2:
      in_path = sys.argv[1]
      out_path = sys.argv[2]
      extractions(in_path,'tiles_app_analytics.jsonl', out_path)
   else:
      print('Please provide the following command line arguments:\n 1) Path to folder containing omsignal CSV files\n 2) Output folder path for preprocessed omsignal CSVs')
