#step4
from data import trajectory, transform_param

def genSmoothTransform(frame_transforms, smooth_trajectories):
    print "Obtaining smooth transformation...",
    t = trajectory(0,0,0)
    new_transforms = []

    for i in range(len(frame_transforms)):
        ft = frame_transforms[i]
        st = smooth_trajectories[i]

        t2 = trajectory(t.x + ft.dx, t.y + ft.dy, t.a + ft.da)
        tp = transform_param(st.x - t2.x, st.y - t2.y, st.a - t2.a)
        tp2 = transform_param(ft.dx + tp.dx, ft.dy + tp.dy, ft.da + tp.da)

        new_transforms.append(tp2)
    print "Done"
    return new_transforms
