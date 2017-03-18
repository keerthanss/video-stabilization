#step 2 
from data import trajectory, transform_param

def getTrajectory(frame_transforms):
    t = trajectory(0,0,0)
    all_frame_trajectory = [] #trajectory at all frames

    for ft in frame_transforms:
        t2 = trajectory(t.x + ft.dx, t.y + ft.dy, t.a + ft.da)
        all_frame_trajectory.append(t2)
        t = t2

    return all_frame_trajectory
