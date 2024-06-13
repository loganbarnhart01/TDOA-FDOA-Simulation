import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

from signal_generator import Emitter, Receiver, channel

c = 2.99792458e8
f0 = 1090e6


def main():
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

        _, _, f1 = channel(signal, times, emitter, receiver1)
        _, _, f2 = channel(signal, times, emitter, receiver2)
        _, _, f3 = channel(signal, times, emitter, receiver3)

        f1 = 1090e6 - f1
        f2 = 1090e6 - f2
        f3 = 1090e6 - f3

        vx = emitter_vel[0]
        vy = emitter_vel[1]

        x1 = receiver1_pos[0]
        y1 = receiver1_pos[1]
        x2 = receiver2_pos[0]
        y2 = receiver2_pos[1]
        x3 = receiver3_pos[0]
        y3 = receiver3_pos[1]

        
        # f1 = f0 / c * ((vx * (ems_pos[0] - x3) + vy * (emitter_pos[1] - y3)) / np.sqrt((emitter_pos[0] - x3)**2 + (emitter_pos[1] - y3)**2))

        xvals = np.linspace(-50, 150, 500)
        yvals = np.linspace(-50, 150, 500)
        X, Y = np.meshgrid(xvals, yvals)
        Z12 = d12(X, Y, emitter_vel, receiver1_pos, receiver2_pos, f1, f2)

        Z13 = d13(X, Y, emitter_vel, receiver1_pos, receiver3_pos, f1, f3)

        plt.figure()
        CS = plt.contour(X, Y, Z12, levels=[0], colors=('red',), linestyles=('dashed',), linewidths=(2,))
        CS = plt.contour(X, Y, Z13, levels=[0], colors=('red',), linestyles=('dashed',), linewidths=(2,))
        plt.plot(emitter_pos[0], emitter_pos[1], 'o', color = 'black', label = 'Emitter')
        plt.plot(x1, y1, 'o', color = 'blue', label = 'Receiver')
        plt.plot(x2, y2, 'o', color = 'blue')
        plt.plot(x3, y3, 'o', color = 'blue')
        plt.quiver(emitter_pos[0], emitter_pos[1], emitter_dir[1], emitter_dir[1], color = 'black', alpha = 0.75, label = 'Emitter Velocity', scale=1, scale_units='xy', angles='xy', pivot='tail', width=0.009)
        plt.ylabel('y')
        plt.xlabel('x')
        plt.title('Lines of Constant FDOA vs Emitter + Receiver Locations')
        plt.legend()
        plt.grid(True)
        plt.show()

        # x0 = np.array([15, -5])
        # x = fsolve(f, x0)
        # print(f"True Emitter position: ({emitter_pos[0]:.3f}, {emitter_pos[1]:.3f})\nInitial_guess: ({x0[0]}, {x0[1]})\nEstimated Emitter position: ({x[0]:.3f}, {x[1]:.3f})\nError: {np.linalg.norm(emitter_pos - x):.3f}")

def d12(x, y, V, X1, X2, F1, F2):
    vx, vy = V
    x1, y1 = X1
    x2, y2 = X2
    f1, f2 = F1, F2
    return ((vx * (x - x1) + vy * (y - y1)) / np.sqrt((x - x1)**2 + (y - y1)**2) 
        - (vx * (x - x2) + vy * (y - y2)) / np.sqrt((x - x2)**2 + (y - y2)**2) 
        - c / f0 * (f1 - f2))

def d13(x, y, V, X1, X3, F1, F3):
    vx, vy = V
    x1, y1 = X1
    x3, y3 = X3
    f1, f3 = F1, F3
    return ((vx * (x - x1) + vy * (y - y1)) / np.sqrt((x - x1)**2 + (y - y1)**2) 
        - (vx * (x - x3) + vy * (y - y3)) / np.sqrt((x - x3)**2 + (y - y3)**2) 
        - c / f0 * (f1 - f3))
    
def f(z, V, X1, X2, X3, F1, F2, F3):
    x, y = z

    return [d12(x, y, V, X1, X2, F1, F2), d13(x,y, V, X1, X3, F1, F3)]

if __name__ == '__main__':
    main()