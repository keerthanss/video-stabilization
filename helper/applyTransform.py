import math
import numpy as np
import cv2

HORIZONTAL_BORDER_CROP = 20


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

def applyTransformation(videofilename, smooth_transform, frame_dim):
    max_frames = getFrameCount(videofilename)
    print "Applying transformation...",
    cap = cv2.VideoCapture(videofilename)
    output_filename = 'output.avi'

    cap.set(1, 0) #moving cap to start of the video
    # max_frames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)


    T = np.empty((2,3),np.float64)
    frame_width, frame_height = frame_dim
    aspect_ratio = frame_width / frame_height
    vert_border = HORIZONTAL_BORDER_CROP * aspect_ratio

    cropped_width = frame_width - 2*vert_border
    cropped_height = frame_height - 2*HORIZONTAL_BORDER_CROP
    cropped_dim = (cropped_width, cropped_height)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_filename,fourcc, 20.0, cropped_dim)

    for k in range(max_frames-1):
        ret, cur = cap.read()
        if not ret:
            break

        T[0,0] = math.cos(smooth_transform[k].da)
        T[0,1] = -1*math.sin(smooth_transform[k].da)
        T[1,0] = math.sin(smooth_transform[k].da)
        T[1,1] = math.cos(smooth_transform[k].da)

        T[0,2] = smooth_transform[k].dx
        T[1,2] = smooth_transform[k].dy

        rows, cols, color = cur.shape
        size = (cols, rows)
        cur2 = cv2.warpAffine(cur, T, size)
        #TODO: Fix this. An error is being thrown when cur2 is clipped but clipping is necessary.
        #cur2 = cur2[ vert_border : -vert_border , HORIZONTAL_BORDER_CROP : -HORIZONTAL_BORDER_CROP ]

        out.write(cur2)

        cv2.imshow("wtf", cur)
        cv2.imshow("yikes", cur2)

        canvas = np.zeros((rows,2*cols+10,3))
        #cur_grey = cv2.cvtColor(cur,cv2.COLOR_BGR2GRAY)
        #cur2_grey = cv2.cvtColor(cur2,cv2.COLOR_BGR2GRAY)
        canvas[0:rows, 0:cols,0:3 ] = cur
        canvas[0:rows, cols+10:2*cols+10, 0:3] = cur2
        #cv2.imshow("Before and after", canvas)
        cv2.waitKey(20)

    out.release()
    cap.release()
    cv2.destroyAllWindows()
    print "Done"
    return output_filename