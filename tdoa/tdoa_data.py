import numpy as np
from geopy import distance

c = 299792458.0 # speed of light in m/s


def main():
    emitter = (1,1,1000)
    receivers = [(0,1,0), (1,0,0), (1,1,0)]
    tdoa = generate_true_2d_tdoa_data(emitter, receivers)
    print(tdoa)

def generate_tdoa_data(emitter, receivers, mode='random_emitter'):
    
    if mode == 'fake_signals':
        return

    if mode == 'random_emitter':
        return generate_random_tdoa_data(receivers)
    
    if mode == 'fixed_emitter':
        if emitter == None:
            raise ValueError('Emitter location must be provided for mode = \'fixed_emitter\'')
        
        if len(receivers) == 3:
            return generate_true_2d_tdoa_data(emitter, receivers)
        if len(receivers) >= 4:
            return generate_true_3d_tdoa_data(emitter, receivers)


def generate_random_tdoa_data(receivers):
    n = len(receivers)

    tdoa = np.zeros( (n, n) )

    for i in range(n):
        for j in range(i + 1, n):
            distance = distance.distance(receivers[i], receivers[j]).m
            max_time_diff = distance/c
            tdoa[i,j] = np.random.random() * max_time_diff
            tdoa[j,i] = tdoa[i,j]

    return tdoa


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

    emitter_lat, emitter_lon, _ = emitter

    # physical distances between receivers and emitters
    distances = []
    for r_lat, r_lon, _ in receivers:
        d = distance.distance((emitter_lat, emitter_lon), (r_lat, r_lon)).m
        
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
            diff = np.abs(arrival_times[i] - arrival_times[j])
            tdoa[i,j] = diff
            tdoa[j,i] = diff
    
    return tdoa

def generate_true_3d_tdoa_data(emitter, receivers):
    '''
        Generates precide time difference of arrival provided with emitter and receiver locations
        Does consider altitude - hence 3d data

        emitter: (lat, lon, alt), position for emitter if known
        receivers: [(lat, lon, alt), (lat, lon, alt), ...], positions for [receiver0, receiver1, ...]
        returns: (num_receivers, num_receivers) matrix of tdoa values. 
                 tdoa[i,j] == tdoa[j,i] is the time difference between receiver i and j  
    '''
    if emitter:
        assert len(emitter) == 2 
    for r in receivers:
        assert len(r) == 2  
    
    emitter_lat, emitter_lon, emitter_alt = emitter

    # physical distances between receivers and emitters
    distances = []
    for r_lat, r_lon, r_alt in receivers:
        d = distance.distance((emitter_lat, emitter_lon), (r_lat, r_lon)).m
        alt_dist = emitter_alt - r_alt
        distances.append(np.sqrt(d**2 + alt_dist**2))

    distances = np.array(distances)

    # true times for signal to travel in seconds
    times = distances/c

    # time differences in seconds
    min_time = min(times)
    arrival_times = times - min_time
    n = len(arrival_times)
    
    tdoa = np.zeros( (n, n))

    for i in range(n):
        for j in range(i + 1, n):
            if i == j:
                continue
            diff = np.abs(arrival_times[i] - arrival_times[j])
            tdoa[i,j] = diff
            tdoa[j,i] = diff
    
    return tdoa


if __name__ == "__main__":
    main()