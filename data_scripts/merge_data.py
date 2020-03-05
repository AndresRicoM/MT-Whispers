import numpy as np
import math
from progressbar import printProgressBar
from interpolation import interpolate
import os

output_data = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/processed/merged/wachusetts/interpolated/'

rm_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/Wachusetts_030320/RM/'
lm_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/processed/modified/wachusetts/gps_correction/'

data_labels = ['time', 'p1', 'p2', 'p3', 'p4', 'p5', 'termite', 'ax', 'ay', 'az', 'rx', 'ry', 'rz', 'roll', 'pitch', 'yaw',
                'q1', 'q2', 'q3', 'q4' ,'calibration', 'temperature', 'humidity', 'pressure', 'flag_rm','lat', 'lacoord',
                'lon', 'locoord', 'capacitive', 'o_lat', 'o_lon', 'used_lat', 'used_lon', 'altitude' , 'flag_lm']


for filename in os.listdir(lm_path):

    if filename != '.DS_Store':

        print('Beginning to process file: ', filename)
        rm = np.genfromtxt(rm_path + filename, delimiter = ',', usecols=np.arange(0,24), invalid_raise=False)
        lm = np.genfromtxt(lm_path + filename, delimiter = ',')

        rm[:,0] = rm[:,0] - rm[0,0] #Adjust timestamps to start from 0.
        lm[:,0] = lm[:,0] - lm[0,0]

        rm_flag = np.zeros((rm.shape[0],1)) #Add Flag Columns to RM
        rm = np.append(rm, rm_flag, axis=1)

        lm_flag = np.zeros((lm.shape[0],2)) #Altitude and Flags
        lm = np.append(lm, lm_flag, axis=1)

        lm[:,-1] = lm[:,6]

        lm = np.delete(lm, 6, 1)

        print("Cleaning RM Data Set")
        check_array = np.isnan(rm[:,6])
        printProgressBar(0, check_array.shape[0], prefix = 'Cleaning RM...', suffix = 'Complete', length = 20)
        for rows in range(0, check_array.shape[0]):
            if check_array[rows] != True:
                np.delete(rm[rows,:])
            printProgressBar(rows, check_array.shape[0], prefix = 'Cleaning RM...', suffix = 'Complete', length = 20)

        print()
        print("Checking Pressure Values")
        first = True
        print(rm.shape[0])
        printProgressBar(0, rm.shape[0], prefix = 'Checking Pressure...', suffix = 'Complete', length = 20)
        for rows in range(0,rm.shape[0]):
            if first:
                clean_data = rm[rows,:]
                first = False
            elif rm[rows,-2] < .9999:
                clean_data = np.vstack((clean_data,rm[rows,:]))
            printProgressBar(rows, rm.shape[0], prefix = 'Checking Pressure...', suffix = 'Complete', length = 20)

        rm = clean_data
        print(rm.shape[0])

        fast_data = np.zeros((rm.shape[0], rm.shape[1] + lm.shape[1] - 1)) #Create new array to store new data set.

        print()
        print('Filling in complete fast data...')
        printProgressBar(0, rm.shape[0], prefix = 'Filling in fast data...', suffix = 'Complete', length = 20)

        for rows in range(rm.shape[0]):
            fast_data[rows,0:25] = rm[rows,:]
            #print(fast_data[rows,:])
            printProgressBar(rows, rm.shape[0], prefix = 'Filling in fast data...', suffix = 'Complete', length = 20)
        print( )

        print('Joining GPS...')
        printProgressBar(0, lm.shape[0], prefix = 'Looking for closest GPS stamps...', suffix = 'Complete', length = 20)
        for rows in range(lm.shape[0]):
            test_array = abs(rm[:,0] - lm[rows,0])
            fast_data[np.argmin(test_array),25:] = lm[rows,1:]
            #print(fast_data[np.argmin(test_array),:])
            printProgressBar(rows, lm.shape[0], prefix = 'Looking for closest GPS stamps...', suffix = 'Complete', length = 20)
        #print(fast_data)

        print('Adding LM...')
        printProgressBar(0, fast_data.shape[0], prefix = 'Filling in LM...', suffix = 'Complete', length = 20)
        for rows in range (0, fast_data.shape[0]):
            if fast_data[rows,-11] == 0:
                fast_data[rows,25:32] = fast_data[rows-1,-11:-4]
            printProgressBar(rows, fast_data.shape[0], prefix = 'Filling in zeros...', suffix = 'Complete', length = 20)


        print('Saving file...')
        #print(data_labels.shape)
        fast_data = np.vstack((data_labels, fast_data)) #Add data labels to set for referencing and plotting.
        np.savetxt(output_data + filename , fast_data, delimiter = ',', fmt = '%s')
        print('Finished saving file: ' , filename)

print('Finished All Files!')
