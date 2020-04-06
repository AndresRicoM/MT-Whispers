import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
from matplotlib import gridspec
import scipy.fftpack
from scipy import signal
from scipy.interpolate import interp1d


class file_select: #Class for selecting new file.
    def __init__(to_an):
        print('What data set do you want to use?')
        to_an.folder = input()
        print('What file do you want to analyze?')
        to_an.name = input()

def select():
    return file_select()

def open_new(ret_path):
    try:
        data = np.genfromtxt(ret_path, delimiter = ',', usecols=np.arange(0,36), invalid_raise=False)
        return data
    except:
        print('Unable to find specified file...')
        name = select()


if __name__ == "__main__":

    plt.style.use('dark_background') #Style Plots With Dark Theme

    print('Ready To Begin Importing Data...')

    name = select()
    #data_path = '/Users/AndresRico/Desktop/MT-Whispers/collected_data/processed/merged/' + name.folder + '/interpolated/' + name.name #Path for getting data

    try:
        print('Importing Data...')
        main_data = open_new('/Users/AndresRico/Desktop/MT-Whispers/collected_data/processed/merged/' + name.folder + '/interpolated/' + name.name)
        print('Data Was Succesfully Imported!')
    except:
        print('Unable to Import Data!')
        main_data = open_new('/Users/AndresRico/Desktop/MT-Whispers/collected_data/processed/merged/' + name.folder + '/interpolated/' + name.name)

    sensor_num = 3
    #main_data = main_data[0:1000, :]
    synth_time = np.linspace(0,main_data.shape[0], main_data.shape[0]) #Vector with synthetic time from data set.

    plt.plot(synth_time, main_data[:,sensor_num])
    plt.show()

    print('Data Imported!')

    #synth_time_fft = np.linspace(0,main_data.shape[0], main_data.shape[0])

    inter = interp1d(main_data[:,0].astype(int), main_data[:,sensor_num].astype(int), kind='linear') #Creates interpolation object.

    new_x = np.linspace(0 ,main_data.shape[0], main_data.shape[0]) #Adding Uniform X for Higher Frequency
    high_freq = inter(new_x)
    high_freq = scipy.signal.detrend(high_freq.astype(int))

    #plt.plot(new_x[:], high_freq[:], '-', synth_time ,main_data[:,sensor_num], '--')
    #plt.show()

    fig, (real, int) = plt.subplots(nrows=2)
    real.plot(synth_time ,main_data[:,sensor_num])
    int.plot(new_x[:], high_freq[:])
    plt.show()


    print(' /////////////////////// Data Set Information ///////////////////////')
    #Time Domain Variables.
    N = main_data[:,sensor_num].shape[0] # Number of Samples
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
    #p1 = scipy.fftpack.fft(high_freq.astype(int))

    print('Finished Creating FFTs!')
    #freq_vect = np.linspace(0.0, fmax, spect)
    #plt.plot(freq_vect, (1/spect)*np.abs(p1[:N//2]))
    #plt.show()

    NFFT = 1000  # the length of the windowing segments

    fig, (ax1, ax2) = plt.subplots(nrows=2)
    ax1.plot(synth_time, main_data[:,sensor_num])
    Pxx, freqs, bins, im = ax2.specgram(main_data[:,sensor_num], NFFT=NFFT, Fs=sampling_rate, noverlap=900)
    # The `specgram` method returns 4 objects. They are:
    # - Pxx: the periodogram
    # - freqs: the frequency vector
    # - bins: the centers of the time bins
    # - im: the matplotlib.image.AxesImage instance representing the data in the plot
    plt.show()

    gs = gridspec.GridSpec(5,1)
    fig = plt.figure()
    for sensors in range(1,6):
        ax = fig.add_subplot(gs[sensors-1])
        ax.specgram(main_data[:,sensors], NFFT=NFFT, Fs=sampling_rate, noverlap=900)

    #plt.specgram(main_data[:,sensor_num], NFFT=NFFT, Fs=sampling_rate, noverlap=900)
    plt.show()
