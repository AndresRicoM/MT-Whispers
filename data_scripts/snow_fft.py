import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
from matplotlib import gridspec

print('Importing Data...')

rm_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/Killington_250120/RM'
#lm_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/Killington_250120/LM'

rm_file = '/4.csv'
#lm_file = '/4.csv'

rm = np.genfromtxt(rm_path + rm_file, delimiter = ',', usecols=np.arange(0,24), invalid_raise=False)
#lm = np.genfromtxt(lm_path + lm_file, delimiter = ',')

print('Data Imported!')

print('Calculating FFT for Piezo and Accel Data')

p1 = np.fft.rfft(rm[:,1])
p2 = np.fft.rfft(rm[:,2])
p3 = np.fft.rfft(rm[:,3])
p4 = np.fft.rfft(rm[:,4])
p5 = np.fft.rfft(rm[:,5])

print('Getting frequencies...')

sum = 0
for rows in range(rm.shape[0]):
    if rows != rm.shape[0] - 1:
        delta = rm[rows + 1,0] - rm[rows,0]
        #print(delta)
        sum = sum + delta


average_delta = (sum / rm.shape[0] - 1)
average_freq = 1 / (average_delta * .001)

print('Avergae collection delta: ' , average_delta * .001 , ' Seconds')
print('Avergae frequency of collection: ' , average_freq, ' Hertz')



"""
ax =
ay =
az =
"""
print(p1)
print('Finished Calculating!')
