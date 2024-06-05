import numpy as np
import matplotlib.pyplot as plt

class ADSBEncoder:
    def __init__(self, freq=1e6 * 1090, sample_rate=1e8, bit_duration=1e-6):
        '''
            freq: frequency to transmit at in MHz - default to 1090 MHz
            sample_rate: number of samples per second - default to 10 MHz
            bit_duration: duration of each bit in seconds
            preamble: preamble to use for the message identification
            modulator: dictionary of functions to modulate the signal depending on bit value
            demodulator: dictionary of functions to demodulate the signal depending on bit value
        '''
        self.preamble = '101000010100000'
        self.preamble_length = len(self.preamble)
        self.freq = freq
        self.period = 1 / freq
        self.sample_rate = sample_rate
        self.bit_duration = bit_duration
        # modulate using BPSK
        self.modulator = {'0': lambda x : np.cos(2*np.pi*freq * x + np.pi), 
                          '1': lambda x : np.cos(2*np.pi*freq * x)}
        self.demodulator = lambda x : np.arccos(x) / (2 * np.pi * freq)


    def modulate(self, bits):    
        bits = self.preamble + bits
        num_samples = int(self.sample_rate * self.bit_duration)
        signal = np.array([])
        for i, bit in enumerate(bits):
            sample_times = np.linspace(0, self.period, num_samples, endpoint=False)
            samples = self.modulator[bit](sample_times)
            signal = np.concatenate((signal, samples))

        return signal
    
    def demodulate(self, signal):
        num_samples_per_bit = int(self.sample_rate * self.bit_duration)
        num_bits = int(len(signal) / num_samples_per_bit)
        bits = ''

        for i in range(num_bits):
            midpoint_idx = i * num_samples_per_bit + int(num_samples_per_bit / 2)
            sample_value = signal[midpoint_idx]
            bit = '1' if sample_value < 0 else '0'
            bits += bit

        bits = bits[self.preamble_length:] # remove the preamble
        
        return bits

encoder = ADSBEncoder()

starting_message = 'Hello!'
binary_message = ''.join(format(ord(i), '08b') for i in starting_message)

modulated_wave = encoder.modulate(binary_message)
noisy = modulated_wave + (np.random.normal(0, .1, len(modulated_wave)))

decoded_message = encoder.demodulate(modulated_wave)
noisy_decoded_message = encoder.demodulate(noisy)

print('Original message: ', binary_message)
print('Ideal decoded message: ', decoded_message)
print('Noisy decoded message: ', noisy_decoded_message)
print('Noisy message == original message?: ', noisy_decoded_message == binary_message)

plt.plot(modulated_wave[:800])
plt.plot(noisy[:800])
plt.show()
# unencoded_wave = encoder.unencoded_wave(binary_message)

# noisy = modulated_wave[:800] + (np.random.random(800) - .5)

# plt.plot(noisy)
# plt.plot(unencoded_wave[:800])
# plt.plot(noisy + unencoded_wave[:800])
# plt.show()
