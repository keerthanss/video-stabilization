import cv2
import numpy as np

def getFeatures(img, draw=False):
    # Initiate STAR detector
    orb = cv2.ORB_create(nfeatures=500)

    # find the keypoints with ORB
    keyPoints = orb.detect(img,None)

    # compute the descriptors with ORB
    keyPoints, des = orb.compute(img, keyPoints)

    return (keyPoints, des)

def getPointsList(keyPoints):
    pointsList = []
    for point in keyPoints:
        x = point.pt[0]
        y = point.pt[1]
        pointsList.append( (x,y) )
    return pointsList

def delaunayTriangulation(img, points, draw=False):
    size = img.shape
    r = (0, 0, size[1], size[0])
    subdiv  = cv2.Subdiv2D(r)

    for p in points:
        subdiv.insert(p)

    triangleList = subdiv.getTriangleList()

    if draw:
        # Check if a point is inside a rectangle
        def rect_contains(rect, point) :
            if point[0] < rect[0] :
                return False
            elif point[1] < rect[1] :
                return False
            elif point[0] > rect[2] :
                return False
            elif point[1] > rect[3] :
                return False
            return True

        delaunay_color = (0,0, 255)

        for t in triangleList :

            pt1 = (t[0], t[1])
            pt2 = (t[2], t[3])
            pt3 = (t[4], t[5])

            if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3) :

                cv2.line(img, pt1, pt2, delaunay_color, 1)
                cv2.line(img, pt2, pt3, delaunay_color, 1)
                cv2.line(img, pt3, pt1, delaunay_color, 1)

    return triangleList

def matchFeatures(old_des,new_des):
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # Match descriptors.
    matches = bf.match(old_des,new_des)
    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)
    return matches
