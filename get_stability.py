import cv2
from sys import argv
from helper import *
from helper.measure import *

if __name__ == '__main__':
    videofilename = argv[1]
    NO_OF_BINS = 10
    # smoothing_radius = int(argv[2])

    cap = cv2.VideoCapture(videofilename)
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame_dim = gray.shape
    cap.release()
    #step 0 - get number of frames in video
    frame_count = getFrameCount(videofilename)
    #step 1 - get transformation from one frame to the next
    transform = getFrameToFrameTransform(videofilename, frame_count)
    #step2 - get the image trajectory from all the transformations
    image_trajectory = getImageTrajectory(transform)
    energyConc = getEnergyConcentrationFromFrameTwoNew(NO_OF_BINS, image_trajectory)
    print 'Stability',energyConc
