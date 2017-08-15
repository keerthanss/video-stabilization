import cv2
from sys import argv
from helper import *
from helper.measure import *

if __name__ == '__main__':
    videofilename = argv[1]
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
    #step2.5 - get optimal smoothing radius
    smoothing_radius = getRadiusValue(image_trajectory, transform, videofilename, frame_dim, frame_count)
    #step3 - smoothen out the trajectory
    smooth_trajectory = getSmoothedTrajectory(image_trajectory, smoothing_radius)
    #step4 - obtain corresponding transformation
    smooth_transform = genSmoothTransform(transform, smooth_trajectory)
    #step5 - apply transformations and save video
    output_filename = applyTransformation(videofilename, smooth_transform, frame_dim, frame_count)

    print 'Distortion in original video:', findDistortionOfVideo(videofilename)
    print 'Distortion in stabilized video:', findDistortionOfVideo(output_filename)

    # plotGraph(smoothing_radius)
