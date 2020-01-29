#Script for converting GPS coordinates for MapBox use.
#Script for processing incoming Bike Data for MapBox Analisis
#Creates a New File in Processed Data Folder

#Convert GPS Data To

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

data_path = '/home/AndresRico/Desktop/HackBike/raw_data'

#data_labels = ['Time', 'Battery Cell Temperature (C)', 'Battery Voltage (mV)', 'Battery Current Value (mA)', 'Battery Percentage (%)', 'Remaining Distance (0.1km)',
#                'Remaining Time (0.1min)', 'Torque (kgf)', 'Crank Sensor Rotation State', 'Crank Sensor RPM', 'Battery Voltage Sensor Value (mV)', 'Motor Current Sensor Value (mA)', 'Motor Temperature Sensor Value (C)',
#                'Motor Duty', 'Motor RPM', 'Motor Speed (km/h)', 'Motor Encoder Counter', 'Speed Sensor (km/h)', 'Current Mode', 'X Accel', 'Y Accel', 'Z Accel', 'Environmental Temperature', 'Light', 'Humidity', 'Proximity', 'Pressure', 'Altitude', 'Dew Point']

for filename in os.listdir(data_path):
    #current_file = open(data_path + '/' + filename, "r")
    current_data = np.genfromtxt(data_path + '/' + filename, delimiter = ',',  dtype='str')
    #print current_data[0,1]

    for rows in range(current_data.shape[0]):

        if (len(current_data[rows,1]) > 10):
            #print len(current_data[55,1])
            lat = current_data[rows,1]
            lat_deg = float(lat[1:3])
            lat_min = float(lat[3:11])
            #lat_sec = float(lat[6:11]) * .001
            #print lat_min
            dd_lat = (lat_deg + (lat_min / 60))
        else:
            dd_lat = 0

        if (len(current_data[rows,2]) > 10):
            #print len(current_data[60,2])
            lon = current_data[rows,2]
            lon_deg = float(lon[2:5])
            lon_min = float(lon[5:14])
            #lon_sec = float(lon[7:14]) * 100
            #print lon_sec
            dd_lon = (lon_deg + (lon_min / 60)) * -1
        else:
            dd_lon = 0

        current_data[rows,1] = dd_lat
        current_data[rows,2] = dd_lon

    current_data = np.vstack((data_labels, current_data)) #Add data labels to set for referencing and plotting.


        #print dd_lat , dd_lon

    np.savetxt('/home/aricom/Desktop/HackBike/processed_data/' + filename , current_data, delimiter = ',', fmt = '%s')
