import cv2
import numpy as np

def getFeatures(img, draw=False):
    # # Initiate STAR detector
    # orb = cv2.ORB_create()
    #
    # # find the keypoints with ORB
    # kp = orb.detect(img,None)
    # print kp
    # # compute the descriptors with ORB
    # kp, des = orb.compute(img, kp)
    #
    # # draw only keypoints location,not size and orientation
    # img2 = cv2.drawKeypoints(img,kp,img,color=(0,255,0), flags=0)

    corners = cv2.goodFeaturesToTrack(img,100,0.01,10)
    corners = np.int0(corners)
    points = []
    for i in corners:
        x,y = i.ravel()
        points.append((x,y))

    if draw:
        point_color = (255,0,0)
        for p in points:
            cv2.circle( img, p, 2, point_color, -1 )

    return points

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
