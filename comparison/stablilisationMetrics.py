from PIL import Image
import numpy as np
import cv2


def findStabilityOfVideo(videofilename):
    cap = cv2.VideoCapture(videofilename)
    ret, prev_frame = cap.read()
    prev_grey = cv2.cvtColor(prev_frame,cv2.COLOR_BGR2GRAY)
    image_prev = np.asarray(prev_grey)
    frame_dim = prev_grey.shape

    stability=0
    f=0.0
    while(True):
        ret, cur = cap.read()
        f+=1.0
        if ret is False:
            break
        cur_grey= cv2.cvtColor(cur,cv2.COLOR_BGR2GRAY)
        image_cur = np.asarray(cur_grey)
        stability += sum(abs(np_img1-np_img2))/255.0 #normalize to 0-1
        image_prev = image_cur
    cap.release()
    cv2.destroyAllWindows()
    return stability/f #Average difference
