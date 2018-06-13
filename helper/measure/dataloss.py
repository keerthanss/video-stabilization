from __future__ import division
from PIL import Image
import numpy as np
import cv2
import sys

def findDataLoss(videofilename):
    cap = cv2.VideoCapture(videofilename)
    totalLoss=0.0
    f = 0.0
    while(True):
        ret, cur = cap.read()
        f+=1.0
        if ret is False:
            break
        cur_grey= cv2.cvtColor(cur,cv2.COLOR_BGR2GRAY)
        image_cur = np.asarray(cur_grey)
        black = np.count_nonzero(image_cur==0)
        black /=(image_cur.shape[0]*image_cur.shape[1])
        totalLoss += black

    cap.release()
    cv2.destroyAllWindows()
    return totalLoss/f

if __name__ == '__main__':
    videofilename = sys.argv[1]
    print findDataLoss(videofilename)
