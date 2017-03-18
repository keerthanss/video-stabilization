import numpy as np

def getFrameToFrameTransforms(cap,prev_grey,out_transform):
    prev_to_cur_transform = []
    k = 1
    max_frames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    while(true):
        last_T = np.zeros(shape=prev_grey.shape())
        ret, cur = cap.read()
        cur_grey = cv2.cvtColor(cur,cv2.COLOR_BGR2GRAY)

        prev_corner = [], cur_corner = []
        prev_corner_2 = [], cur_corner_2 = []
        status = []
        err = []


        cv2.calcOpticalFlowPyrLK(prev_grey,cur_grey,prev_corner,cur_corner,status,err)

        for in in len(status):
            if status[i]:
                prev_corner_2.append(prev_corner[i])
                cur_corner_2.append(cur_corner[i])

        T = np.zeros(shape=prev_grey.shape())
        T = cv2.estimateRigidTransform(prev_corner_2,cur_corner_2,False)

        if np.count_nonzero(T):
            T = last_T

        last_T = T
        dx = T[0,2]
        dy = T[1,2]
        da = atan2(T[1,0], T[0,0])

        prev_to_cur_transform.append(transform_param(dx,dy,da))

        prev = cur
        prev_grey = cur_grey

        out_transform.write("Frame: "+str(k)+"/"str(max_frames)+" - good optical flow: "+len(prev_corner_2)+"\n")
