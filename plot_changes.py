import matplotlib.pyplot as plt

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
        a.append(float(line.split()[2]))

    plt.figure(i)
    plt.plot(frame_no,x,'r')
    plt.plot(frame_no,y,'b')
    plt.plot(frame_no,a,'g')
plt.show()
