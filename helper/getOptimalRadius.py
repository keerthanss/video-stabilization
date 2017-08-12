#step 2.5
import cv2
from sys import argv
from averageWindow import *
from genTransform import *
from applyTransform import *
from dataloss import *
from stab_measure_new import *
import matplotlib.pyplot as plt

def getRadiusValue(unsmoothedTrajectory, transform, videofilename, frame_dim, frame_count):
    THRESHOLD_DATA_LOSS = 0.1
    RADIUS_INCREMENT = 2
    NO_OF_BINS = 6

    datapoints = []
    smoothingRadius = 1
    dataLoss = 0
    #while ( dataLoss < THRESHOLD_DATA_LOSS ):
    for i in range(20):
        #step 3
        smooth_trajectory = getSmoothedTrajectory(unsmoothedTrajectory,smoothingRadius)

        energyConc = getEnergyConcentrationFromFrameTwoNew(NO_OF_BINS, smooth_trajectory)

        #step 4
        smooth_transform = genSmoothTransform(transform, smooth_trajectory)

        #step 5
        output_filename = applyTransformation(videofilename, smooth_transform, frame_dim, frame_count, '-intermediate.avi')

        #DONE  Apply smoothed trajectory to get smoothed videofile
        dataLoss = findDataLoss(output_filename)

        # Use the stability metric to get stability

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
    ec_root = [elem**0.5 for elem in ec]
    temp = dl[0]
    dl[0] = 1
    dl_root = [(1-elem)**0.5 for elem in dl]

    prod = [d*e for d,e in zip(dl_root,ec_root)]
    # prod = [math.exp( -( ( ( (d+e)/2 - 0.5 )* 3/0.5)**2 ) ) for d,e in zip(dl,ec)]
    print 'MAX index= ', prod.index(max(prod))
    # ratio_after = [e/d for e,d in zip(ec,dl)]
    # ra_min = min(ratio_after)
    # ra_max = max(ratio_after)
    # ratio_after = [(elem-ra_min)/(ra_max-ra_min) for elem in ratio_after]
    dl[0] = temp
    plt.plot(x_axis,dl,'r',label='dataloss')
    plt.plot(x_axis,ec,'b',label='energyconc')
    # plt.plot(x_axis,ec_root,'g',label='log(ec)')
    # plt.plot(x_axis,dl_root,'y',label='dl_root')
    plt.plot(x_axis,prod,'c',label='prod')
    plt.xlabel('Smoothing radius')
    plt.legend()
    plt.show()
    return datapoints[-1][0]
    # find correct point from datapoints
    # return found value
