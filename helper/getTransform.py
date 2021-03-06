import numpy as np
import cv2
import math
from data import transform_param

def getFrameCount(videofilename):
    #print "Getting frame count"
    cap = cv2.VideoCapture(videofilename)
    frame_count= 0
    while(True):
        ret, frame = cap.read()
        if ret is True:
            frame_count+=1
        else:
            break
        # cv2.imshow('counting', frame)
        # cv2.waitKey(20)
    #print "Frame count = " + str(frame_count)
    cap.release()
    return frame_count

def getFrameToFrameTransform(videofilename, max_frames):
    print "Getting frame to frame transform...",

    cap = cv2.VideoCapture(videofilename)

    ret, prev_frame = cap.read()
    prev_grey = cv2.cvtColor(prev_frame,cv2.COLOR_BGR2GRAY)

    prev_to_cur_transform = []
    k = 1
    # max_frames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

    f = 0
    last_T = []
    while(True):
        last_T = np.zeros(shape=prev_grey.shape)
        ret, cur = cap.read()
        if ret is False:
            break
        f+=1
        cur_grey = cv2.cvtColor(cur,cv2.COLOR_BGR2GRAY)



        prev_corner = []
        cur_corner = []
        prev_corner_2 = []
        cur_corner_2 = []
        status = []
        err = []

        prev_corner = cv2.goodFeaturesToTrack(prev_grey, 200, 0.01, 30)
        cur_corner, status, err = cv2.calcOpticalFlowPyrLK(prev_grey,cur_grey,prev_corner,None)
        status = [i for [i] in status]

        for i in xrange(len(status)):
            if status[i]:
                prev_corner_2.append(prev_corner[i])
                cur_corner_2.append(cur_corner[i])


        prev_corner_2 = np.asarray(prev_corner_2)
        cur_corner_2 = np.asarray(cur_corner_2)

        # T = np.zeros(shape=prev_grey.shape)
        T = cv2.estimateRigidTransform(prev_corner_2,cur_corner_2,False)
        if T is None:
            T = last_T

        last_T = T
        dx = T[0,2]
        dy = T[1,2]
        da = math.atan2(T[1,0], T[0,0])

        prev_to_cur_transform.append(transform_param(dx,dy,da))

        prev = cur
        prev_grey = cur_grey

        k+=1

    cap.release()
    cv2.destroyAllWindows()
    print "Done"
    return prev_to_cur_transform
