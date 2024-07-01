from typing import Optional, List

import matplotlib.pyplot as plt
import numpy as np
import random

from signal_generator import Emitter, Receiver
from caf import convolution_caf, fft_caf
from solver import estimate_emitter

def simulate_doa(emitter_position: np.ndarray,
                 emitter_velocity: np.ndarray,  
                 receiver_positions: List[np.ndarray], 
                 message: Optional[str], 
                 emitter_freq: Optional[int] = 1090e6, 
                 sampling_rate: Optional[int] = 21.80e6,
                 bit_duration: Optional[float] = 1e-6, 
                 ):
    
    assert len(receiver_positions) >= 4, "At least 4 receivers are needed to simulate DOA in 3d"

    if message is None:
        message = ''.join([random.choice('01') for _ in range(10000)])
    
    emitter = Emitter(emitter_freq, emitter_position, emitter_velocity)
    receivers = [Receiver(sampling_rate, bit_duration, pos) for pos in receiver_positions]
   
    symbols = emitter.generate_signal(message)
    signals = []

    for receiver in receivers:
        signal, tdoa, fdoa = receiver.receive(symbols, emitter, return_true_values=True)
        signals.append(signal)

    fft_fdoa_values = [0]
    fft_tdoa_values = [0]
    conv_fdoa_values = [0]   
    conv_tdoa_values = [0]

    for s in signals[1:]:
        _, tshift, fshift, _, _ = fft_caf(signals[0], s, 11)
        fft_fdoa_values.append(fshift * receiver.sample_rate)
        fft_tdoa_values.append(tshift / receiver.sample_rate)
        _, tshift, fshift, _, _ = convolution_caf(signals[0], s, 11)
        conv_fdoa_values.append(fshift * receiver.sample_rate)
        conv_tdoa_values.append(tshift / receiver.sample_rate)

    fft_est_emitter = estimate_emitter(receivers, fft_fdoa_values, fft_tdoa_values)
    conv_est_emitter = estimate_emitter(receivers, conv_fdoa_values, conv_tdoa_values)

    fft_pos = fft_est_emitter[:3]
    fft_vel = fft_est_emitter[3:]
    conv_pos = conv_est_emitter[:3]
    conv_vel = conv_est_emitter[3:]

    fft_pos_error = np.linalg.norm(fft_pos - emitter_position)
    fft_vel_error = np.linalg.norm(fft_vel - emitter_velocity)
    conv_pos_error = np.linalg.norm(conv_pos - emitter_position)
    conv_vel_error = np.linalg.norm(conv_vel - emitter_velocity)

    return fft_pos, fft_vel, conv_pos, conv_vel
    
def main():
    emitter_position = np.array([100, 100, 100])
    emitter_velocity = np.array([0, -70, 0])
    receiver_positions = [np.array([0, 0, 0]), np.array([100, 0, 0]), np.array([0, 100, 0]), np.array([0, 0, 100])]
    fft_pos, fft_vel, conv_pos, conv_vel = simulate_doa(emitter_position, emitter_velocity, receiver_positions, None)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(*emitter_position, marker='o', c='b', label='Emitter')
    ax.quiver(*emitter_position, *emitter_velocity, color='b')
    ax.scatter(*fft_pos, marker='o', c='g', label='FFT-CAF')
    ax.quiver(*fft_pos, *fft_vel, color='g')
    ax.scatter(*conv_pos, marker='x', c='r', label='Conv-CAF')
    ax.quiver(*conv_pos, *conv_vel, color='r')
    ax.scatter(*receiver_positions[0], c='k', label=f'Receiver')

    for i, receiver in enumerate(receiver_positions[1:]):
        ax.scatter(*receiver, c='k') 

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    plt.show()

if __name__ == "__main__":
    main()