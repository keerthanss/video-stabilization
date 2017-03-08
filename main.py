import cv2
import numpy as np
from sys import argv
import extractFeatures as EF


feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

videofilename = argv[1]
cap = cv2.VideoCapture(videofilename)

features = []
while(1):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    points, descriptor = EF.getFeatures(gray, draw=True)
    triangleList = EF.delaunayTriangulation(gray, points, draw=True)

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
