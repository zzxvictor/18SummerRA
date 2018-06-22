#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 13:36:05 2018

@author: victorzhang
"""

import numpy as np
import pandas as pd
from datetime import datetime
import os
import sys

def igbtFeaturextraction(fileName, inPath):
    os.chdir(inPath)
    df = pd.read_csv(fileName)
    df = df.drop('igtb_incomplete',axis=1)
    df.columns = ['uid','timestamp','shipley_voc','shipley_abs','irb','itp','ocb','iod_id','iod_od','ext',
              'agr','con','neu','ope','pos_af','neg_af','stai','audit','gats_status','gats_quantity','gats_quantity_sub',
              'ipaq','psqi']
    columns_list = ['uid','timestamp','itp','irb','iod_id','iod_od','ocb','shipley_abs','shipley_voc','neu',
                'con','ext','agr','ope','pos_af','neg_af','stai','audit','gats_status','gats_quantity',
                'ipaq','psqi']
    df = df[columns_list]
    columns_list = [item+'_igtb' if item not in ['uid','timestamp'] else item for item in columns_list]
    df.columns = columns_list
    df_result = df.copy()
    for feature in df_result.columns:
        if feature not in ['uid','survey_type','timestamp','gats_status_igtb']:
            df_result[feature] = pd.to_numeric(df_result[feature],errors='coerce',downcast='float')
        elif feature in ['timestamp']:
            df_result[feature] = [datetime.strftime(datetime.strptime(item,'%Y-%m-%d %H:%M:%S'), '%Y-%m-%dT%H:%M:%S.%f' )for item in df_result[feature]]
        elif feature in ['gats_status_igtb']:
            df_result[feature] = [item if item in ['never','current','past'] else np.nan for item in df_result[feature]]
    df_result['gats_status_igtb'] = df_result['gats_status_igtb'].map({'never':0.0,'past':1.0,'current':2.0})
    df_result = df_result[~df_result.uid.str.contains('PILOT')]
    df_result = df_result.sort_values(['uid','timestamp']).reset_index(drop=True)
    df_result['timestamp'] = [item for item in df_result['timestamp']]
    return df_result

def demographicsFeatureExtraction(fileName, input):
    os.chdir(input)
    df_dg = pd.read_csv(fileName, sep = ',')
    df_dg = df_dg[['Name','gender','age','bornUS','lang','educ','jobstat','occup','supervise','size','duration','income']]
    df_dg.columns = ['uid','gender','age','bornUS','language','education','jobstat','occupation','supervise','supervise_size','employer_duration','income']
    df_dg = df_dg.sort_values('uid')
    return df_dg

def innerJoin(left, right, key):
    result = pd.merge(left, right, on = key, how = 'inner')
    return result

def reformat(table, idMap):
    #rename a column 
    idMap.rename(columns = {'user_id':'uid'}, inplace = True)
    #left join 
    newTable = pd.merge(table, idMap, on = 'uid', how = 'left')
    #swap  columns
    columns = ['timestamp', 'OMuser_id', 'gender', 'age', 'bornUS', 'language', 'education',
                 'jobstat', 'occupation', 'supervise', 'supervise_size', 'employer_duration',
                 'income', 'itp_igtb', 'irb_igtb', 'iod_id_igtb', 'iod_od_igtb', 
                 'ocb_igtb', 'shipley_abs_igtb', 'shipley_voc_igtb', 'neu_igtb', 'con_igtb', 
                 'ext_igtb', 'agr_igtb', 'ope_igtb', 'pos_af_igtb', 'neg_af_igtb', 'stai_igtb', 
                 'audit_igtb', 'gats_status_igtb', 'gats_quantity_igtb', 'ipaq_igtb', 'psqi_igtb'
                 ]
    newTable = newTable [columns]
    #rename 
    newTable.columns = ['Timestamp' if x=='timestamp' else 'participant_id' if x == 'OMuser_id' else x    for x in newTable.columns  ]
    return newTable
if __name__ == '__main__':
   if len(sys.argv) == 6:
      in_path = sys.argv[1]
      out_path = sys.argv[2]
      fileName1 = sys.argv[3]
      fileName2 = sys.argv[4]
      fileName3 = sys.argv[5]
      
      idMap = pd.read_csv(in_path+'/'+fileName3, sep = ',')
      demograohics = demographicsFeatureExtraction(fileName1, in_path)
      others = igbtFeaturextraction(fileName2, in_path)
      #join two tables
      result = innerJoin(demograohics,others, 'uid')
      os.chdir(out_path)
      #convert to new IDs and move Timestampe Column to the first
      result = reformat(result, idMap)
      result.to_csv('igtb_comprehensive.csv', sep = ',', index = False)
   else:
      print('Please provide the following command line arguments:\n 1) Path to folder containing omsignal CSV files\n 2) Output folder path for preprocessed omsignal CSVs')
