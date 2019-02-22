#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 22:54:34 2018

Input: 
    a sequence of integer number: 'seq'
    window size: 'width'
    step size: 'stepsize'
Output:
    a set of unique subsequences with the window size 'w'
    
@author: Shariful
"""

#import necessary modules
import scipy.io
import os
import numpy as np
import pandas as pd 


##===============compute unique sliding windows for a given sequence=====
def window_stack(sequence, stepsize=1, width=5):
    # returns all unique windows
    if (width > len(sequence)):
        print('window size is greater than the length of the sequence')
        return
    
    sub_windows = np.hstack(sequence[i:1+i-width or None:stepsize] \
                               for i in range(0,width))
    
    return pd.DataFrame(sub_windows).drop_duplicates()
    

home_dir = '/Users/Shariful/Documents/SysCallDataset/PreparedData/Canali_dataset'

window_size = 5
step_size = 1

for filename in os.listdir(home_dir):
    
    file_path = home_dir + '/' + filename
    
    if not os.path.isfile(file_path) or filename == '.DS_Store':
        continue
    
    seqs = scipy.io.loadmat(file_path) # seqs is a dict 
    
    #dict does not allow indexing, so convert it into list of objects
    seqs = list(seqs.values()[0])

    all_windows_df = pd.DataFrame()
    for sequence in seqs:
        sequence = np.array(list(sequence)) 
        sequence = list(sequence.reshape(sequence.shape[2]))
        sequence = np.array(sequence).reshape(-1,1)
        sub_windows_df = window_stack(sequence, step_size, window_size)
        all_windows_df = pd.concat([all_windows_df, sub_windows_df])
    
    all_unique_windows_df = all_windows_df.drop_duplicates()
    
    save_path = home_dir + '/sliding_window_5/' + filename.split('.')[0] + '.csv'
    all_unique_windows_df.to_csv(save_path, header=False, index=False)
