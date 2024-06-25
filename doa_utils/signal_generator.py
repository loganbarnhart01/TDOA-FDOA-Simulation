from typing import List

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from matplotlib import cm

from caf import caf

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

    def generate_signal(self, 
                        bits: str):
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
    
    def apply_doppler(self, 
                      signal: np.ndarray, 
                      emitter: Emitter):
        
        c = 299792458.0
        f0 = emitter.frequency
        distance = np.linalg.norm(emitter.position - self.position) # meters
        v = np.dot(emitter.velocity, self.position - emitter.position) / distance # velocity in direction of receiver m/s
        
        f1 = f0 * (c / (c + v)) - f0

        doppler_shifted_signal = signal * np.exp(2 * np.pi * 1j * f1 / self.sample_rate * np.arange(len(signal)))
        return doppler_shifted_signal, f1
    
    def add_time_delay(self, 
                       signal: np.ndarray, 
                       emitter: Emitter):
        
        ''' OR TAKE FFT to get into freq. domain, multiply all signal values by e^{2pi* j * f * tshift} then take ifft. (tshift is in seconds and f is a range of freqs)'''
        c = 299792458.0
        distance = np.linalg.norm(emitter.position - self.position)
        time_delay_seconds = distance / c

        # time_delay_samples = time_delay_seconds * self.sample_rate

        # print(f"Time delay: {time_delay_seconds} seconds - {time_delay_samples} samples")
        # N = len(signal)
        # k = np.arange(N)
        # # time_shift = np.exp( (2 * np.pi * 1j * k * time_delay_samples) / N + time_delay_samples * np.pi * 1j)
        # time_shift = -np.exp( (2 * np.pi * 1j * k * time_delay_samples) / N)
        # freq_shift = np.fft.fftshift(time_shift)

        # fft_signal = np.fft.fft(signal)
        # fft_delay_signal = fft_signal * freq_shift
        # shift_signal = np.fft.ifft(fft_delay_signal)

        # return shift_signal, time_delay_seconds

        time_delay_samples = time_delay_seconds * self.sample_rate
        integer_delay = int(time_delay_samples)
        fractional_delay = time_delay_samples - integer_delay

        N = 100
        n = np.arange(N)
        h = np.sinc(n - (N - 1) / 2 - fractional_delay)
        h *= np.blackman(N)
        h /= np.sum(h)

        time_delayed_signal = np.convolve(signal, h, mode='same')
        integer_delay_signal = np.zeros(integer_delay, dtype=complex)
        time_delayed_signal = np.append(integer_delay_signal, time_delayed_signal)
        time_delayed_signal = time_delayed_signal[:len(signal)]

        return time_delayed_signal, time_delay_seconds
    
    def signal_to_noise_ratio(self, 
                              signal: np.ndarray, 
                              distance: float):
        signal_power = np.sum(np.abs(signal)**2) / len(signal)
        snr_from_distance = lambda x : (1 - 4) / (400000) * x + 4
        snr = snr_from_distance(distance)
        noise_var = signal_power / snr
        return noise_var
    
    def add_noise(self, 
                  signal: np.ndarray, 
                  emitter: Emitter):
        distance = np.linalg.norm(emitter.position - self.position)
        noise_var = self.signal_to_noise_ratio(signal, distance)
        real_noise = np.random.normal(0, noise_var**2/2, len(signal))
        imag_noise = np.random.normal(0, noise_var**2/2, len(signal))
        noise = real_noise + 1j * imag_noise
        return signal + noise

def main():
    emitter = Emitter(1090e6, np.array([0, 0, 0]), np.array([100, 0, 0]))
    receiver1 = Receiver(21.80e6, 1e-6, np.array([1000, 0, 0]))
    receiver2 = Receiver(21.80e6, 1e-6, np.array([-50, 0, 0]))
    
    message = '1010'
    symbols = emitter.generate_signal(message)
 
    signal1 = receiver1.sample_signal(symbols)

    doppler_signal1, f1 = receiver1.apply_doppler(signal1, emitter)
    time_delayed_signal1, t1 = receiver1.add_time_delay(doppler_signal1, emitter)
    noisy_signal1 = receiver1.add_noise(time_delayed_signal1, emitter)

    signal2 = receiver2.sample_signal(symbols)
    doppler_signal2, f2 = receiver2.apply_doppler(signal2, emitter)
    time_delayed_signal2, t2 = receiver2.add_time_delay(doppler_signal2, emitter)

    fig, ax = plt.subplots(2, 1)

    ax[0].plot(np.real(signal1))
    ax[1].plot(np.real(time_delayed_signal1), c='r')
    plt.show()
    noisy_signal2 = receiver2.add_noise(time_delayed_signal2, emitter)

    plt.plot(noisy_signal1)
    plt.plot(noisy_signal2)
    plt.show()

    max_caf, tshift_caf, fshift_caf, caf_values = caf(noisy_signal1, noisy_signal2, 80, 800, 250)

    print(f"True time shift: {int((t1 - t2) * receiver1.sample_rate)} samples")
    print(f"Time shift: {tshift_caf} samples")

    print(f"True freq shift: {f1 - f2} Hz")
    print(f"Freq shift: {fshift_caf} Hz")

    noisy_signal1 = noisy_signal1[int(tshift_caf):]
    noisy_signal1 = noisy_signal1 * np.exp(2j * np.pi * fshift_caf * np.arange(len(noisy_signal1)) / receiver1.sample_rate)

    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    X, Y = np.linspace(-6, 6, caf_values.shape[1]), np.linspace(-800, 800, caf_values.shape[0])
    X, Y = np.meshgrid(X, Y)

    Z = np.abs(caf_values)
    ls = LightSource(270, 45)
    rgb = ls.shade(Z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=rgb,
                       linewidth=0, antialiased=False, shade=False)
    
    plt.imshow(np.abs(caf_values), aspect='auto', extent=[-6, 6, -800, 800])
    plt.show()


if __name__ == '__main__':
    main()