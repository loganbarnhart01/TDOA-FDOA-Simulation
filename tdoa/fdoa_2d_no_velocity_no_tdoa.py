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

        receiver4_pos = np.random.random(2) * 100
        receiver4 = Receiver(1090e6, 2180e6, receiver4_pos)

        receiver5_pos = np.random.random(2) * 100
        receiver5 = Receiver(1090e6, 2180e6, receiver5_pos)

        message = '1010'

        signal, times = emitter.generate_signal(message)

        _, _, f1 = channel(signal, times, emitter, receiver1)
        _, _, f2 = channel(signal, times, emitter, receiver2)
        _, _, f3 = channel(signal, times, emitter, receiver3)
        _, _, f4 = channel(signal, times, emitter, receiver4)
        _, _, f5 = channel(signal, times, emitter, receiver5)

        f1 = 1090e6 - f1
        f2 = 1090e6 - f2
        f3 = 1090e6 - f3
        f4 = 1090e6 - f4
        f5 = 1090e6 - f5

        
        # x0 = np.concatenate((emitter_pos, emitter_vel)) + np.random.random(4)
        x0 = np.random.random(4) * 100
        print(x0)
        x = fsolve(f, x0, args=(receiver1_pos, receiver2_pos, receiver3_pos, receiver4_pos, receiver5_pos, f1, f2, f3, f4, f5))  
        print(f'Emitter position: {emitter_pos} Emitter velocity: {emitter_vel}')
        print(f'Estimated position: {x[:2]} Estimated velocity: {x[2:]}')
        print(f'Error: {np.linalg.norm(emitter_pos - x[:2])}')    

        plt.plot(receiver1_pos[0], receiver1_pos[1], 'bo')
        plt.plot(receiver2_pos[0], receiver2_pos[1], 'bo')
        plt.plot(receiver3_pos[0], receiver3_pos[1], 'bo')
        plt.plot(receiver4_pos[0], receiver4_pos[1], 'bo')
        plt.plot(receiver5_pos[0], receiver5_pos[1], 'bo', label='Receivers') 
        plt.plot(emitter_pos[0], emitter_pos[1], 'ro', label='Emitter')
        plt.quiver(emitter_pos[0], emitter_pos[1], emitter_vel[0], emitter_vel[1], label = 'Emitter velocity')
        plt.plot(x[0], x[1], 'gX', label='Estimated position')
        plt.quiver(x[0], x[1], x[2], x[3], alpha = 0.5, label = 'Estimated velocity')
        plt.title(f"Emitter position error: {np.linalg.norm(emitter_pos - x[:2]):.3f}\nEmiiter velocity error: {np.linalg.norm(emitter_vel - x[2:]):.3f}")

        xvals = np.linspace(-50, 150, 500)
        yvals = np.linspace(-50, 150, 500)
        X, Y = np.meshgrid(xvals, yvals)

        Z12 = dij(X, Y, emitter_vel[0], emitter_vel[1], receiver1_pos, receiver2_pos, f1, f2)

        Z13 = dij(X, Y, emitter_vel[0], emitter_vel[1], receiver1_pos, receiver3_pos, f1, f3)

        Z14 = dij(X, Y, emitter_vel[0], emitter_vel[1], receiver1_pos, receiver4_pos, f1, f4)

        Z15 = dij(X, Y, emitter_vel[0], emitter_vel[1], receiver1_pos, receiver5_pos, f1, f5)

        CS = plt.contour(X, Y, Z12, levels=[0], colors=('red',), linestyles=('dashed',), linewidths=(2,), alpha=0.5)
        CS = plt.contour(X, Y, Z13, levels=[0], colors=('red',), linestyles=('dashed',), linewidths=(2,), alpha=0.5)
        CS = plt.contour(X, Y, Z14, levels=[0], colors=('red',), linestyles=('dashed',), linewidths=(2,), alpha=0.5)
        CS = plt.contour(X, Y, Z15, levels=[0], colors=('red',), linestyles=('dashed',), linewidths=(2,), alpha=0.5)
            
        plt.legend()
        plt.show() 

        num_trials = 1000
        errors = np.zeros(num_trials)
        for i in range(num_trials):
            emitter_pos = np.random.random(2) * 100
            emitter_vel = np.random.random(2) * 100
            emitter = Emitter(1090e6, 1e8, 1e8, emitter_pos, emitter_vel)
            receiver1_pos = np.random.random(2) * 100
            receiver1 = Receiver(1090e6, 2180e6, receiver1_pos)
            receiver2_pos = np.random.random(2) * 100
            receiver2 = Receiver(1090e6, 2180e6, receiver2_pos)
            receiver3_pos = np.random.random(2) * 100
            receiver3 = Receiver(1090e6, 2180e6, receiver3_pos)
            receiver4_pos = np.random.random(2) * 100
            receiver4 = Receiver(1090e6, 2180e6, receiver4_pos)
            receiver5_pos = np.random.random(2) * 100
            receiver5 = Receiver(1090e6, 2180e6, receiver5_pos)
            message = '1010'
            signal, times = emitter.generate_signal(message)
            _, _, f1 = channel(signal, times, emitter, receiver1)
            _, _, f2 = channel(signal, times, emitter, receiver2)
            _, _, f3 = channel(signal, times, emitter, receiver3)
            _, _, f4 = channel(signal, times, emitter, receiver4)
            _, _, f5 = channel(signal, times, emitter, receiver5)
            f1 = 1090e6 - f1
            f2 = 1090e6 - f2
            f3 = 1090e6 - f3
            f4 = 1090e6 - f4
            f5 = 1090e6 - f5
            x0 = np.random.random(4) * 100
            x = fsolve(f, x0, args=(receiver1_pos, receiver2_pos, receiver3_pos, receiver4_pos, receiver5_pos, f1, f2, f3, f4, f5))  
            errors[i] = np.linalg.norm(emitter_pos - x[:2])
        print(f'Mean error: {np.mean(errors)}')
        print(f'Std error: {np.std(errors)}')
        print(f"median error: {np.median(errors)}")
        print(f"Percent correct solutions: {np.sum(errors < 1) / num_trials * 100}")

def dij(x, y, vx, vy, X1, X2, F1, F2):
    x1, y1 = X1
    x2, y2 = X2
    f1, f2 = F1, F2
    return ((vx * (x - x1) + vy * (y - y1)) / np.sqrt((x - x1)**2 + (y - y1)**2) 
        - (vx * (x - x2) + vy * (y - y2)) / np.sqrt((x - x2)**2 + (y - y2)**2) 
        - c / f0 * (f1 - f2))
    
def f(z, X1, X2, X3, X4, X5, F1, F2, F3, F4, F5):
    x, y, vx, vy = z

    return [dij(x, y, vx, vy, X1, X2, F1, F2), 
            dij(x, y, vx, vy, X1, X3, F1, F3), 
            dij(x, y, vx, vy, X1, X4, F1, F4),
            dij(x, y, vx, vy, X1, X5, F1, F5)]

if __name__ == '__main__':
    main()