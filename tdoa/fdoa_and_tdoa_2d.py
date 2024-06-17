import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

from signal_generator import Emitter, Receiver

c = 2.99792458e8
f0 = 1090e6

def main():
        emitter_pos = np.random.random(2) * 100
        emitter_vel = np.random.random(2) * 100
        emitter = Emitter(1090e6, emitter_pos, emitter_vel)

        receiver1_pos = np.random.random(2) * 100
        receiver1 = Receiver(20.90e6, 1e-6, receiver1_pos)

        receiver2_pos = np.random.random(2) * 100
        receiver2 = Receiver(20.90e6, 1e-6, receiver2_pos)

        receiver3_pos = np.random.random(2) * 100
        receiver3 = Receiver(20.90e6, 1e-6, receiver3_pos)

        message = '1010'

        symbols = emitter.generate_signal(message)
        signal1 = receiver1.sample_signal(symbols)
        signal2 = receiver2.sample_signal(symbols)
        signal3 = receiver3.sample_signal(symbols)

        # apply doppler
        signal1, f1 = receiver1.apply_doppler(signal1, emitter)
        signal2 ,f2 = receiver2.apply_doppler(signal2, emitter)
        signal3, f3 = receiver3.apply_doppler(signal3, emitter)

        # apply time shifts
        toa1 = receiver1.add_time_delay(signal1, emitter)
        toa2 = receiver2.add_time_delay(signal2, emitter)
        toa3 = receiver3.add_time_delay(signal3, emitter)

        # find solution
        x0 = np.concatenate((emitter_pos, emitter_vel)) + np.random.random(4) * 10
        x = least_squares(f, x0, args=(receiver1_pos, receiver2_pos, receiver3_pos, f1, f2, f3, toa1, toa2, toa3)).x

        print('Position error: ', np.linalg.norm(emitter_pos - x[:2]))
        print('Velocity error: ', np.linalg.norm(emitter_vel - x[2:]))
        print(x[2:])
        print(emitter_vel)

        # plotting
        x1 = receiver1_pos[0]
        y1 = receiver1_pos[1]
        x2 = receiver2_pos[0]
        y2 = receiver2_pos[1]
        x3 = receiver3_pos[0]
        y3 = receiver3_pos[1]

        xvals = np.linspace(-50, 150, 500)
        yvals = np.linspace(-50, 150, 500)
        X, Y = np.meshgrid(xvals, yvals)
        Z12 = dij(X, Y, emitter_vel[0], emitter_vel[1], receiver1_pos, receiver2_pos, f1, f2)
        Z13 = dij(X, Y, emitter_vel[0], emitter_vel[1], receiver1_pos, receiver3_pos, f1, f3)
        Z14 = tij(X, Y, receiver1_pos, receiver2_pos, toa1, toa2)
        Z15 = tij(X, Y, receiver1_pos, receiver3_pos, toa1, toa3)

        plt.figure()
        CS = plt.contour(X, Y, Z12, levels=[0], colors=('red',), linestyles=('dashed',), linewidths=(2,))
        CS = plt.contour(X, Y, Z13, levels=[0], colors=('red',), linestyles=('dashed',), linewidths=(2,))
        CS = plt.contour(X, Y, Z14, levels=[0], colors=('blue',), linestyles=('dashed',), linewidths=(2,))
        CS = plt.contour(X, Y, Z15, levels=[0], colors=('blue',), linestyles=('dashed',), linewidths=(2,))
        plt.plot(emitter_pos[0], emitter_pos[1], 'o', color = 'black', label = 'Emitter')
        plt.plot(x1, y1, 'o', color = 'blue', label = 'Receiver')
        plt.plot(x2, y2, 'o', color = 'blue')
        plt.plot(x3, y3, 'o', color = 'blue')
        plt.quiver(emitter_pos[0], emitter_pos[1], emitter_vel[0], emitter_vel[1], color = 'black', label = 'Emitter Velocity')
        plt.plot(x[0], x[1], marker='X', color = 'green', markersize = 10, label = 'Estimated Emitter Position')
        plt.quiver(x[0], x[1], x[2], x[3], color = 'green', width = 0.005, label = 'Estimated Emitter Velocity')
        plt.ylabel('y')
        plt.xlabel('x')
        plt.title('Lines of Constant FDOA/TDOA vs Emitter + Receiver Locations')
        plt.legend()
        plt.grid(True)
        plt.show()

def dij(x, y, vx, vy, X1, X2, F1, F2):
    x1, y1 = X1
    x2, y2 = X2
    f1, f2 = F1, F2
    return ((vx * (x - x1) + vy * (y - y1)) / np.sqrt((x - x1)**2 + (y - y1)**2) 
        - (vx * (x - x2) + vy * (y - y2)) / np.sqrt((x - x2)**2 + (y - y2)**2) 
        - c / f0 * (f1 - f2))

def tij(x, y, X1, X2, T1, T2):
    x1, y1 = X1
    x2, y2 = X2
    t1, t2 = T1, T2
    return np.sqrt((x - x1)**2 + (y - y1)**2) - np.sqrt((x - x2)**2 + (y - y2)**2) - (t1 - t2) * c
    
def f(z, X1, X2, X3, F1, F2, F3, toa1, toa2, toa3):
    x, y, vx, vy = z

    return [dij(x, y, vx, vy, X1, X2, F1, F2), dij(x,y, vx, vy, X1, X3, F1, F3), tij(x, y, X1, X2, toa1, toa2), tij(x, y, X1, X3, toa1, toa3)]

if __name__ == '__main__':
    main()