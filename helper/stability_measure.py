from __future__ import division
import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt
from sys import argv

no_of_bins = int(argv[1])
orig_video = argv[2].rsplit('.',1)[0]

fIn = []

fIn.append(open(orig_video+'_trajectory.txt','r'))
fIn.append(open(orig_video+'_stabilized_trajectory.txt','r'))
fIn.append(open(orig_video+'_youtube_trajectory.txt','r'))

def getFreqRepresentation():
    x = [[],[],[]]; y = [[],[],[]]; a = [[],[],[]]
    xf = [[],[],[]]; yf = [[],[],[]]; af = [[],[],[]];
    for file in range(3):
        for line in fIn[file]:
            line = line.split()
            x[file].append(float(line[0]))
            y[file].append(float(line[1]))
            a[file].append(float(line[2]))

        xf[file] = fft(x[file])
        yf[file] = fft(y[file])
        af[file] = fft(a[file])

        # if file==0:
        #     plt.figure('Original video')
        #     plt.title('Original video')
        # else:
        #     plt.figure('Smoothed video')
        #     plt.title('Smoothed video')

        # plt.plot(frame,magxf[file],'r',label='X coordinate')
        # plt.plot(frame,magyf,'b',label='Y coordinate')
    frame = range(1,len(xf[0])+1)
    magxf = np.absolute(xf)
    magyf = np.absolute(yf)
    magaf = np.absolute(af)
    # print type(magxf[0])

    # plt.figure('Original video')
    plt.plot(frame[1:],list(magxf[0][1:]),'r:',label='Original')
    # plt.legend()
    # plt.figure('Stabilized video')
    plt.plot(frame[1:],list(magxf[1][1:]),'b',label='Discussed method')
    plt.plot(frame[1:],list(magxf[2][1:]),'g--',label='YouTube')
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude of signal')
    plt.legend()
    plt.show()

    # plt.show()

    return (magxf,magyf,magaf)

def getEnergyConcentrationFromFrameTwo(no_of_bins):
    (magxf,magyf,magaf) = getFreqRepresentation()

    energyX = np.array(magxf)**2
    energyY = np.array(magyf)**2
    energyA = np.array(magaf)**2

    print type(energyY)
    print type(energyY[0])

    for file in range(3):
        energyEnd = (sum(energyY[file][1:1+no_of_bins]) + sum(energyY[file][1:1+no_of_bins]))/2

        energyTotal = (sum(energyY[file][1:]) + sum(energyY[file][1:]))/2

        if file == 0:
            print "Original video:"
        elif file == 1:
            print "Our method:"
        else:
            print "YouTube:"
        # print "Percentage of energy in the first",no_of_bins,"bins =",energyEnd/energyTotal*100
        print "energyTotal =", energyTotal
        print "energyEnd =", energyEnd
        print "ratio =", 2*energyEnd/energyTotal


getEnergyConcentrationFromFrameTwo(no_of_bins)
