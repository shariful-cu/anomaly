#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 10:28:15 2019

@author: Shariful
"""
from __future__ import division
import pandas as pd
import os

def df_to_excel(df, file_name):

    writer = pd.ExcelWriter(file_name+'.xlsx')
    df.to_excel(writer, sheet_name='Sheet')
    writer.save()


data_dir = '/Users/Shariful/Documents/Rahul/Gnome'

#br_fields = ['Component', 'Product', 'Severity', 'Priority', 'Os', \
#                    'Version', 'Assignee', 'Status']

field_statistic = {}
for filename in os.listdir(data_dir):
    
    file_path = data_dir + '/' + filename
    
    if not os.path.isfile(file_path) or filename == '.DS_Store':
        continue
    
    field_ids = pd.ExcelFile(file_path)
    field_ids = field_ids.parse('Sheet')
    
    reassign_ids = field_ids.iloc[:,0].dropna().unique()
    not_reassign_ids = field_ids.iloc[:,1].dropna().unique()
    
    br_ids = len(reassign_ids) + len(not_reassign_ids)
    
    reassign_pct = (len(reassign_ids) / br_ids) * 100
    
    not_reassign_pct = (len(not_reassign_ids) / br_ids) * 100
    
    
    check_unique = len([reassign_id for reassign_id in reassign_ids \
                    if reassign_id in not_reassign_ids])
    if check_unique: 
        print ('ERROR: there has common bug ID')
        break
    
    field_statistic[filename] = [br_ids, reassign_pct, not_reassign_pct]
    
file_name = data_dir + '/eclispe_info' 
    
field_statistic_df = pd.DataFrame(field_statistic)

df_to_excel(field_statistic_df, file_name)
