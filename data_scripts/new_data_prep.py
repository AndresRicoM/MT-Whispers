# Main Processing Script for Collected Data.
import numpy as np
import os
from gps_coord_conv import *
from merge_data import *

print('Input Data Set To Process:')
to_process = input()

rm_raw_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/' + to_process + '/RM/'
lm_raw_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/' + to_process + '/LM/'
gps_conv_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/processed/modified/' + to_process + '/gps_correction/'
merged_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/processed/merged/' + to_process + '/interpolated/'

print('Making New Directories...')
try:
    os.makedirs(rm_raw_path)
    os.makedirs(lm_raw_path)
    os.makedirs(gps_conv_path)
    os.makedirs(merged_path)
    print('Finished Making new Directories!')
except:
    print('Direcotries already exist!')

input('Load Files to Raw Folders... Press ENTER when done loading')

#Convert GPS
print('Starting GPS conversion...')
convert_gps(lm_raw_path, gps_conv_path)
print('Finished GPS conversion!')


#Merge Data Set
print('Starting Data Merge...')
merge_data(rm_raw_path, gps_conv_path, merged_path)
print('Finished Merging Data!')

print('Data is READY!!! =)')
