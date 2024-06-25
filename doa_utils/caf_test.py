import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import ZoomFFT, firwin, fftconvolve
from scipy import signal, linalg
from matplotlib.colors import LightSource
from matplotlib import cm


def naive_caf(sig1, sig2, max_time_shift, max_freq_shift, num_freqs = 51):
    assert len(sig1) == len(sig2), "Signals must be the same length."
    
    K = len(sig1)

    time_shifts = np.arange(-max_time_shift, max_time_shift + 1)
    freq_shifts = np.linspace(-max_freq_shift, max_freq_shift, num_freqs) / K

    print(time_shifts)
    print(freq_shifts)

    caf_out = np.zeros((len(freq_shifts), len(time_shifts)), dtype = np.complex128)

    for i, tshift in enumerate(time_shifts):
        for j, fshift in enumerate(freq_shifts):
            sig2_shifted = np.roll(sig2, tshift).conj()
            caf = sig1 * sig2_shifted * np.exp(-2j * np.pi * fshift * np.arange(K))
            caf_out[j, i] = np.sum(caf)

    max_ind = np.unravel_index(np.argmax(np.abs(caf_out)), caf_out.shape)
    time_shift  = time_shifts[max_ind[1]]
    freq_shift = freq_shifts[max_ind[0]]

    return caf_out, time_shift, freq_shift

def fft_caf(sig1, sig2, max_time_shift):
    assert len(sig1) == len(sig2), "Signals must be the same length."

    K = len(sig1)
    time_shifts = np.arange(-max_time_shift, max_time_shift + 1)
    
    caf_out = np.zeros((K, len(time_shifts)), dtype = np.complex128)

    for i, tshift in enumerate(time_shifts):
        sig2_shifted = np.roll(sig2, tshift).conj()
        caf = np.fft.fft(sig1 * sig2_shifted)
        caf_out[:, i] = caf
    
    max_ind = np.unravel_index(np.argmax(np.abs(caf_out)), caf_out.shape)
    time_shift  = time_shifts[max_ind[1]]
    freq_shift = max_ind[0] / K

    max_mag = np.max(np.abs(caf_out))
    median_mag = np.median(np.abs(caf_out))

    return caf_out, time_shift, freq_shift, max_mag, median_mag

def convolution_caf(sig1, sig2, num_freq_shifts = 51):
    assert len(sig1) == len(sig2), "Signals must be the same length."

    K = len(sig1)

    freq_sig1 = np.fft.fft(sig1)
    freq_sig2 = np.fft.fft(sig2)
    freq_sig2_conj = freq_sig2.conj()

    caf_out = np.zeros((K, num_freq_shifts), dtype = np.complex128)

    for i in range(num_freq_shifts):
        sig1_shifted = freq_sig1
        sig2_shifted = np.roll(freq_sig2_conj, i)
        caf = np.fft.ifft(sig1_shifted * sig2_shifted)
        caf_out[:, i] = caf

    max_ind = np.unravel_index(np.argmax(np.abs(caf_out)), caf_out.shape)

    print(max_ind)

    time_shift  = K - max_ind[0]
    freq_shift = max_ind[1] / K

    max_mag = np.max(np.abs(caf_out))
    median_mag = np.median(np.abs(caf_out))

    print(time_shift, freq_shift)
    print(max_mag, median_mag)

    return caf_out, time_shift, freq_shift, max_mag, median_mag



def test_caf():
    sig1 = np.random.randn(1024) + 1j * np.random.randn(1024)

    # caf_out1, tshift1, fshift1, max_mag, median_mag = convolution_caf(sig1, sig1, 100)
    # print(tshift1, fshift1, max_mag, median_mag)

    # sig2 = np.roll(sig1, 8)

    # caf, _, _, _, _ = convolution_caf(sig1, sig2)

    # caf_out2, tshift2, fshift2, max_mag, median_mag = fft_caf(sig1, sig2, 10)
    # print(tshift2, fshift2, max_mag, median_mag)

    sig3 = sig1 *  np.exp(1j * 2 * np.pi * .1 * np.arange(len(sig1)))

    convolution_caf(sig1, sig3, 1000)

    # caf_out3, tshift3, fshift3, max_mag, median_mag = fft_caf(sig1, sig3, 100)
    # print(tshift3, fshift3, max_mag, median_mag)

    # sig4 = np.roll(sig3, 2)
    # caf_out4, tshift4, fshift4, max_mag, median_mag = fft_caf(sig1, sig4, 100)
    # print(tshift4, fshift4, max_mag, median_mag)


    # plt.subplot(2,2,1)
    # plt.imshow(np.abs(caf_out1), origin='lower', aspect = 'auto', extent=[-10, 10, -10/1024, 10/1024])
    # plt.xlabel("time")
    # plt.ylabel("frequency")
    # plt.title("No shift")
    # plt.subplot(2,2,3)
    # plt.imshow(np.abs(caf_out2), origin='lower', aspect = 'auto', extent=[-10, 10, -10/1024, 10/1024])
    # plt.title("2 sample shift")
    # plt.xlabel("time")
    # plt.ylabel("frequency")
    # plt.subplot(2,2,2)
    # plt.imshow(np.abs(caf_out3), origin='lower', aspect = 'auto', extent=[-10, 10, -1000/1024, 1000/1024])
    # plt.title(".1 freq shift")
    # plt.xlabel("time")
    # plt.ylabel("frequency")
    # plt.show()

if __name__ == '__main__':
    test_caf()