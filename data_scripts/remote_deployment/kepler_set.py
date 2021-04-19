import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import math
import datetime

path = '../../collected_data_2/raw/ski1_andorra_D1.txt'
destin_path = '../../collected_data_2/processed/ski1_andorra_D1.csv'
data_labels = ['datetime', 'millis', 'lat', 'coordlat', 'lon', 'coordlon','pressure','altitude', 'temp']

input_data = np.genfromtxt(path, delimiter = ',', dtype='str',  invalid_raise=False) #,  dtype='str')

#for rows in


latitudes = input_data[:,2].astype(np.float)
longitudes= input_data[:,4].astype(np.float)

#Convert coordinates

for rows in range(latitudes.shape[0]):

    lat = latitudes[rows] * .01
    lat_deg = math.floor(lat)
    lat_min = ((lat - lat_deg) * 100) / 60
    dd_lat = lat_deg + lat_min

    lon = longitudes[rows] * .01
    lon_deg = math.floor(lon)
    lon_min = ((lon - lon_deg) * 100) / 60
    dd_lon =  (lon_deg + lon_min)

    latitudes[rows] = dd_lat
    longitudes[rows] = dd_lon

input_data[:,2] = latitudes[:]
input_data[:,4] = longitudes[:]

print(latitudes.shape)

#Adjust GPS Decimals

#Join Independent data sets.
output_data = np.vstack([data_labels, input_data])

print(output_data)
np.savetxt(destin_path, output_data, delimiter = ',', fmt = '%s')
