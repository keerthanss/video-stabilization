import matplotlib.pyplot as plt

def plotGraph(smoothing_radius):
    fIn = []

    fIn.append(open('frame_to_frame_changes.txt','r'))
    fIn.append(open('smooth_changes.txt','r'))

    for i in range(2):
        x = []; y = []; a = []; frame_no = []; count = 1
        for line in fIn[i]:
            frame_no.append(count)
            count += 1
            x.append(float(line.split()[0]))
            y.append(float(line.split()[1]))
            # a.append(1000*float(line.split()[2]))

        # plt.figure(i)
        if i==0:
            plt.figure('Original video')
            plt.title('Original video')
        else:
            plt.figure('Smoothed video')
            plt.title('Smoothing radius = '+ str(smoothing_radius))
        plt.plot(frame_no,x,'r--',label='X coordinate')
        plt.plot(frame_no,y,'b',label='Y coordinate')
        # plt.plot(frame_no,a,'g',label='Angle w.r.t horizontal')
        plt.xlabel('Frame number')
        plt.ylabel('Movement')
        plt.legend()
    plt.show()
