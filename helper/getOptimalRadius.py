#step 2.5
import cv2
from sys import argv
from averageWindow import *
from genTransform import *
from applyTransform import *
from measure import getEnergyConcentrationFromFrameTwoNew, findDataLoss
import matplotlib.pyplot as plt

def getRadiusValue(unsmoothedTrajectory, transform, videofilename, frame_dim, frame_count):
    THRESHOLD_DATA_LOSS = 0.1
    RADIUS_INCREMENT = 2
    NO_OF_BINS = 10
    EPSILON = 0.01

    datapoints = []
    smoothingRadius = 1
    dataLoss = 0
    while ( dataLoss < THRESHOLD_DATA_LOSS and smoothingRadius < 40):
    # for i in range(20):
        smooth_trajectory = getSmoothedTrajectory(unsmoothedTrajectory,smoothingRadius)
        energyConc = getEnergyConcentrationFromFrameTwoNew(NO_OF_BINS, smooth_trajectory)
        smooth_transform = genSmoothTransform(transform, smooth_trajectory)
        output_filename = applyTransformation(videofilename, smooth_transform, frame_dim, frame_count, '-intermediate.avi')
        dataLoss = findDataLoss(output_filename)

        datapoints.append((smoothingRadius,dataLoss,energyConc))
        smoothingRadius += RADIUS_INCREMENT

    for dp in datapoints:
        print dp[0], dp[1], dp[-1]

    x_axis = [sr[0] for sr in datapoints]
    print x_axis
    dl = [sr[1] for sr in datapoints]
    ec = [sr[2] for sr in datapoints]
    # ratio_before = [e/d for e,d in zip(ec,dl)]
    # rb_min = min(ratio_before)
    # rb_max = max(ratio_before)
    # ratio_before = [(elem-rb_min)/(rb_max-rb_min) for elem in ratio_before]
    dl_min = min(dl)
    dl_max = max(dl)
    dl = [(elem-dl_min)/(dl_max-dl_min) for elem in dl]
    ec_min = min(ec)
    ec_max = max(ec)
    ec = [(elem-ec_min)/(ec_max-ec_min) for elem in ec]
    ec_root = [(elem+EPSILON)**0.5 for elem in ec]
    temp = dl[0]
    dl[0] = 1
    dl_root = [(1-elem+EPSILON)**0.5 for elem in dl]

    prod = [d*e for d,e in zip(dl_root,ec_root)]
    # prod = [math.exp( -( ( ( (d+e)/2 - 0.5 )* 3/0.5)**2 ) ) for d,e in zip(dl,ec)]
    print 'MAX index= ', prod.index(max(prod))
    print 'Max goodness at smoothing radius of', 1 + RADIUS_INCREMENT*prod.index(max(prod))
    print 'Stability value at that smoothing radius =', datapoints[prod.index(max(prod))][2]
    print 'Stability of original video =', getEnergyConcentrationFromFrameTwoNew(NO_OF_BINS, unsmoothedTrajectory)
    # ratio_after = [e/d for e,d in zip(ec,dl)]
    # ra_min = min(ratio_after)
    # ra_max = max(ratio_after)
    # ratio_after = [(elem-ra_min)/(ra_max-ra_min) for elem in ratio_after]
    dl[0] = temp
    plt.plot(x_axis[1:-2],dl[1:-2],'r',label='Data loss (normalized)')
    plt.plot(x_axis[1:-2],ec[1:-2],'g',label='Stability (normalized)')
    # plt.plot(x_axis,ec_root,'g',label='log(ec)')
    # plt.plot(x_axis,dl_root,'y',label='dl_root')
    plt.plot(x_axis[1:-2],prod[1:-2],'b',label='Goodness')
    plt.xlabel('Smoothing radius')
    plt.legend()
    plt.show()
    return datapoints[prod.index(max(prod))][0]
    # find correct point from datapoints
    # return found value
