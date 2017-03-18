#step 2
from data import trajectory, transform_param

def getImageTrajectory(frame_transforms):
    print "Getting trajectories...",
    t = trajectory(0,0,0)
    image_trajectory = [] #trajectory at all frames

    for ft in frame_transforms:
        t2 = trajectory(t.x + ft.dx, t.y + ft.dy, t.a + ft.da)
        image_trajectory.append(t2)
        t = t2

    print "Done"
    return image_trajectory
