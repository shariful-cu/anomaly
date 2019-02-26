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

test_files = ['machine10.mat', 'malware.mat', 'malware-test.mat']

train_normal_df = pd.DataFrame()
test_df = pd.DataFrame()
test_index_label = np.empty([0,3], int)
next_start_test_idx = 0

window_size = 5
step_size = 1
start_index = 0
flag_test = False

for filename in os.listdir(home_dir):
    
    file_path = home_dir + '/' + filename
    
    if not os.path.isfile(file_path) or filename == '.DS_Store':
        continue
    
    print('============ processing file: {} ============'.format(filename))
#    setting class label of the processed observation sequences
    if filename in test_files:
        flag_test = True
        if filename == 'machine10.mat':
            labels = 0
        else:
            labels = 1
    else:
        labels = 0
    
    seqs = scipy.io.loadmat(file_path) # seqs is a dict 
    
    #dict does not allow indexing, so convert it into list of objects
    seqs = list(seqs.values()[0])
    
    print('-- processing {} sequences from {}'.format(len(seqs), filename))
    
    all_windows_df = pd.DataFrame()
    start_end_idxs = []
    next_start_idx = next_start_test_idx
    for i, sequence in enumerate(seqs):
        sequence = np.array(list(sequence)) 
        sequence = list(sequence.reshape(sequence.shape[2]))
        sequence = np.array(sequence).reshape(-1,1)
        sub_windows_df = window_stack(sequence, step_size, window_size)
        
        all_windows_df = pd.concat([all_windows_df, sub_windows_df])
        
        start_end_idxs.append([next_start_idx, \
                               next_start_idx + sub_windows_df.shape[0] - 1, \
                               labels])
        
        next_start_idx = next_start_idx + sub_windows_df.shape[0]
    
    
    
    if flag_test:
        test_df = pd.concat([test_df, all_windows_df])
        test_index_label = np.append(test_index_label, \
                                     np.array(start_end_idxs), \
                                     axis=0)
        next_start_test_idx = next_start_idx
    else:
        train_normal_df = pd.concat([train_normal_df, \
                                     all_windows_df.drop_duplicates()])
        
    flag_test = False
    
    print('-- no. of train windows: {}'.format(train_normal_df.shape[0]))
    print('-- no. of test windows: {}'.format(test_df.shape[0]))
    print('============ DONE: {} ============='.format(filename))

# saving training set of sliding normal windows   
save_path = home_dir + '/sliding_window_5/' + 'train_set.csv'
train_normal_df.drop_duplicates().to_csv(save_path, header=False, index=False)

# saving testing set of sliding normal and attack windows   
save_path = home_dir + '/sliding_window_5/' + 'test_set.csv'
test_df.to_csv(save_path, header=False, index=False)

# saving indexes and labels of all unique windows produced by each testing 
# sequence
save_path = home_dir + '/sliding_window_5/' + 'test_set_index_range_label.csv'
pd.DataFrame(test_index_label).to_csv(save_path, header=False, index=False)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
