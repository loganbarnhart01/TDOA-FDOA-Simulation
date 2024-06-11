import numpy as np
import matplotlib.pyplot as plt
import pymap3d as pm
from scipy import optimize as op
import random
from geopy import distance
from mpl_toolkits.mplot3d import Axes3D


c = 299792458.0 # speed of light in m/s

def tdoa_solver_3d():

    
    x_min = -2
    x_max = 2
    y_min = -2
    y_max = 2
    z_min = 0
    z_max = 2
    bounds = ([3*x_min, 3*y_min, 3*z_min], [3*x_max, 3*y_max, 3*z_max])
    receivers = [(x_min, y_min, z_min), (x_min, y_max, z_min), (x_max, y_min, z_min), (x_max, y_max, z_min)]
    emitter = (0, 0, 3*z_max)
    emitter_lat, emitter_lon, emitter_alt = emitter 
    
    '''
    r1 = (random.uniform(x_min, x_max), random.uniform(y_min, y_max))
    r2 = (random.uniform(x_min, x_max), random.uniform(y_min, y_max))
    r3 = (random.uniform(x_min, x_max), random.uniform(y_min, y_max))
    receivers = [r1, r2, r3]

    emitter = (random.uniform(3*x_min, 3*x_max), random.uniform(3*y_min, 3*y_max))
    emitter_lat, emitter_lon = emitter
    
    
    
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
    
    true_diff_01 = c*tdoas[0][1]
    true_diff_02 = c*tdoas[0][2]
    true_diff_03 = c*tdoas[0][3]
    true_diff_12 = c*tdoas[1][2]
    true_diff_13 = c*tdoas[1][3]
    true_diff_23 = c*tdoas[2][3]

    print(true_diff_01, ", ", true_diff_02, ", ", true_diff_03)

    x = np.linspace(3*x_min-1, 3*x_max+1, 100)
    y = np.linspace(3*y_min-1, 3*y_max+1, 100)
    z = np.linspace(3*z_min-1, 3*z_max+1, 100)
    X, Y, Z = np.meshgrid(x, y, z)

    eq0 = hyperboloid_3d(X, Y, Z, receivers[0], receivers[1], true_diff_01)
    eq1 = hyperboloid_3d(X, Y, Z, receivers[0], receivers[2], true_diff_02)
    eq2 = hyperboloid_3d(X, Y, Z, receivers[0], receivers[3], true_diff_03)
    eq3 = hyperboloid_3d(X, Y, Z, receivers[1], receivers[2], true_diff_12)
    eq4 = hyperboloid_3d(X, Y, Z, receivers[1], receivers[3], true_diff_13)
    eq5 = hyperboloid_3d(X, Y, Z, receivers[2], receivers[3], true_diff_23)

    eqs = [eq0, eq1, eq2, eq3, eq4, eq5]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for eq in eqs:
        ax.contourf(X, Y, Z, facecolors=plt.cm.viridis(eq), alpha=0.5)

    # plot_hyperboloid(ax, X, Y, Z, receivers[0], receivers[1], true_diff_01, 'r', alpha=0.5)
    # plot_hyperboloid(ax, X, Y, Z, receivers[0], receivers[2], true_diff_02, 'g', alpha=0.5)
    # plot_hyperboloid(ax, X, Y, Z, receivers[0], receivers[3], true_diff_03, 'b', alpha=0.5)
    # plot_hyperboloid(ax, X, Y, Z, receivers[1], receivers[2], true_diff_12, 'm', alpha=0.5)
    # plot_hyperboloid(ax, X, Y, Z, receivers[1], receivers[3], true_diff_13, 'c', alpha=0.5)
    # plot_hyperboloid(ax, X, Y, Z, receivers[2], receivers[3], true_diff_23, 'y', alpha=0.5)

    ax.scatter(emitter_lat, emitter_lon, emitter_alt, c='black', marker='s', s=100, label='True Emitter Location')
    ax.scatter([r[0] for r in receivers], [r[1] for r in receivers], [r[2] for r in receivers], c='blue', label='Receivers')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D TDOA Hyperboloid Visualization')
    plt.legend()
    plt.show()

    return 

    def equation(p):
            x, y = p
            eq1 = hyperbola(x, y, receivers[0], receivers[1], true_diff_01)
            eq2 = hyperbola(x, y, receivers[0], receivers[2], true_diff_02)
            eq3 = hyperbola(x, y, receivers[1], receivers[2], true_diff_12)
            return [eq1, eq2, eq3]
    
    result_ls = op.least_squares(equation, initial_guess, bounds=bounds)

    x_true, y_true = result_ls.x

#-------------------------start of loop to add noise-------------------------------------------------------------------------------------------------------------
    num_samples = 0
    hyperbolaA = []
    hyperbolaB = []
    hyperbolaC = []
    equations = []
    results = []

    
    for sample in range(num_samples):       
        # Add noise to the TDOA data (assuming Gaussian noise)
        noise_variance = 1e-9  # Adjust as needed
        noisy_tdoas = tdoas + np.random.normal(scale=noise_variance, size=tdoas.shape)
        
        diff_01 = c*noisy_tdoas[0][1]
        diff_02 = c*noisy_tdoas[0][2]
        diff_12 = c*noisy_tdoas[1][2]
    
        


        eqA = hyperbola(X, Y, receivers[0], receivers[1], diff_01)
        eqB = hyperbola(X, Y, receivers[0], receivers[2], diff_02)
        eqC = hyperbola(X, Y, receivers[1], receivers[2], diff_12)
          
        hyperbolaA.append(eqA)
        hyperbolaB.append(eqB)
        hyperbolaC.append(eqC)

        def equations(p):
            x, y = p
            eq1 = hyperbola(x, y, receivers[0], receivers[1], diff_01)
            eq2 = hyperbola(x, y, receivers[0], receivers[2], diff_02)
            eq3 = hyperbola(x, y, receivers[1], receivers[2], diff_12)
            return [eq1, eq2, eq3]

        # Find estimated emitter location
        result_ls = op.least_squares(equations, initial_guess, bounds=bounds)

        results.append(result_ls)
        

        '''
        initial_guess = [(0, 0), (-150, -150), (-150, 150), (150, -150), (150, 150)]
        results = []
        for i in initial_guess:
            result_ls = op.least_squares(equations_ls, i, bounds=bounds)
            results.append(result_ls.x)


        print("least squares: ", results)
        print("real:", emitter_lat, ", ", emitter_lon)

        '''
    
    for A in hyperbolaA:
        plt.contour(X, Y, A, levels=[0], colors='r', alpha=0.2)
    for B in hyperbolaB:
        plt.contour(X, Y, B, levels=[0], colors='g', alpha=0.2)
    for C in hyperbolaC:
        plt.contour(X, Y, C, levels=[0], colors='b', alpha=0.2)
    # ------------------------------ end of loop ---------------------------------------------------------------------------------------------------------------------    
        
    #error = np.sqrt((x_est - emitter_lat)**2 + (y_est - emitter_lon)**2)
    plt.contour(X, Y, eq0, levels=[0], colors='r')
    plt.contour(X, Y, eq1, levels=[0], colors='g')
    plt.contour(X, Y, eq2, levels=[0], colors='b')
    plt.scatter(emitter_lat, emitter_lon, c='black', marker='s', s=100,  label='True Emitter Location')
    plt.scatter(x_true, y_true, c='green', marker='s', s=60, label='Estimated Emitter Location')
    plt.scatter([r.x[0] for r in results], [r.x[1] for r in results], c='red', label='estimated emitters')
    plt.scatter([r[0] for r in receivers], [r[1] for r in receivers], c='blue', label='Receivers')
    #plt.annotate(f'Error: {error:.2f}', xy=(x_est, y_est), xytext=(x_est + 1, y_est + 1),
    #            arrowprops=dict(facecolor='black', shrink=.05))
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('TDOA Visualization')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()


    
def hyperbola(x, y, receiver_1, receiver_2, diff_ab):
    if diff_ab > 0:
        xa, ya = receiver_1
        xb, yb = receiver_2
    else:
        xa, ya = receiver_2
        xb, yb = receiver_1
        diff_ab = -diff_ab
    return np.sqrt((x - xb) ** 2 + (y - yb) ** 2) - np.sqrt((x - xa) ** 2 + (y - ya) ** 2) - diff_ab

def hyperboloid_3d(x, y, z, receiver_1, receiver_2, diff_ab):
    if diff_ab > 0:
        xa, ya, za = receiver_1
        xb, yb, zb = receiver_2
    else:
        xa, ya, za = receiver_2
        xb, yb, zb = receiver_1
        #diff_ab = -diff_ab
    return np.sqrt((x - xb) ** 2 + (y - yb) ** 2 + (z - zb) ** 2) - np.sqrt((x - xa) ** 2 + (y - ya) ** 2 + (z - za) ** 2) - diff_ab

def plot_hyperboloid(ax, X, Y, Z, receiver_1, receiver_2, diff_ab, color, alpha):
    xa, ya, za = receiver_1
    xb, yb, zb = receiver_2
    ax.plot_surface(X, Y, Z, color=color, alpha=alpha)

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