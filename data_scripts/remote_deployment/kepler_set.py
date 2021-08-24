import numpy as np
import os
import math
import datetime
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
from matplotlib import gridspec

path = '../../collected_data_2/raw/porto.txt'
destin_path = '../../collected_data_2/processed/porto.csv'
data_labels = ['datetime', 'millis', 'lat', 'coordlat', 'lon', 'coordlon','pressure','altitude', 'temp']

input_data = np.genfromtxt(path, delimiter = ',', dtype='str',  invalid_raise=False) #,  dtype='str')

#for rows in


latitudes = input_data[:,2].astype(float)
longitudes= input_data[:,4].astype(float)

#Convert coordinates

for rows in range(1):#latitudes.shape[0]):

    #print(latitudes[rows])
    lat = latitudes[rows] * .01
    #print(lat)
    lat_deg = math.floor(lat)
    #print(lat_deg)
    lat_min = ((lat - lat_deg) * 100) / 60
    #print(lat_min)
    dd_lat = lat_deg + lat_min
    #print(dd_lat)

    print(longitudes[rows])
    lon = longitudes[rows] * .01
    lon_deg = math.floor(lon)
    lon_min = ((lon - lon_deg) * 100) / 60
    dd_lon =  (lon_deg + lon_min)
    print(dd_lon)

    latitudes[rows] = dd_lat
    longitudes[rows] = dd_lon

input_data[:,2] = latitudes[:]
input_data[:,4] = longitudes[:]

#Join Independent data sets.
output_data = np.vstack([data_labels, input_data])
np.savetxt(destin_path, output_data, delimiter = ',', fmt = '%s')

#Visualization
plt.style.use('dark_background')

gs = gridspec.GridSpec(3,1)
fig = plt.figure()
dot_size = 3


ax = fig.add_subplot(gs[0])
ax.plot(input_data[:,1].astype(float),input_data[:,6].astype(float), 'cyan')
ax.set_ylabel(r'Pressure (Pa)', size =16)

ax = fig.add_subplot(gs[1])
ax.plot(input_data[:,1].astype(float),input_data[:,7].astype(float), 'magenta')
ax.set_ylabel(r'Altitude (m)', size =16)

ax = fig.add_subplot(gs[2])
ax.plot(input_data[:,1].astype(float),input_data[:,8].astype(float), 'yellow')
ax.set_ylabel(r'Temperature (C)', size =16)
ax.set_xlabel(r'Time (millis)', size =16)

fig.suptitle('Andorra Test Deployment', fontsize=32)

#plt.show()
