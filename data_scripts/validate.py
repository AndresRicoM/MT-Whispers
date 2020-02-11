#Validation script for ski data. Makes sure data has correct structure and no errors.

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
from matplotlib import gridspec

print('Validation Starting...')

rm_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/Killington_250120/RM'
lm_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/Killington_250120/LM'

rm_file = '/3.csv'
lm_file = '/3.csv'

print('Importing Files')

rm = np.genfromtxt(rm_path + rm_file, delimiter = ',', usecols=np.arange(0,24), invalid_raise=False)
lm = np.genfromtxt(lm_path + lm_file, delimiter = ',')

print('Finished Importing Files!')

print('Getting Data Stats...')

print('Shape of RM is: ' , rm.shape)
print('Size of RM is: ' , rm.size)
print('Total time of collection: ', (rm[rm.shape[0] - 1,0] - rm[0,0]) / 60000)
print('Frequency of collection: ', rm.shape[0] / ((rm[rm.shape[0] - 1,0]) / 1000))

print('Shape of LM is: ' , lm.shape)
print('Size of LM is: ' , lm.size)
print('Total time of collection: ', (lm[lm.shape[0] - 1,0] - lm[0,0]) / 60000)
print('Frequency of collection: ', lm.shape[0] / ((lm[lm.shape[0] - 1,0]) / 1000))

print('Reviewing piezo sensor values...')

values = 0

for i in range (rm.shape[0]):
    for col in range (5):
        if rm[i, 1] == rm[i, col]:
            values = values + 1

print('Found % equal values were found' %int(values))

print('Generating Data Visualization')

plt.style.use('dark_background')

gs = gridspec.GridSpec(2,1)
fig = plt.figure()
dot_size = 3


#for i in range (6):
#    if i > 0:
#        ax = fig.add_subplot(gs[i - 1])
#        ax.plot(rm[:,0],rm[:,i])
#        ax.set_ylabel(r'Piezo', size =16)

"""
sensor_num = [1,2,3,4]

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlabel('Piezo')
ax.set_ylabel('Time')
ax.set_zlabel('Sensor Number')
img = ax.scatter3D(rm[:,0], X[:, 1], X[:, ])
plt.show()
"""

ax = fig.add_subplot(gs[0])
ax.plot(rm[:,0],rm[:,5], 'y')
ax.plot(rm[:,0],rm[:,2], 'g')
ax.plot(rm[:,0],rm[:,3], 'b')
ax.plot(rm[:,0],rm[:,1],'r')

ax.set_ylabel(r'Piezo Array', size =16)

ax = fig.add_subplot(gs[1])
ax.plot(rm[:,0],rm[:,7],'r')
ax.plot(rm[:,0],rm[:,8], 'g')
ax.plot(rm[:,0],rm[:,9], 'b')
#ax.plot(rm[:,0],rm[:,23], 'y')
ax.set_ylabel(r'Pressure', size =16)

print("Showing Piezo and Accelerometer Readings...")

plt.show()

print("Showing Capacitive Readings...")

plt.plot(rm[:,0],rm[:,23])
plt.show()

#"""

print("Data sets are valid!")
