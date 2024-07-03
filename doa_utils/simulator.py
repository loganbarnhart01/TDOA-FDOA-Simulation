from typing import Optional, List

import matplotlib.pyplot as plt
import numpy as np
import random
import pymap3d as pm

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
                 cartesian: Optional[bool] = True
                 ):
    
    assert len(receiver_positions) >= 4, "At least 4 receivers are needed to simulate DOA in 3d"

    if not cartesian:
        # assuming velocity is already in east north up format. 
        lat0, lon0, h0 = receiver_positions[0]
        emitter_position = pm.geodetic2enu(*emitter_position, lat0, lon0, h0)
        receiver_positions = [pm.geodetic2enu(*pos, lat0, lon0, h0) for pos in receiver_positions]
        
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

    if not cartesian:
        fft_pos = pm.enu2geodetic(*fft_pos, lat0, lon0, h0)
        conv_pos = pm.enu2geodetic(*conv_pos, lat0, lon0, h0)
        # still assuming we're good with enu velocity. 

    return fft_pos, fft_vel, conv_pos, conv_vel
