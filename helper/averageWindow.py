#step 3
from data import trajectory, transform_param
def getSmoothedTrajectory(unsmoothed_trajectory,smoothing_radius):
    smoothed_trajectory = []
    for i in range(len(unsmoothed_trajectory)):
        count = 0
        sum_t = Trajectory(0,0,0)
        for j in range (-1*smoothing_radius,smoothing_radius+1):
            if i+j>0 and i+j<len(unsmoothed_trajectory):
                sum_t = trajectory(
                                sum_t.x + unsmoothed_trajectory[i+j].x, 
                                sum_t.y+unsmoothed_trajectory[i+j].y,
                                sum_t.a + unsmoothed_trajectory[i+j].a
                                )
                count +=1
        average_point = Trajectory(sum_t.x/count,sum_t.y/count,sum_t.a/count)

        smoothed_trajectory.append(average_point)
    return smoothed_trajectory
