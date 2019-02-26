#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 10:28:15 2019

@author: Shariful
"""
import pandas as pd
import os

data_dir = '/Users/Shariful/Documents/Rahul/Eclipse'

br_fields = ['Component', 'Product', 'Severity', 'Priority', 'OS', \
                    'Version', 'Assigtne', 'Status']

for filename in os.listdir(data_dir):
    field_ids = pd.ExcelFile(data_dir + '/' + filename)
    field_ids = field_ids.parse('Sheet')

# read SMLV data from Excel and prepare smlv_df DataFrame
smlv_df = pd.ExcelFile(data_dir + '/SMLV.xlsx')
smlv_df = smlv_df.parse('Sheet1')
smlv_list = []
for i in range(len(smlv_df)):
    val = smlv_df.iloc[i]
    smlv_list.append(str(val[0]).split('  ')) 

smlv_df = pd.DataFrame(smlv_list)
smlv_df.columns = ['Date', 'SMLV']
smlv_df.index = pd.to_datetime(smlv_df['Date'])
smlv_df = smlv_df.drop('Date', axis=1)
smlv_df['SMLV'] = smlv_df['SMLV'].astype(float)