import numpy as np
import matplotlib.pyplot as plt

global frequency_scale
frequency_scale = 1000

class Emitter: 
    def __init__(self, 
                 frequency: int, 
                 bit_rate: int, 
                 sample_rate: int,
                 position: np.ndarray,
                 velocity: np.ndarray):
        self.bit_rate = bit_rate / frequency_scale
        self.frequency = frequency / frequency_scale
        self.sample_rate = 20 * self.frequency # 20 samples per cycle for continuous effect when emitting
        self.position = position
        self.velocity = velocity

        self.preamble = '101000010100000'
        self.modulator = {'0' : lambda x : np.cos((2 * np.pi * self.frequency * x + np.pi)),
                          '1' : lambda x : np.cos((2 * np.pi * self.frequency * x))}

    def generate_signal(self, bits):
        bits = self.preamble + bits
        num_samples = int(self.sample_rate / self.bit_rate)
        bit_duration = 1 / self.bit_rate
        
        signal = np.array([])

        for i, bit in enumerate(bits):
            sample_times = np.linspace(i * bit_duration, (i + 1)*bit_duration, num_samples, endpoint=False)
            samples = self.modulator[bit](sample_times)
            signal = np.concatenate((signal, samples))

        time_values = np.linspace(0, len(signal) / self.sample_rate, len(signal))

        return signal, time_values
    
class Receiver:
    def __init__(self, 
                 carrier_frequency: int,
                 sample_rate: int, 
                 position: np.ndarray):
        # info about emitter to sample accurately
        self.carrier_frequency = carrier_frequency / frequency_scale
        self.carrier_rate = 20 * self.carrier_frequency

        self.sample_rate = sample_rate / frequency_scale

        self.position = position

    def collect_signal(self, signal, times):
        signal_time = len(signal) / self.carrier_rate

        sampling_interval = int(self.carrier_rate / self.sample_rate)

        sampled_signal = signal[::sampling_interval]
        sampled_times = times[::sampling_interval]

        return sampled_signal
    
def channel(signal: np.ndarray, 
            times: np.ndarray, 
            emitter: Emitter, 
            receiver: Receiver):
    
    c = 299792458.0

    # Calculate and apply doppler shifts 
    f0 = emitter.frequency
    assert emitter.position.shape == receiver.position.shape
    distance = np.linalg.norm(emitter.position - receiver.position)
    f1 = f0 * (c / (c - (np.dot(emitter.velocity, receiver.position - emitter.position) / distance)))
    doppler_ratio = f1 / f0
    times = times / doppler_ratio

    # apply time shift, signal arrives at receiver at t=d/c
    time_shift = distance / c
    times = times + time_shift

    # add noise according to distance
    noise_var = signal_to_noise_ratio(signal, distance)
    noise = np.random.normal(0, noise_var, len(signal))
    signal = signal + noise

    return signal, times
    
def signal_to_noise_ratio(signal: np.ndarray,
                          distance: float):
    signal_power = np.sum(np.abs(signal)**2) / len(signal)

    snr_from_distance = lambda x : 17 / (1 + np.exp(.05 * (x / 1000) - 3)) + .999

    snr = snr_from_distance(distance)

    noise_var = signal_power / snr
    return noise_var


def main():
    emitter_pos = np.array([0, 0, 0])
    emitter_vel = np.array([1, 0, 0])
    receiver_pos = np.array([400000, 0, 0])
    emitter = Emitter(1090e6, 1e8, 1e8, emitter_pos, emitter_vel)
    receiver = Receiver(1090e6, 2180e6, receiver_pos)
    
    signal, times = emitter.generate_signal('1010')
    signal, times = channel(signal, times, emitter, receiver)
    sampled_signal = receiver.collect_signal(signal, times)


if __name__ == '__main__':
    main()