import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
from matplotlib import gridspec
import scipy.fftpack
from scipy import signal
from scipy.interpolate import interp1d

print('Importing Data...')

data_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/processed/merged/fft_250320/interpolated/'
#lm_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/raw/Killington_250120/LM'

data_file = '884.csv'#'910.csv'#'301.csv'#'837.csv'

window = 300

main_data = np.genfromtxt(data_path + data_file, delimiter = ',', usecols=np.arange(0,36), invalid_raise=False)
main_data = main_data[:window,:]
print('Data Imported!')

synth_time = np.linspace(0,main_data.shape[0], main_data.shape[0])

inter = interp1d(main_data[:,0].astype(int), main_data[:,1].astype(int), kind='cubic')
new_x = np.linspace(0 ,main_data.shape[0], main_data.shape[0] * 2)
high_freq = inter(new_x)

plt.plot(new_x[:300], high_freq[:300], '-', main_data[:300,0] ,main_data[:300,1], '--')
plt.show()

print(' /////////////////////// Data Set Information ///////////////////////')

#Time Domain Variables.
N = high_freq.shape[0] # Number of Samples
T = main_data[main_data.shape[0]-1, 0] / 1000 # Frame Size
dT = T/N #Delta T
sampling_rate = 1/dT #Fs or Sampling Frequency

#Frequency Domain Variables.
df = sampling_rate/N #Frequecy Resolution (frequency bin).
fmax = sampling_rate/2 #Bandwith or Max Freq
spect = N/2 #Spectral lines.

print('Number of Saples (N): ', N)
print('Frame Size (Total Collection Time) (T): ', T, ' seconds')
print('dT: ', dT)
print('Sampling rate (freq): ', sampling_rate, ' Hz')
print('Frequency resolution: ', df, ' Hz')

print(' /////////////////////////////////////////////////////////////////////')

print('Calculating FFT for Piezo and Accel Data...')

"""
p1 = np.fft.rfft(main_data[:,1])
p2 = np.fft.rfft(main_data[:,2])
p3 = np.fft.rfft(main_data[:,3])
p4 = np.fft.rfft(main_data[:,4])
p5 = np.fft.rfft(main_data[:,5])
"""
#test = np.linspace(0,10,10)
#print(scipy.fftpack.fft(test))
p1 = scipy.signal.detrend(high_freq.astype(int))
p1 = scipy.fftpack.fft(high_freq.astype(int))

print('Finished Creating FFTs!')

freq_vect = np.linspace(0.0, fmax, spect)

#plt.plot(freq_vect, (1/spect)*np.abs(p1[:N//2]))
plt.plot(freq_vect, (1/spect)*np.abs(p1[:N//2]))

#print((1/spect)*np.abs(p1[:N//2]))
#plt.plot(freq_vect, (1/spect)*np.abs(p1))

plt.show()
