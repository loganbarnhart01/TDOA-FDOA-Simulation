import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

from signal_generator import Emitter, Receiver, channel


emitter_pos = np.array([0,0])
emitter_vel = np.array([10,10])
emitter = Emitter(1090e6, 1e8, 1e8, emitter_pos, emitter_vel)

receiver1_pos = np.array([10, 15])
receiver1 = Receiver(1090e6, 2180e6, receiver1_pos)

receiver2_pos = np.array([-17, -8])
receiver2 = Receiver(1090e6, 2180e6, receiver2_pos)

receiver3_pos = np.array([10, -11])
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

c = 2.99792458e8
f0 = 1090e6

# f1 = f0 / c * ((vx * (ems_pos[0] - x3) + vy * (emitter_pos[1] - y3)) / np.sqrt((emitter_pos[0] - x3)**2 + (emitter_pos[1] - y3)**2))

def d12(x, y):
    return ((vx * (x - x1) + vy * (y - y1)) / np.sqrt((x - x1)**2 + (y - y1)**2) 
            - (vx * (x - x2) + vy * (y - y2)) / np.sqrt((x - x2)**2 + (y - y2)**2) 
            - c / f0 * (f1 - f2))

def d13(x, y):
    return ((vx * (x - x1) + vy * (y - y1)) / np.sqrt((x - x1)**2 + (y - y1)**2) 
            - (vx * (x - x3) + vy * (y - y3)) / np.sqrt((x - x3)**2 + (y - y3)**2) 
            - c / f0 * (f1 - f3))
      
def f(z):
    x, y = z

    return [d12(x, y), d13(x,y)]

xvals = np.linspace(-20, 30, 500)
yvals = np.linspace(-20, 20, 500)
X, Y = np.meshgrid(xvals, yvals)
Z12 = d12(X, Y)

Z13 = d13(X, Y)

plt.figure()
CS = plt.contour(X, Y, Z12, levels=[0], colors=('red',), linestyles=('dashed',), linewidths=(2,))
CS = plt.contour(X, Y, Z13, levels=[0], colors=('red',), linestyles=('dashed',), linewidths=(2,))
plt.plot(emitter_pos[0], emitter_pos[1], 'o', color = 'black', label = 'Emitter')
plt.plot(x1, y1, 'o', color = 'blue', label = 'Receiver')
plt.plot(x2, y2, 'o', color = 'blue')
plt.plot(x3, y3, 'o', color = 'blue')
plt.quiver([emitter_vel[0]], [emitter_vel[1]], color = 'black', alpha = 0.75, label = 'Emitter Velocity', scale=1, scale_units='xy', angles='xy', pivot='tail', width=0.009)
plt.ylabel('y')
plt.xlabel('x')
plt.title('Lines of Constant FDOA vs Emitter + Receiver Locations')
plt.legend()
plt.grid(True)
plt.show()

fig, ax = plt.subplots()
CS = ax.contourf(X, Y, Z12 + Z13)
plt.plot(emitter_pos[0], emitter_pos[1], 'o', color = 'black', label = 'Emitter')
plt.plot(x1, y1, 'o', color = 'blue', label = 'Receiver')
plt.plot(x2, y2, 'o', color = 'blue')
plt.plot(x3, y3, 'o', color = 'blue')
plt.quiver([emitter_vel[0]], [emitter_vel[1]], color = 'black', alpha = 0.75, label = 'Emitter Velocity', scale=1, scale_units='xy', angles='xy', pivot='tail', width=0.009)
plt.ylabel('y')
plt.xlabel('x')
plt.title('Lines of Constant FDOA vs Emitter + Receiver Locations')
# CS = plt.contour(X, Y, Z12, levels=[0], colors=('red',), linestyles=('dashed',), linewidths=(2,), label = 'Constant FDOA')
ax.clabel(CS, inline=1, fontsize=10, colors='white')
ax.set_title('Lines of Constant FDOA vs Emitter + Receiver Locations')
plt.show()