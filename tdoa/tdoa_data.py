import numpy as np
from geopy import distance

def main():
    emitter = (1,1,1000)
    receivers = [(0,1,0), (1,0,0), (1,1,0)]
    tdoa = generate_true_2d_tdoa_data(emitter, receivers)
    print(tdoa)

def generate_tdoa_data(emitter, receivers, mode=''):
    
    if mode == 'fake_signals':
        return

    if mode == 'random_emitter':
        return
    
    if mode == 'fixed_emitter':
        if emitter == None:
            raise ValueError('Emitter location must be provided')
        
        if len(receivers) == 3:
            return generate_true_2d_tdoa_data(emitter, receivers)
        if len(receivers) >= 4:
            return generate_true_3d_tdoa_data(emitter, receivers)


def generate_random_2d_tdoa_data(receivers):
    return

def generate_true_2d_tdoa_data(emitter, receivers):
    '''
        Generates precide time difference of arrival provided with emitter and receiver locations
        Does not consider altitude - hence 2d data

        emitter: (lat, lon, alt) 
        receivers: [(lat, lon, alt), (lat, lon, alt), ...] 
        returns: [tdoa1, tdoa2, ...], tdoai == 0 is the reciever which first receives the signal
    '''
    

    c = 299792458.0 # speed of light in m/s

    emitter_lat, emitter_lon, _ = emitter

    # physical distances between receivers and emitters
    distances = []
    for r_lat, r_lon, _ in receivers:
        d = distance.distance((emitter_lat, emitter_lon), (r_lat, r_lon)).m
        
        distances.append(d)

    times = np.array(distances)/c
    min_time = min(times)
    tdoa = times - min_time
    return tdoa

def generate_true_3d_tdoa_data(emitter, receivers):
    '''
        Generates precide time difference of arrival provided with emitter and receiver locations
        Does consider altitude - hence 3d data

        emitter: (lat, lon, alt) 
        receivers: [(lat, lon, alt), (lat, lon, alt), ...] 
        returns: [tdoa1, tdoa2, ...], tdoai == 0 is the reciever which first receives the signal
    '''
    c = 299792458.0 # speed of light in m/s
    
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
    tdoa = times - min_time

    return tdoa


if __name__ == "__main__":
    main()