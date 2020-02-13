import numpy as np
import math
from progressbar import printProgressBar
from interpolation import interpolate

output_data = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/processed/merged/killington/interpolated/'

rm_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/Killington_250120/RM'
lm_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/processed/modified/killington/gps_correction'

rm_file = '/2.csv'
lm_file = '/2.csv'

#for filename in os.listdir(lm_path):

rm = np.genfromtxt(rm_path + rm_file, delimiter = ',', usecols=np.arange(0,24), invalid_raise=False)
lm = np.genfromtxt(lm_path + lm_file, delimiter = ',')

rm[:,0] = rm[:,0] - rm[0,0] #Adjust timestamps to start from 0.
lm[:,0] = lm[:,0] - lm[0,0]

rm_flag = np.zeros((rm.shape[0],1)) #Add Flag Columns to RM
rm = np.append(rm, rm_flag, axis=1)

lm_flag = np.zeros((lm.shape[0],2)) #Add Flag Columns to LM
lm = np.append(lm, lm_flag, axis=1)

#rm = rm[0:5,:]
#lm = lm[0:5,:]

data_labels = ['time', 'p1', 'p2', 'p3', 'p4', 'p5', 'termite', 'ax', 'ay', 'az', 'rx', 'ry', 'rz', 'roll', 'pitch', 'yaw',
                'q1', 'q2', 'q3', 'q4' ,'calibration', 'temperature', 'humidity', 'pressure', 'flag_rm','lat', 'lacoord',
                'lon', 'locoord', 'capacitive', 'o_lat', 'o_lon', 'used_lat', 'used_lon', 'altitude' , 'flag_lm']

fast_data = np.zeros((rm.shape[0], rm.shape[1] + lm.shape[1] - 1)) #Create new array to store new data set.

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
np.savetxt(output_data + 'pre.csv' , fast_data, delimiter = ',', fmt = '%s')

np.savetxt(output_data + 'pre.csv' , fast_data, delimiter = ',', fmt = '%s')

print('Fixing empty GPS and Capacitance...')
printProgressBar(0, fast_data.shape[0], prefix = 'Filling in missing GPS and Capacitance...', suffix = 'Complete', length = 20)

for rows in range(0, fast_data.shape[0]): #Interpolates latitudes

    interpolated = False
    spaces = 0

    if rows == fast_data.shape[0] - 1: #Exit loop when reaching last value.
        break

    #Check if fast value is the same as next value.
    if fast_data[rows,-11] == 0:
        fast_data[rows,-6] = fast_data[rows-1, -6]
        spaces = spaces + 1 #Begin looking for amount of values that are the same and store in spaces.
        blank = False
        while not blank:
            if fast_data[rows + spaces, -11] == 0:
                spaces = spaces + 1
            else:
                blank = True
                interpolated = True

    if interpolated:
        interpolated = False
        interpolator_lat = np.zeros((spaces + 2,1))

        interpolator_lat = interpolate(fast_data[rows-1, -11], fast_data[rows + spaces, -11], spaces + 2)
        print(interpolator_lat)
        for coords in range(0,interpolator_lat.shape[0]):
            if coords != interpolator_lat.shape[0] - 1 and coords != 0:
                fast_data[rows + coords - 1, -11] = interpolator_lat[coords, 0]

    interpolated = False
    spaces = 0

    if rows == fast_data.shape[0] - 1: #Exit loop when reaching last value.
        break

    #Check if fast value is the same as next value.
    if fast_data[rows,-9] == 0:
        fast_data[rows,-5] = fast_data[rows-1, -5]
        spaces = spaces + 1 #Begin looking for amount of values that are the same and store in spaces.
        blank = False
        while not blank:
            if fast_data[rows + spaces, -9] == 0:
                spaces = spaces + 1
            else:
                blank = True
                interpolated = True

    if interpolated:
        interpolated = False
        interpolator_lat = np.zeros((spaces + 2,1))

        interpolator_lat = interpolate(fast_data[rows-1, -9], fast_data[rows + spaces, -9], spaces + 2)
        print(interpolator_lat)
        for coords in range(0,interpolator_lat.shape[0]):
            if coords != interpolator_lat.shape[0] - 1 and coords != 0:
                fast_data[rows + coords - 1, -9] = interpolator_lat[coords, 0]



    printProgressBar(rows, fast_data.shape[0], prefix = 'Filling in missing GPS and Capacitance...', suffix = 'Complete', length = 20)


print('Saving file...')
fast_data = np.vstack((data_labels, fast_data)) #Add data labels to set for referencing and plotting.
np.savetxt(output_data + 'interpolated.csv' , fast_data, delimiter = ',', fmt = '%s')

print('Finished!')
