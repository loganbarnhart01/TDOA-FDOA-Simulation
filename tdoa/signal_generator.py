from typing import List

import numpy as np
import matplotlib.pyplot as plt

class Emitter: 
    def __init__(self, 
                 frequency: int, 
                 position: np.ndarray,
                 velocity: np.ndarray):
        self.frequency = frequency
        self.sample_rate = 20 * self.frequency # 20 samples per cycle for continuous effect when emitting
        self.position = position
        self.velocity = velocity

        self.preamble = '101000010100000'
        self.modulator = {'0' : -1, # exp(2pi * j * freq * (0 + pi))
                          '1' : 1} # exp(2pi * j * freq * 1)

    def generate_signal(self, bits):
        bits = self.preamble + bits
                
        symbols = []

        for i, bit in enumerate(bits):
            symbols.append(self.modulator[bit])

        return symbols
    
class Receiver:
    def __init__(self, 
                 sample_rate: int, # samples / sec
                 bit_duration: int, # sec / bit
                 position: np.ndarray): # cartesian position coords
        # info about emitter to sample accurately
        self.sample_rate = sample_rate 
        self.bit_duration = bit_duration
        self.position = position

    def sample_signal(self, symbols: List[int]):
        samples_per_bit = int(self.sample_rate * self.bit_duration)
        demodded_signal = np.array([])
        for sym in symbols:
            sym_samples = np.ones(samples_per_bit) * sym
            demodded_signal = np.append(demodded_signal, sym_samples)
        return demodded_signal
    
    def apply_doppler(self, signal: np.ndarray, emitter: Emitter):
        
        c = 299792458.0
        f0 = emitter.frequency
        distance = np.linalg.norm(emitter.position - self.position) # meters
        v = np.dot(emitter.velocity, self.position - emitter.position) / distance # velocity in direction of receiver m/s
        
        f1 = f0 * (c / (c + v)) - f0

        doppler_shifted_signal = signal * np.exp(2 * np.pi * 1j * f1)
        return doppler_shifted_signal, f1
    
    def add_time_delay(self, signal: np.ndarray, emitter: Emitter):
        c = 299792458.0
        distance = np.linalg.norm(emitter.position - self.position)
        time_delay = distance / c
        # return np.append(np.zeros(int(time_delay * self.sample_rate)), signal)
        return time_delay
    
    def signal_to_noise_ratio(self, signal: np.ndarray, distance: float):
        signal_power = np.sum(np.abs(signal)**2) / len(signal)
        snr_from_distance = lambda x : (1 - 4) / (400000) * x + 4
        snr = snr_from_distance(distance)
        noise_var = signal_power / snr
        return noise_var
    
    def add_noise(self, signal: np.ndarray, emitter: Emitter):
        distance = np.linalg.norm(emitter.position - self.position)
        noise_var = self.signal_to_noise_ratio(signal, distance)
        real_noise = np.random.normal(0, noise_var**2/2, len(signal))
        imag_noise = np.random.normal(0, noise_var**2/2, len(signal))
        noise = real_noise + 1j * imag_noise
        return signal + noise
