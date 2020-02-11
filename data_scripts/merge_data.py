import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
from matplotlib import gridspec
import math
from progressbar import printProgressBar

output_data = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/processed/merged/killington/'

rm_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/Killington_250120/RM'
lm_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/Killington_250120/LM'

#output_name =

rm_file = '/3.csv'
lm_file = '/3.csv'

rm = np.genfromtxt(rm_path + rm_file, delimiter = ',', usecols=np.arange(0,24), invalid_raise=False)
lm = np.genfromtxt(lm_path + lm_file, delimiter = ',')

rm[:,0] = rm[:,0] - rm[0,0] #Adjust timestamps to start from 0.
lm[:,0] = lm[:,0] - lm[0,0]

rm_flag = np.zeros((rm.shape[0],1)) #Add Flag Columns to RM
rm = np.append(rm, rm_flag, axis=1)

lm_flag = np.zeros((lm.shape[0],1)) #Add Flag Columns to LM
lm = np.append(lm, lm_flag, axis=1)

#rm = rm[0:10,:]
#lm = lm[0:10,:]

data_labels = ['time', 'p1', 'p2', 'p3', 'p4', 'p5', 'termite', 'ax', 'ay', 'az', 'rx', 'ry', 'rz', 'roll', 'pitch', 'yaw',
                'q1', 'q2', 'q3', 'q4' ,'calibration', 'temperature', 'humidity', 'pressure', 'flag_rm','lat', 'lacoord',
                'lon', 'locoord', 'capacitive', 'flag_lm']

fast_data = np.zeros((rm.shape[0], rm.shape[1] + lm.shape[1] - 1)) #Create new array to store new data set.

print('Joining GPS...')
printProgressBar(0, lm.shape[0], prefix = 'Looking for closest GPS stamps...', suffix = 'Complete', length = 20)
for rows in range(lm.shape[0]):
    test_array = abs(rm[:,0] - lm[rows,0])
    fast_data[np.argmin(test_array),25:] = lm[rows,1:]
    printProgressBar(rows, lm.shape[0], prefix = 'Looking for closest GPS stamps...', suffix = 'Complete', length = 20)

print('Filling in complete fast data...')
printProgressBar(0, rm.shape[0], prefix = 'Filling in fast data...', suffix = 'Complete', length = 20)

for rows in range(rm.shape[0]):
    fast_data[rows,0:25] = rm[rows,:]
    printProgressBar(rows, rm.shape[0], prefix = 'Filling in fast data...', suffix = 'Complete', length = 20)
print( )

print('Fixing empty GPS and Capacitance...')
printProgressBar(0, fast_data.shape[0], prefix = 'Filling in missing GPS and Capacitance...', suffix = 'Complete', length = 20)

for rows in range(0,fast_data.shape[0]):

    lat = fast_data[rows,-6] * .01 #Converts type of GPS used.
    lat_deg = math.floor(lat)
    lat_min = ((lat - lat_deg) * 100) / 60
    dd_lat = lat_deg + lat_min
    #print(dd_lat)

    lon = fast_data[rows,-4] * .01 #Converts type of GPS units used.
    lon_deg = math.floor(lon)
    lon_min = ((lon - lon_deg) * 100) / 60
    dd_lon = - (lon_deg + lon_min)

    fast_data[rows,-6] = dd_lat
    fast_data[rows,-4] = dd_lon

    if fast_data[rows,-4] == 0:
        fast_data[rows,25:] = fast_data[rows-1,25:]

    fast_data[rows,-3] = 4 #West
    fast_data[rows,-5] = 1 #North

    printProgressBar(rows, fast_data.shape[0], prefix = 'Filling in missing GPS and Capacitance...', suffix = 'Complete', length = 20)

print('Saving file...')

fast_data = np.vstack((data_labels, fast_data)) #Add data labels to set for referencing and plotting.
np.savetxt(output_data + 'ski_merged_3.csv' , fast_data, delimiter = ',', fmt = '%s')

print('Finished!')
