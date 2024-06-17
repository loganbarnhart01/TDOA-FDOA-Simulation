import warnings

import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

from signal_generator import Emitter, Receiver

c = 2.99792458e8
f0 = 1090e6


def main():
        
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
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
        # Apply doppler
        signal1, f1 = receiver1.apply_doppler(signal1, emitter)
        signal2, f2 = receiver2.apply_doppler(signal2, emitter)
        signal3, f3 = receiver3.apply_doppler(signal3, emitter)

        # solve for soln from initial guess near emitter
        x0 = emitter_pos + np.random.random(2) * 10
        x = least_squares(f, x0, args=(emitter_vel, receiver1_pos, receiver2_pos, receiver3_pos, f1, f2, f3)).x
        print(x)
        
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
        Z12 = dij(X, Y, emitter_vel, receiver1_pos, receiver2_pos, f1, f2)
        Z13 = dij(X, Y, emitter_vel, receiver1_pos, receiver3_pos, f1, f3)
        plt.figure()
        CS = plt.contour(X, Y, Z12, levels=[0], colors=('red',), linestyles=('dashed',), linewidths=(2,))
        CS = plt.contour(X, Y, Z13, levels=[0], colors=('red',), linestyles=('dashed',), linewidths=(2,))
        plt.plot(emitter_pos[0], emitter_pos[1], 'o', color = 'black', label = 'Emitter')
        plt.plot(x[0], x[1], 'X', color = 'green', label = 'Emitter Estimate')
        plt.plot()
        plt.plot(x1, y1, 'o', color = 'blue', label = 'Receiver')
        plt.plot(x2, y2, 'o', color = 'blue')
        plt.plot(x3, y3, 'o', color = 'blue')
        plt.quiver(emitter_pos[0], emitter_pos[1], emitter_vel[0], emitter_vel[1], color = 'black', alpha = 0.75, label = 'Emitter Velocity', scale=1, scale_units='xy', angles='xy', pivot='tail', width=0.009)
        plt.legend()
        plt.show()

def channel(signal: np.ndarray, 
            times: np.ndarray, 
            emitter: Emitter, 
            receiver: Receiver):
    
    c = 299792458.0
    # Calculate and apply doppler shifts 
    f0 = emitter.frequency
    assert emitter.position.shape == receiver.position.shape
    distance = np.linalg.norm(emitter.position - receiver.position)
    f1 = f0 * (c / (c - (np.dot(emitter.velocity, receiver.position - emitter.position) / distance)))

    return  f1 
            

def dij(x, y, V, X1, X2, F1, F2):
    vx, vy = V
    x1, y1 = X1
    x2, y2 = X2
    f1, f2 = F1, F2
    return ((vx * (x - x1) + vy * (y - y1)) / np.sqrt((x - x1)**2 + (y - y1)**2) 
        - (vx * (x - x2) + vy * (y - y2)) / np.sqrt((x - x2)**2 + (y - y2)**2) 
        - c / f0 * (f1 - f2))
    
def f(z, V, X1, X2, X3, F1, F2, F3):
    x, y = z

    return [dij(x, y, V, X1, X2, F1, F2), dij(x,y, V, X1, X3, F1, F3)]

if __name__ == '__main__':
    main()