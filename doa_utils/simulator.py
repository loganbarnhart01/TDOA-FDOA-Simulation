from typing import Optional, List

import numpy as np
import random

from signal_generator import Emitter, Receiver
from caf import convolution_caf, fft_caf

def simulate_doa(emitter_position: np.ndarray,
                 emitter_velocity: np.ndarray,  
                 receiver_positions: List[np.ndarray], 
                 message: Optional[str], 
                 emitter_freq: Optional[int] = 1090e6, 
                 sampling_rate: Optional[int] = 21.80e6,
                 bit_duration: Optional[float] = 1e-6, 
                 ):
    
    if message is None:
        message = ''.join([random.choice('01') for _ in range(10000)])
    
    emitter = Emitter(emitter_freq, emitter_position, emitter_velocity)
    receivers = [Receiver(sampling_rate, bit_duration, pos) for pos in receiver_positions]
   
    symbols = emitter.generate_signal(message)
    signals = [receiver.receive(symbols, emitter) for receiver in receivers]

    fft_fdoa_values = []
    fft_tdoa_values = []
    conv_fdoa_values = []   
    conv_tdoa_values = []

    for s in signals[1:]:
        _, tshift, fshift, _, _ = fft_caf(signals[0], s, 1001)
        fft_fdoa_values.append(fshift)
        fft_tdoa_values.append(tshift)
        _, tshift, fshift, _, _ = convolution_caf(signals[0], s, 1001)
        conv_fdoa_values.append(fshift)
        conv_tdoa_values.append(tshift)

    

