#step 2
from data import trajectory, transform_param

def getImageTrajectory(frame_transforms,output_filename='frame_to_frame_changes.txt'):
    print "Getting trajectories...",
    fOut = open(output_filename,'w')
    t = trajectory(0,0,0)
    image_trajectory = [] #trajectory at all frames

    for ft in frame_transforms:
        t2 = trajectory(t.x + ft.dx, t.y + ft.dy, t.a + ft.da)
        image_trajectory.append(t2)
        t = t2
        fOut.write(str(t.x)+'\t'+str(t.y)+'\t'+str(t.a)+'\n')

    print "Done"
    return image_trajectory
