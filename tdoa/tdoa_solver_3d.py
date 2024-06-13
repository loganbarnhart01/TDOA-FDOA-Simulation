import numpy as np
from scipy import optimize as op
import random
# possible imports for 3d graphing
import matplotlib.pyplot as plt
from geopy import distance
from mpl_toolkits.mplot3d import Axes3D
import pyvista as pv
import pymap3d as pm
from pymap3d import ecef2geodetic
from mayavi import mlab
import pyqtgraph as pg
from PyQt5 import QtWidgets

c = 299792458.0 # speed of light in m/s


def tdoa_solver_3d():

    
    x_min = -100
    x_max = 100
    y_min = -100
    y_max = 100
    z_min = 0
    z_max = 100
    bounds = ([3*x_min, 3*y_min, 3*z_min], [3*x_max, 3*y_max, 3*z_max])
    
    # receivers = [(x_min, y_min, z_min), (x_min, y_max, z_min), (x_max, y_min, z_min), (x_max, y_max, z_min)]
    # emitter = (0, 4, 3*z_max)
    # emitter_lat, emitter_lon, emitter_alt = emitter 

    num_trials = 10000
    errors = np.zeros(num_trials)
    for i in range (num_trials):

        
        r0 = (random.uniform(x_min, x_max), random.uniform(y_min, y_max), random.uniform(z_min, z_max))
        r1 = (random.uniform(x_min, x_max), random.uniform(y_min, y_max), random.uniform(z_min, z_max))
        r2 = (random.uniform(x_min, x_max), random.uniform(y_min, y_max), random.uniform(z_min, z_max))
        r3 = (random.uniform(x_min, x_max), random.uniform(y_min, y_max), random.uniform(z_min, z_max))
        receivers = [r0, r1, r2, r3]

        emitter = (random.uniform(3*x_min, 3*x_max), random.uniform(3*y_min, 3*y_max), random.uniform(3*z_min, 3*z_max))
        
        
        '''
        ###################################
        test case for 2 possible solutions
        receivers = [(-131, -120), (-68, -122), (-72, -68)]
        emitter = (5, 40)
        emitter_lat, emitter_lon = emitter
        
        '''  

        tdoas = generate_true_tdoa_data(emitter, receivers)

        '''
        # physical distances between receivers and emitters 
        real_dists = []
        for r in receivers:
            receiver_lat, receiver_lon = r
            d = np.sqrt((receiver_lat - emitter_lat)**2 + (receiver_lon - emitter_lon)**2)
            real_dists.append(d)

        diff_01 = (real_dists[1] - real_dists[0])
        diff_02 = (real_dists[2] - real_dists[0])
        diff_12 = (real_dists[2] - real_dists[1])
        '''

        x = np.linspace(3*x_min-1, 3*x_max+1, 300)
        y = np.linspace(3*y_min-1, 3*y_max+1, 300)
        z = np.linspace(3*z_min-1, 3*z_max+1, 300)
        #X, Y = np.meshgrid(x, y)
        initial_guess = (0, 0, 0)


        true_diffs = c * tdoas[np.triu_indices(len(receivers), 1)]

        def equations(p):
            x, y, z = p
            eq1 = hyperboloid_3d(x, y, z, receivers[0], receivers[1], true_diffs[0])
            eq2 = hyperboloid_3d(x, y, z, receivers[0], receivers[2], true_diffs[1])
            eq3 = hyperboloid_3d(x, y, z, receivers[0], receivers[3], true_diffs[2])

            eq4 = hyperboloid_3d(x, y, z, receivers[1], receivers[2], true_diffs[3])
            eq5 = hyperboloid_3d(x, y, z, receivers[1], receivers[3], true_diffs[4])
            eq6 = hyperboloid_3d(x, y, z, receivers[2], receivers[3], true_diffs[5])
            return [eq1, eq2, eq3, eq4, eq5, eq6]


        initial_guess = (0, 0, 3*z_max)
        result = op.least_squares(equations, initial_guess, bounds=bounds, ftol=1e-8, xtol=1e-8, gtol=1e-8)
        errors[i] = np.linalg.norm(result.x - np.array(emitter))

    print(f'Mean error: {np.mean(errors)}')
    print(f'Std error: {np.std(errors)}')
    print(f"median error: {np.median(errors)}")
    print(f"Percent correct solutions: {np.sum(errors < 1) / num_trials * 100}")


def hyperboloid_3d(x, y, z, receiver_1, receiver_2, diff_ab):
        if diff_ab > 0:
            xa, ya, za = receiver_1
            xb, yb, zb = receiver_2
        else:
            xa, ya, za = receiver_2
            xb, yb, zb = receiver_1
            diff_ab = -diff_ab
        return np.sqrt((x - xb) ** 2 + (y - yb) ** 2 + (z - zb) ** 2) - np.sqrt((x - xa) ** 2 + (y - ya) ** 2 + (z - za) ** 2) - diff_ab

def generate_true_tdoa_data(emitter, receivers, coord_sys='cartesian'):
    distance_func = get_distance_func(len(emitter), coord_sys)

    # physical distances between receivers and emitters
    distances = []
    for r in receivers:
        d = distance_func(emitter, r)
        distances.append(d)

    times = np.array(distances)/c
    min_time = min(times)
    arrival_times = times - min_time
    n = len(arrival_times)
    
    tdoa = np.zeros( (n, n))

    for i in range(n):
        for j in range(i + 1, n):
            if i == j:
                continue
            diff = arrival_times[j] - arrival_times[i]
            tdoa[i,j] = diff
            tdoa[j,i] = diff
    
    return tdoa

def get_distance_func(dim, coord_sys):
    if coord_sys == 'cartesian':
        if dim == 2:
            return lambda x,y: np.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)
        if dim == 3:
            return lambda x,y: np.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2 + (x[2] - y[2])**2)
        
    if coord_sys == 'latlon':
        if dim == 2:
            return lambda x,y: distance.distance(x,y).m
        if dim == 3:
            return lambda x,y: np.sqrt( (distance.distance((x[0], x[1]), (y[0], y[1])).m)**2 + (x[2] - y[2])**2)

    
tdoa_solver_3d()