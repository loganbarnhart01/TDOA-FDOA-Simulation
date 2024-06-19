import numpy as np

from signal_generator import Emitter, Receiver
from solver import estimate_emitter

def main():
    flag = "fdoa"
    dim = 2

    num_receivers_map = {
        "tdoa + fdoa" : dim + 1,
        "tdoa" : dim + 1,
        "fdoa no velocity" : 2*dim + 1,
        "fdoa" : dim + 1,
    }

    num_receivers = num_receivers_map[flag]

    emitter_pos = (np.random.random(dim) - 0.5) * 10000
    emitter_vel = (np.random.random(dim) - 0.5) * 100
    emitter = Emitter(1090e6, emitter_pos, emitter_vel)

    message = "1010"

    receivers = [Receiver(20.90e6, 1e-6, (np.random.random(dim) - 0.5) * 10000) for i in range(num_receivers)]
    
    symbols = emitter.generate_signal(message)

    signals = [receiver.sample_signal(symbols) for receiver in receivers]
    doppler_info = [receivers[i].apply_doppler(signals[i], emitter) for i in range(num_receivers)]
    signals, doppler_freqs = zip(*doppler_info)
    times_info = [receivers[i].add_time_delay(signals[i], emitter) for i in range(num_receivers)]
    time_signal, time_delays = zip(*times_info)

    times = times + np.random.random(len(times), 1e-6)
    doppler_freqs = doppler_freqs + np.random.random(len(doppler_freqs), 1e-6)
    
    if flag == "tdoa + fdoa":
        solution = estimate_emitter(receivers, fdoa_data=doppler_freqs, toa_data=times)
        position = solution[:dim]
        velocity = solution[dim:]

    if flag == "tdoa":
        solution = estimate_emitter(receivers, toa_data=times)
        position = solution

    if flag == "fdoa no velocity":
        solution = estimate_emitter(receivers, fdoa_data=doppler_freqs)
        position = solution[:dim]
        velocity = solution[dim:]

    if flag == "fdoa":
        solution = estimate_emitter(receivers, fdoa_data=doppler_freqs, emitter_velocity=emitter_vel)
        position = solution

    print(f"True Emitter Position: {emitter_pos}")
    print(f"Estimated Emitter Position: {position}")
    
    if flag == "tdoa + fdoa" or flag == "fdoa no velocity":
        print(f"True Emitter Velocity: {emitter_vel}")
        print(f"Estimated Emitter Velocity: {velocity}")

    print(f"Error in Position: {np.linalg.norm(emitter_pos - position)}")
    
    if flag == "tdoa + fdoa" or flag == "fdoa no velocity":
        print(f"Error in Velocity: {np.linalg.norm(emitter_vel - velocity)}")


if __name__ == "__main__":
    main()