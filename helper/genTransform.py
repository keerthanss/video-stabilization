#step4
from data import trajectory, transform_param

def genSmoothTransform(frame_transforms, smooth_trajectories):
    t = trajectory(0,0,0)
    new_transforms = []

    for i in range(len(frame_transforms)):

        ft = frame_transforms[i] #current
        st = smooth_trajectories[i] #target
        t.x += ft.dx
        t.y += ft.dy
        t.a += ft.da
        tp = transform_param(st.x - t.x, st.y - t.y, st.a - t.a)
        tp2 = transform_param(ft.dx + tp.dx, ft.dy + tp.dy, ft.da + tp.da)

        new_transforms.append(tp2)

    return new_transforms
