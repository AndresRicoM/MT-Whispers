import numpy as np
import math
import os

output_data = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/processed/modified/killington/'

rm_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/Killington_250120/RM/'
lm_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/Killington_250120/LM/'

input_data_path = rm_path

for filename in os.listdir(input_data_path):
    if filename != '.DS_Store':
        current_data = np.genfromtxt(input_data_path + filename, delimiter = ',',  invalid_raise=False) #,  dtype='str')
        print(filename)
