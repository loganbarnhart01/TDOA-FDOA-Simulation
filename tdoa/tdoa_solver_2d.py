import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import least_squares
import random

c = 299792458.0 # speed of light in m/s

def test():

    
    x_min = 0
    x_max = 100
    y_min = 0
    y_max = 100
    
    
    r1 = (random.uniform(x_min, x_max), random.uniform(y_min, y_max))
    r2 = (random.uniform(x_min, x_max), random.uniform(y_min, y_max))
    r3 = (random.uniform(x_min, x_max), random.uniform(y_min, y_max))
    receivers = [r1, r2, r3]

    emitter = (random.uniform(3*x_min, 3*x_max), random.uniform(3*y_min, 3*y_max))
    emitter_lat, emitter_lon = emitter
    '''
    
    receivers = [(0, 0), (100, 0), (0, 100)]
    emitter = (300, 300)
    emitter_lat, emitter_lon = emitter
    '''
    '''
    tdoas = generate_true_2d_tdoa_data(emitter, receivers)

    print(tdoas)

    diff_01 = -tdoas[0][1]
    diff_02 = -tdoas[0][2]
    diff_12 = -tdoas[1][2]
  
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
    

    x = np.linspace(-2, 300, 1000)
    y = np.linspace(-2, 300, 1000)
    X, Y = np.meshgrid(x, y)


    eqA = hyperbola(X, Y, receivers[0], receivers[1], diff_01)
    plt.contour(X, Y, eqA, levels=[0], colors='r')

    eqB = hyperbola(X, Y, receivers[0], receivers[2], diff_02)
    plt.contour(X, Y, eqB, levels=[0], colors='g')
    
    
    eqC = hyperbola(X, Y, receivers[1], receivers[2], diff_12)
    plt.contour(X, Y, eqC, levels=[0], colors='b')
    
    
    
    
    def equations(p):
        x, y = p
        eq1 = hyperbola(x, y, receivers[0], receivers[1], diff_01)
        eq2 = hyperbola(x, y, receivers[0], receivers[2], diff_02)
        eq3 = hyperbola(x, y, receivers[1], receivers[2], diff_12)
        return [eq1, eq2, eq3]

    initial_guess = (receivers[0][0], receivers[0][1])

    result = least_squares(equations, initial_guess)

    x_est, y_est = result.x

    error = np.sqrt((x_est - emitter_lat)**2 + (y_est - emitter_lon)**2)



    plt.scatter(emitter_lat, emitter_lon, c='black', marker='s', s=100,  label='True Emitter Location')
    plt.scatter(x_est, y_est, c='red', label='Estimated Emitter Location')
    plt.scatter([r[0] for r in receivers], [r[1] for r in receivers], c='blue', label='Receivers')
    plt.annotate(f'Error: {error:.2f}', xy=(x_est, y_est), xytext=(x_est + 0.1, y_est + 0.1),
                 arrowprops=dict(facecolor='black', shrink=0.05))
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
        diff_ab = abs(diff_ab)
    

    return np.sqrt((x - xb) ** 2 + (y - yb) ** 2) - np.sqrt((x - xa) ** 2 + (y - ya) ** 2) - diff_ab


def generate_true_2d_tdoa_data(emitter, receivers):
    '''
        Generates precide time difference of arrival provided with emitter and receiver locations
        Does not consider altitude - hence 2d data

        emitter: (lat, lon), position for emitter if known
        receivers: [(lat, lon), (lat, lon), ...] = coords for [receiver0, receiver1, ...]
        returns: matrix of tdoa values with shape (num_receivers, num_receivers)  
                 tdoa[i,j] == tdoa[j,i] is the time difference between receiver i and j  
    '''

    if emitter:
        assert len(emitter) == 2 
    for r in receivers:
        assert len(r) == 2  

    emitter_lat, emitter_lon = emitter

    # physical distances between receivers and emitters
    distances = []
    for r_lat, r_lon in receivers:
        d = np.sqrt((r_lat - emitter_lat)**2 + (r_lon - emitter_lon)**2)
        
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
            diff = (arrival_times[j] - arrival_times[i])
            tdoa[i,j] = diff
            tdoa[j,i] = diff
    
    return tdoa
    
test()