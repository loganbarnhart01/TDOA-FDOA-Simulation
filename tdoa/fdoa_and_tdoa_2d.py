import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

from signal_generator import Emitter, Receiver, channel

c = 2.99792458e8
f0 = 1090e6

def main():
        emitter_pos = np.random.random(2) * 100
        emitter_vel = np.random.random(2) * 100
        emitter = Emitter(1090e6, 1e8, 1e8, emitter_pos, emitter_vel)

        receiver1_pos = np.random.random(2) * 100
        receiver1 = Receiver(1090e6, 2180e6, receiver1_pos)

        receiver2_pos = np.random.random(2) * 100
        receiver2 = Receiver(1090e6, 2180e6, receiver2_pos)

        receiver3_pos = np.random.random(2) * 100
        receiver3 = Receiver(1090e6, 2180e6, receiver3_pos)

        message = '1010'

        signal, times = emitter.generate_signal(message)

        _, times1, f1 = channel(signal, times, emitter, receiver1)
        _, times2, f2 = channel(signal, times, emitter, receiver2)
        _, times3, f3 = channel(signal, times, emitter, receiver3)

        toa1 = times1[0]
        toa2 = times2[0]
        toa3 = times3[0]

        f1 = 1090e6 - f1
        f2 = 1090e6 - f2
        f3 = 1090e6 - f3

        x1 = receiver1_pos[0]
        y1 = receiver1_pos[1]
        x2 = receiver2_pos[0]
        y2 = receiver2_pos[1]
        x3 = receiver3_pos[0]
        y3 = receiver3_pos[1]

        x0 = np.random.random(4) * 100
        x = fsolve(f, x0, args=(receiver1_pos, receiver2_pos, receiver3_pos, f1, f2, f3, toa1, toa2, toa3))

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
        plt.quiver(emitter_pos[0], emitter_pos[1], emitter_vel[0], emitter_vel[1], color = 'black', alpha = 0.75, label = 'Emitter Velocity', scale=1, scale_units='xy', angles='xy', pivot='tail', width=0.009)
        plt.plot(x[0], x[1], marker='X', color = 'blue', markersize = 10, label = 'Estimated Emitter Position')
        plt.quiver(x[0], x[1], x[2], x[3], color = 'green', label = 'Estimated Emitter Velocity')
        plt.ylabel('y')
        plt.xlabel('x')
        plt.title('Lines of Constant FDOA/TDOA vs Emitter + Receiver Locations')
        plt.legend()
        plt.grid(True)
        plt.show()
        print(f"Actual emitter velocity: {emitter_vel} ")
        print(f"Estimated emitter velocity: {x[2:]}")
        
        
        # Test how often we get the correct solution
        num_tests = 10000
        pos_errors = np.zeros(num_tests)
        vel_errors = np.zeros(num_tests)
        for i in range(num_tests):
            emitter_pos = np.random.random(2) * 100
            emitter_vel = np.random.random(2) * 100
            emitter_dir = emitter_vel / np.linalg.norm(emitter_vel) * 30
            emitter = Emitter(1090e6, 1e8, 1e8, emitter_pos, emitter_vel)

            receiver1_pos = np.random.random(2) * 100
            receiver1 = Receiver(1090e6, 2180e6, receiver1_pos)

            receiver2_pos = np.random.random(2) * 100
            receiver2 = Receiver(1090e6, 2180e6, receiver2_pos)

            receiver3_pos = np.random.random(2) * 100
            receiver3 = Receiver(1090e6, 2180e6, receiver3_pos)

            message = '1010'

            signal, times = emitter.generate_signal(message)

            _, times1, f1 = channel(signal, times, emitter, receiver1)
            _, times2, f2 = channel(signal, times, emitter, receiver2)
            _, times3, f3 = channel(signal, times, emitter, receiver3)

            toa1 = times1[0]
            toa2 = times2[0]
            toa3 = times3[0]

            f1 = 1090e6 - f1
            f2 = 1090e6 - f2
            f3 = 1090e6 - f3

            x1 = receiver1_pos[0]
            y1 = receiver1_pos[1]
            x2 = receiver2_pos[0]
            y2 = receiver2_pos[1]
            x3 = receiver3_pos[0]
            y3 = receiver3_pos[1]

            # x0 = np.concatenate((emitter.position, emitter_vel)) + np.random.random(4) * 10
            x0 = np.random.random(4) * 100
            x = fsolve(f, x0, args=(receiver1_pos, receiver2_pos, receiver3_pos, f1, f2, f3, toa1, toa2, toa3))
        
            pos_errors[i] = np.linalg.norm(emitter_pos - x[:2])
            vel_errors[i] = np.linalg.norm(emitter_vel - x[2:])
        
        print(f'Average Position Error: {np.mean(pos_errors):.3f}')
        print(f'Average Velocity Error: {np.mean(vel_errors):.3f}')
        print(f'Percent correct pos convergence: {np.sum(pos_errors < 1e-3) / num_tests * 100:.3f}%')
        print(f'Percent correct vel convergence: {np.sum(vel_errors < 1e-3) / num_tests * 100:.3f}%')

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