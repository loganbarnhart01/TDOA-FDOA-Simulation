import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters for the hyperboloids
a = 1
b = 1
c = 1

# Create a grid of points
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
x, y = np.meshgrid(x, y)

# Hyperboloid of one sheet
fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
z1 = np.sqrt((x**2/a**2 + y**2/b**2 - 1) * c**2)
z2 = -z1
ax.plot_surface(x, y, z1, alpha=0.5, cmap='viridis')
ax.plot_surface(x, y, z2, alpha=0.5, cmap='viridis')
ax.set_title('Hyperboloid of One Sheet')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Hyperboloid of two sheets
fig = plt.figure()
ax = fig.add_subplot(122, projection='3d')
z1 = np.sqrt((x**2/a**2 - y**2/b**2 + 1) * c**2)
z2 = -z1
ax.plot_surface(x, y, z1, alpha=0.5, cmap='viridis')
ax.plot_surface(x, y, z2, alpha=0.5, cmap='viridis')
ax.set_title('Hyperboloid of Two Sheets')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
