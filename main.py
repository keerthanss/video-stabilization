import cv2
import numpy as np
from sys import argv
#import gst
import extractFeatures as EF


feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

videofilename = argv[1]
cap = cv2.VideoCapture(videofilename)

#list of all active trajectories. Each trajectories is individually a list that starts as a single point in space&time
trajectories = []

ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame,cv2.COLOR_BGR2GRAY)
frame_number = 1
prev_keyPoints, prev_descriptor = EF.getFeatures(prev_gray, draw=True)
prev_points = EF.getPointsList(prev_keyPoints)
prev_triangleList = EF.delaunayTriangulation(prev_gray, prev_points, draw=True)

#Create new trajectories for all
for p in prev_points:
    trajectories.append([ (p[0],p[1],frame_number) ])

print len(trajectories)
retired_trajectories = []
while(1):
    ret, frame = cap.read()
    frame_number +=1
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    keyPoints, descriptor = EF.getFeatures(gray, draw=True)
    points = EF.getPointsList(keyPoints)

    matches = EF.matchFeatures(prev_descriptor, descriptor)
    triangleList = EF.delaunayTriangulation(gray, points, draw=True)

    for m in matches:
        train = m.trainIdx #corresponding to current frame
        query = m.queryIdx #corresponding to previous frame

        new_p = keyPoints[train]
        old_p = prev_keyPoints[query]

        #the two points that match
        new_p = (new_p.pt[0], new_p.pt[1],frame_number)
        old_p = (old_p.pt[0], old_p.pt[1],frame_number-1)

        #need to find old_p in trajectories and append new_p into it
        for i in xrange(len(trajectories)):
            if old_p == trajectories[i][-1]:
                trajectories[i].append( new_p )

                #TODO: Fix this. Error is thrown whenever trajectories intersect.
                try:
                    points.remove(new_p)
                except Exception as e:
                    #print e
                    pass

    #append those points which form the start of a new trajectory
    for p in points:
        trajectories.append([ (p[0],p[1],frame_number) ])

    print trajectories[0:2], len(trajectories)
    for t in trajectories:
        if t[-1][2] != frame_number:
            retired_trajectories.append(t)
            trajectories.remove(t)

    print len(retired_trajectories), len(trajectories)
    prev_frame, prev_keyPoints, prev_descriptor = frame, keyPoints, descriptor

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
