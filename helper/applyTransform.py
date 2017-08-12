import math
import numpy as np
import cv2

def applyTransformation(videofilename, smooth_transform, frame_dim, max_frames, out_suffix = '_stabilized.avi'):
    print "Applying transformation...",
    cap = cv2.VideoCapture(videofilename)
    output_filename = videofilename.split('.')[0]+out_suffix

    cap.set(1, 0) #moving cap to start of the video
    # max_frames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)


    T = np.empty((2,3),np.float64)
    frame_width, frame_height = frame_dim
    aspect_ratio = float(frame_width) / frame_height
    HORIZONTAL_BORDER_CROP = 0#int((1-math.sqrt(0.7))/2*frame_width)
    vert_border = HORIZONTAL_BORDER_CROP * aspect_ratio
    vert_border = int(vert_border)
    print vert_border, frame_width, HORIZONTAL_BORDER_CROP, frame_height
    cropped_width = frame_width - 2*vert_border
    cropped_height = frame_height - 2*HORIZONTAL_BORDER_CROP
    cropped_dim = (cropped_width, cropped_height)

    fps = cap.get(cv2.CAP_PROP_FPS)
    codec = "MJPG"

    fourcc = cv2.VideoWriter_fourcc(*codec)
    writer = None
    (h,w) = (None, None)

    for k in xrange(max_frames-1):
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
        cur2 = cur2[vert_border:frame_width-vert_border, HORIZONTAL_BORDER_CROP:frame_height-HORIZONTAL_BORDER_CROP]

        if writer is None:
            (h,w) = cur2.shape[:2]
            writer = cv2.VideoWriter(output_filename, fourcc, fps, (w,h), True)

        writer.write(cur2)

        if(out_suffix == '_stabilized.avi'):
            cv2.imshow("Before stabilization", cur)
            cv2.imshow("After stabilization", cur2)
        #
        # canvas = np.zeros((rows,2*cols+10,3))
        # cur_grey = cv2.cvtColor(cur,cv2.COLOR_BGR2GRAY)
        # cur2_grey = cv2.cvtColor(cur2,cv2.COLOR_BGR2GRAY)
        # canvas[0:rows, 0:cols,0:3 ] = cur
        # canvas[0:rows, cols+10:2*cols+10, 0:3] = cur2
        # cv2.imshow("Before and after", canvas)
        cv2.waitKey(20)

    writer.write(cur2)

    cap.release()
    writer.release()
    cv2.destroyAllWindows()
    print "Done"
    return output_filename
