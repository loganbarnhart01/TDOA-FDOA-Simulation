import numpy as np
import matplotlib.pyplot as plt

def caf(signal1, signal2, max_time_shift, max_freq_shift, freq_count = 51):
    assert len(signal1) == len(signal2), "Signals must be the same length"

    time_shifts = np.arange(-max_time_shift, max_time_shift + 1)
    freq_shifts = np.linspace(-max_freq_shift, max_freq_shift, freq_count)
    caf_values = np.zeros((len(time_shifts), len(freq_shifts)), dtype=complex)
    for i, t in enumerate(time_shifts):
        for j, f in enumerate(freq_shifts):
            signal1_shifted = np.roll(signal1, t) * np.exp(2j * np.pi * f * np.arange(len(signal1)))
            caf_values[i, j] = signal1_shifted @ signal2.conj()
    caf_values = caf_values.T
    max_ind = np.unravel_index(np.argmax(np.abs(caf_values)), caf_values.shape)
    time_shift  = time_shifts[max_ind[1]]
    freq_shift = freq_shifts[max_ind[0]]
    return caf_values[max_ind], -time_shift, freq_shift,caf_values

def test_caf():
    sig1 = np.random.randn(1024) + 1j * np.random.randn(1024)
    
    caf_peak, _, _ , caf_out1= caf(sig1, sig1, 10, .5)

    sig2 = np.roll(sig1, 2)

    caf_peak, _, _ , caf_out2= caf(sig1, sig2, 10, .5)

    sig3 = sig1 *  np.exp(1j * 2 * np.pi * .1 * np.arange(len(sig2)))

    caf_peak, _, _ , caf_out3= caf(sig1, sig3, 10, .5)

    plt.subplot(2,2,1)
    plt.imshow(np.abs(caf_out1), origin='lower', aspect = 'auto')
    plt.xlabel("time")
    plt.ylabel("frequency")
    plt.subplot(2,2,3)
    plt.imshow(np.abs(caf_out2), origin='lower', aspect = 'auto')
    plt.xlabel("time")
    plt.ylabel("frequency")
    plt.subplot(2,2,2)
    plt.imshow(np.abs(caf_out3), origin='lower', aspect = 'auto')
    plt.xlabel("time")
    plt.ylabel("frequency")
    plt.show()

# if __name__ == '__main__':
#     test_caf()