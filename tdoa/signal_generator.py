import numpy as np
import matplotlib.pyplot as plt

global frequency_scale
frequency_scale = 1e6
    
    # def demodulate(self, signal):
    #     num_samples_per_bit = int(self.sample_rate * self.bit_duration)
    #     num_bits = int(len(signal) / num_samples_per_bit)
    #     bits = ''

    #     for i in range(num_bits):
    #         midpoint_idx = i * num_samples_per_bit + int(num_samples_per_bit / 2)
    #         sample_value = signal[midpoint_idx]
    #         bit = '0' if np.abs(np.angle(sample_value)) < 1/2 else '1'
    #         bits += bit

    #     bits = bits[self.preamble_length:] # remove the preamble
        
    #     return bits
    
    # def find_signal_start(self, receiver_signal):
    #     preamble_signal = self.modulate('', noisy=False)
    #     correlation = np.correlate(receiver_signal, preamble_signal, mode='full')
    #     return np.argmax(correlation), correlation

class Emitter: 
    def __init__(self, frequency, bit_rate, sample_rate, x, y, z = None):
        self.bit_rate = bit_rate / frequency_scale
        self.frequency = frequency / frequency_scale
        self.sample_rate = sample_rate / frequency_scale

        self.x = x
        self.y = y
        self.z = z
        
        self.preamble = '101000010100000'
        self.modulator = {'0' : lambda x : np.exp(1j * (2 * np.pi * self.frequency * x + np.pi)),
                          '1' : lambda x : np.exp(1j * (2 * np.pi * self.frequency * x))}

    def generate_signal(self, bits):
        bits = self.preamble + bits
        num_samples = int(self.sample_rate / self.bit_rate)
        signal = np.array([])

        for bit in bits:
            sample_times = np.linspace(0, 1 / self.bit_rate, num_samples, endpoint=False)
            samples = self.modulator[bit](sample_times)
            signal = np.concatenate((signal, samples))

        return signal
    
class Receiver:
    def __init__(self, sample_rate, x, y, z = None):
        self.sample_rate = sample_rate / frequency_scale

        self.x = x
        self.y = y
        self.z = z

    def collect_signal(self, signal):
        sampling_interval = int(np.ceil((1e8 / frequency_scale) / self.sample_rate))

        sampled_signal = signal[::sampling_interval]
        return sampled_signal

    
def main():
    emitter = Emitter(1090e6, 1e6, 1e8)
    receiver = Receiver(2180e6)
    
    signal = emitter.generate_signal('1010')
    sampled_signal = receiver.collect_signal(signal)

    fig, ax = plt.subplots(2, 1)
    ax[0].plot(np.real(signal)[:200], label = 'real')
    ax[0].plot(np.imag(signal)[:200], label = 'imag')
    ax[0].set_title('\'True\' Signal')

    ax[1].plot(np.real(sampled_signal)[:200], label = 'real')
    ax[1].plot(np.imag(sampled_signal)[:200], label = 'imag')
    ax[1].set_title('Sampled Signal')
    plt.show()

if __name__ == '__main__':
    main()