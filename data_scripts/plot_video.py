import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import time
import numpy as np
from matplotlib import gridspec


plt.style.use('dark_background')

input_path = '/Users/AndresRico/Desktop/working/MT-Whispers/collected_data/processed/merged/wachusetts_030320/interpolated/910.csv'
data = np.genfromtxt(input_path, delimiter = ',', usecols=np.arange(0,36), invalid_raise=False)
print('Imported Data')

#23
"""
pressure_vals = []
max_pressure
for rows in range(0,data.shape[0]):
    pressure_vals.append( (data[rows,23] - np.min(data[:,23])  / (np.max(np.min(data[:,23]) - np.min(data[:,23])))))
"""

N = data[:,1].shape[0] # Number of Samples
T = data[data.shape[0]-1, 0] / 1000 # Frame Size
dT = T/N #Delta T
sampling_rate = 1/dT #Fs or Sampling Frequency

df = sampling_rate/N #Frequecy Resolution (frequency bin).
fmax = sampling_rate/2 #Bandwith or Max Freq
spect = N/2 #Spectral l

x_vals = []
y_vals = []
spect_vals = []
NFFT = 10

p1 = []
p2 = []
p3 = []
p4 = []
p5 = []

index = count()

gs = gridspec.GridSpec(5,1)
fig = plt.figure()

def animatescroll(i):
    if len(x_vals) > 150:
        x_vals.append(next(index))
        y_vals.append(data[next(index),23])
        x_vals.remove(x_vals[0])
        y_vals.remove(y_vals[0])
        plt.cla()
        plt.plot(x_vals, y_vals)
        plt.plot(x_vals, pressure_vals)
        plt.ylabel(r'Analog Voltage', size =12)
        plt.xlabel(r'Time', size =12)
        plt.title(r'Sensor Output', size =12)
    else:
        x_vals.append(next(index))
        y_vals.append(data[next(index),23])
        plt.cla()
        plt.plot(x_vals, y_vals)
        plt.ylabel(r'Analog Voltage', size =12)
        plt.xlabel(r'Time', size =12)
        plt.title(r'Sensor Output', size =12)

def animatestack(i):
    x_vals.append(next(index))
    y_vals.append(data[next(index),23])
    plt.cla()
    plt.plot(x_vals, y_vals)
    plt.plot(x_vals, x_vals)
    plt.ylabel(r'Analog Voltage', size =12)
    plt.xlabel(r'Time', size =12)
    plt.title(r'Sensor Output', size =12)

def piezoanimatescroll(i):
    if len(x_vals) > 50:
        x_vals.append(next(index))
        p1.append(data[next(index), 1])
        p2.append(data[next(index), 2])
        p3.append(data[next(index), 3])
        p4.append(data[next(index), 4])
        p5.append(data[next(index), 5])
        x_vals.remove(x_vals[0])
        p1.remove(p1[0])
        p2.remove(p2[0])
        p3.remove(p3[0])
        p4.remove(p4[0])
        p5.remove(p5[0])
        plt.cla()
        plt.plot(x_vals, p1, label = 'P1')
        plt.plot(x_vals, p2, label = 'P2')
        plt.plot(x_vals, p3, label = 'P3')
        plt.plot(x_vals, p4, label = 'P4')
        plt.plot(x_vals, p5, label = 'P5')
        plt.legend(loc = 'upper right')
        plt.ylabel(r'Analog Voltage', size =12)
        plt.xlabel(r'Time', size =12)
        plt.title(r'Sensor Output', size =12)
    else:
        x_vals.append(next(index))
        p1.append(data[next(index), 1])
        p2.append(data[next(index), 2])
        p3.append(data[next(index), 3])
        p4.append(data[next(index), 4])
        p5.append(data[next(index), 5])
        plt.cla()
        plt.plot(x_vals, p1, label = 'P1')
        plt.plot(x_vals, p2, label = 'P2')
        plt.plot(x_vals, p3, label = 'P3')
        plt.plot(x_vals, p4, label = 'P4')
        plt.plot(x_vals, p5, label = 'P5')
        plt.legend(loc = 'upper right')
        plt.ylabel(r'Analog Voltage', size =12)
        plt.xlabel(r'Time', size =12)
        plt.title(r'Sensor Output', size =12)


def piezoanimatestack(i):
    x_vals.append(next(index))
    p1.append(data[next(index), 1])
    p2.append(data[next(index), 2])
    p3.append(data[next(index), 3])
    p4.append(data[next(index), 4])
    p5.append(data[next(index), 5])
    plt.cla()
    plt.plot(x_vals, p1, label = 'P1')
    plt.plot(x_vals, p2, label = 'P2')
    plt.plot(x_vals, p3, label = 'P3')
    plt.plot(x_vals, p4, label = 'P4')
    plt.plot(x_vals, p5, label = 'P5')
    plt.legend(loc = 'upper right')
    plt.ylabel(r'Analog Voltage', size =12)
    plt.xlabel(r'Time', size =12)
    plt.title(r'Sensor Output', size =12)

def animategrid(i):
    x_vals.append(next(index))
    y_vals.append(data[next(index),23])

    #plt.cla()
    ax = fig.add_subplot(gs[0])
    ax.plot(x_vals,y_vals)
    #ax.set_xlabel(r'Time', size =15)
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    #ax.set_yticklabels([])
    ax.set_xticklabels([])

    #plt.cla()
    ax = fig.add_subplot(gs[1])
    ax.plot(x_vals,y_vals)
    #ax.set_xlabel(r'Time', size =15)
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    #ax.set_yticklabels([])
    ax.set_xticklabels([])

    #plt.cla()
    ax = fig.add_subplot(gs[2])
    ax.plot(x_vals,y_vals)
    #ax.set_xlabel(r'Time', size =15)
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    #ax.set_yticklabels([])
    ax.set_xticklabels([])

    #plt.cla()
    ax = fig.add_subplot(gs[3])
    ax.plot(x_vals,y_vals)
    #ax.set_xlabel(r'Time', size =15)
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    #ax.set_yticklabels([])
    ax.set_xticklabels([])

    #plt.cla()
    ax = fig.add_subplot(gs[4])
    ax.plot(x_vals,y_vals)
    #ax.set_xlabel(r'Time', size =15)
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    #ax.set_yticklabels([])
    ax.set_xticklabels([])


def animatespect(i):
    x_vals.append(next(index))
    spect_vals.append(data[next(index),1])
    plt.cla()
    plt.specgram(spect_vals, NFFT=NFFT, Fs=sampling_rate, noverlap=9)
    plt.ylabel(r'Frequency (HZ)', size =12)
    plt.xlabel(r'Time', size =12)
    plt.title(r'Feedback Spectogram', size =12)

ani = FuncAnimation(plt.gcf(), animatespect, interval=10)

plt.plot(x_vals, y_vals)
plt.tight_layout()
plt.show()
