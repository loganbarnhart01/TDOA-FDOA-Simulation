import numpy as np
import matplotlib.pyplot as plt

#TODO: 
# implement correlation techniques / matched filtering to 
# let receiver recognize when it gets a signal it's looking for

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
        # # modulate using real valued BPSK
        # self.modulator = {'0': lambda x : np.cos(2*np.pi*freq * x + np.pi), 
        #                   '1': lambda x : np.cos(2*np.pi*freq * x)}
        # modulate using complex valued BPSK
        self.modulator = {'0' : lambda x : np.exp(1j * 2 * np.pi * self.freq * x + np.pi),
                          '1' : lambda x : np.exp(1j * 2 * np.pi * self.freq * x)}
        self.demodulator = lambda x : np.arccos(x) / (2 * np.pi * freq)


    def modulate(self, bits, noisy=False, time_delay=0):
        '''
            Modulates a signal and simulates a time delay until the actual signal starts, can add noise if desired
            bits: string of bits to modulate
            noisy: whether or not to add noise to the signal
            time_delay: time delay in seconds to simulate before the actual signal starts
        '''
        bits = self.preamble + bits
        num_samples = int(self.sample_rate * self.bit_duration)
        signal = np.array([])
        for i, bit in enumerate(bits):
            sample_times = np.linspace(0, self.period, num_samples, endpoint=False)
            samples = self.modulator[bit](sample_times)
            signal = np.concatenate((signal, samples))

        # add a time delay to the signal

        time_delay_samples = int(time_delay * self.sample_rate)
        signal = np.concatenate((np.zeros(time_delay_samples), signal))

        if noisy:
            signal += np.random.normal(0, .1, len(signal))

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
    
    def find_signal_start(self, receiver_signal):
        preamble_signal = self.modulate('', noisy=True)
        correlation = np.correlate(receiver_signal, preamble_signal, mode='full')
        return np.argmax(correlation), correlation

