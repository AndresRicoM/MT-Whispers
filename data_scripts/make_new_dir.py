import os

#Assign Path Names
print('Type Name of New Data Set:')
data_name = input() #'test_000000'

rm_raw_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/' + data_name + '/RM'
lm_raw_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/' + data_name + '/LM'
gps_conv_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/processed/modified/' + data_name + '/gps_correction'
merged_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/processed/merged/' + data_name + '/interpolated'

#Create New Directories.
print('Making New Directories...')
try:
    os.makedirs(rm_raw_path)
    os.makedirs(lm_raw_path)
    os.makedirs(gps_conv_path)
    os.makedirs(merged_path)
    print('Finished Making new Directories!')
except:
    print('Direcotries already exist!')
