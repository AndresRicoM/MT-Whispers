#Convert

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import math
from interpolation import interpolate

def delete_zeros(data_set):
    first = True
    for rows in range(0, data_set.shape[0]):
        if first:
            clean_data = data_set[rows,:]
            first = False
        elif (data_set[rows, 1] < -1) or (data_set[rows, 1] > 1) and (data_set[rows, 3]) < -1 or (data_set[rows, 3] > 1):
            #print(data_set[rows, 3])
            clean_data = np.vstack((clean_data, data_set[rows,:]))
    return clean_data

def convert_gps(input_data_path, output_data_path):
    #input_data_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/metepec_230320/LM/'
    #output_data_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/processed/modified/metepec_230320/gps_correction/'

    data_labels = ['millis', 'latitude', 'coord1', 'longitude', 'coord2', 'altitude','capacitive','flag', 'original_lat', 'original_lon', 'used_lat', 'used_lon']

    for filename in os.listdir(input_data_path):

        if filename != '.DS_Store':

            current_data = np.genfromtxt(input_data_path + filename, delimiter = ',',  invalid_raise=False) #,  dtype='str')
            current_data = delete_zeros(current_data)
            original = np.zeros((current_data.shape[0], 4))
            #original_lon = np.zeros((current_data.shape[0], 1))
            current_data = np.hstack((current_data, original))

            current_data[:,-4] = current_data[:,1]
            current_data[:,-3] = current_data[:,3]

            print (filename)

            to_check = 0
            for rows in range(0, current_data.shape[0]): #Interpolates

                interpolated = False
                spaces = 0

                if rows == to_check:

                    if rows == current_data.shape[0] - 1: #Exit loop when reaching last value.
                        break

                    #Check if current value is the same as next value.
                    if current_data[rows,1] == current_data[rows + 1, 1]:
                        current_data[rows, -2] = 1
                        spaces = spaces + 1 #Begin looking for amount of values that are the same and store in spaces.

                        blank = False
                        while not blank:
                            if rows + spaces + 1 == current_data.shape[0]:
                                break
                            if current_data[rows, 1] == current_data[rows + spaces + 1, 1]:
                                spaces = spaces + 1
                            else:
                                blank = True
                                interpolated = True

                    if interpolated:

                        interpolated = False
                        interpolator_lat = np.zeros((spaces + 1,1))

                        interpolator_lat = interpolate(current_data[rows, 1], current_data[rows + spaces + 1, 1], spaces + 1)

                        for coords in range(0,interpolator_lat.shape[0]):
                            current_data[rows + coords, 1] = interpolator_lat[coords, 0]

                        to_check = to_check + spaces + 1
                        #print('Check: ', to_check)

            to_check = 0
            for rows in range(0, current_data.shape[0]): #Interpolates

                interpolated = False
                spaces = 0

                if rows == to_check:

                    if rows == current_data.shape[0] - 1: #Exit loop when reaching last value.
                        break

                    #Check if current value is the same as next value.
                    if current_data[rows,3] == current_data[rows + 1, 3]:
                        current_data[rows, -1] = 1
                        spaces = spaces + 1 #Begin looking for amount of values that are the same and store in spaces.

                        blank = False
                        while not blank:
                            if rows + spaces + 1 == current_data.shape[0]:
                                break
                            if current_data[rows + spaces, 3] == current_data[rows + spaces + 1, 3]:
                                spaces = spaces + 1
                            else:
                                blank = True
                                interpolated = True

                    if interpolated:

                        interpolated = False
                        interpolator_lon = np.zeros((spaces + 1,1))

                        interpolator_lon = interpolate(current_data[rows, 3], current_data[rows + spaces + 1, 3], spaces + 1)

                        for coords in range(0,interpolator_lon.shape[0]):
                            current_data[rows + coords, 3] = interpolator_lon[coords, 0]

                        to_check = to_check + spaces + 1


            for rows in range(0, current_data.shape[0]): #Converts every coordinate into readable coordinates.

                lat = current_data[rows,1] * .01
                lat_deg = math.floor(lat)
                lat_min = ((lat - lat_deg) * 100) / 60
                dd_lat = lat_deg + lat_min

                lon = current_data[rows,3] * .01
                lon_deg = math.floor(lon)
                lon_min = ((lon - lon_deg) * 100) / 60
                dd_lon = - (lon_deg + lon_min)

                current_data[rows,1] = dd_lat
                current_data[rows,3] = dd_lon

            print(current_data.shape)
            #current_data = np.vstack((data_labels, current_data)) #Add data labels to set for referencing and plotting.
            np.savetxt(output_data_path + filename , current_data, delimiter = ',', fmt = '%s')
            print('Saved ', filename)


                #current_data[rows,-3] = 4 #West
                #current_data[rows,-5] = 1 #North
