#Script for processing incoming Bike Data for MapBox Analisis
#Creates a New File in Processed Data Folder

#Convert GPS Data To

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import math

input_data_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/Killington_250120/LM/'
output_data_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/Killington_250120/processed_LM/'
script_path = '/Users/AndresRico/Desktop/MT_Whispers/data_scripts/'

data_labels = ['millis', 'latitude', 'coord1', 'longitude', 'coord2', 'capacitive']

for filename in os.listdir(input_data_path):

    current_data = np.genfromtxt(input_data_path + filename, delimiter = ',') #,  dtype='str')
    #np.array2string(current_data)
    print current_data[0,1]

    for rows in range(current_data.shape[0]):

        lat = current_data[rows,1]
        lat_deg = math.floor(lat)
        lat_min = ((lat - lat_deg) * 100) / 60
        dd_lat = lat_deg + lat_min
        #print(dd_lat)

        lon = current_data[rows,3]
        lon_deg = math.floor(lon)
        lon_min = ((lon - lon_deg) * 100) / 60
        dd_lon = - (lon_deg + lon_min)
        #print(dd_lon)

        """

        if (len(current_data[rows,1]) > 7):
            #print len(current_data[55,1])
            lat = current_data[rows,1]
            lat_deg = float(lat[1:3])
            lat_min = float(lat[3:11])
            #lat_sec = float(lat[6:11]) * .001
            #print lat_min
            dd_lat = (lat_deg + (lat_min / 60))
        else:
            dd_lat = 0



        if (len(current_data[rows,3]) > 7):
            #print len(current_data[60,2])
            lon = current_data[rows,2]
            lon_deg = float(lon[2:5])
            lon_min = float(lon[5:14])
            #lon_sec = float(lon[7:14]) * 100
            #print lon_sec
            dd_lon = (lon_deg + (lon_min / 60)) * -1
        else:
            dd_lon = 0

        """

        current_data[rows,1] = dd_lat
        current_data[rows,3] = dd_lon

    current_data = np.vstack((data_labels, current_data)) #Add data labels to set for referencing and plotting.



    np.savetxt(output_data_path + filename , current_data, delimiter = ',', fmt = '%s')
