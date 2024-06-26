import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import ZoomFFT, firwin
from scipy import signal, linalg


def caf(signal1, signal2, max_time_shift, max_freq_shift, freq_count = 51):
    assert len(signal1) == len(signal2), "Signals must be the same length"

    time_shifts = np.arange(0, max_time_shift + 1)
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
    return np.abs(caf_values[max_ind]), -time_shift, freq_shift, caf_values

def fftconvolve(sig1,sig2,freq_shift=0):
    tmp1 = np.empty_like(sig1); tmp2 = np.empty_like(sig2)
    pad_size = np.abs(len(sig2) - len(sig1))
    if len(sig2) > len(sig1):
        tmp1 = np.hstack((sig1,np.zeros(pad_size)))
    elif len(sig1) > len(sig2):
        tmp2 = np.hstack((sig2,np.zeros(pad_size)))

    tmp1 = np.hstack((sig1,np.zeros(sig2.size)))
    tmp2 = np.hstack((sig2,np.zeros(sig1.size)))
    S1 = np.fft.fftshift(np.fft.fft(tmp1))
    S2 = np.fft.fftshift(np.fft.fft(tmp2))
    S1 = np.roll(S1,int(np.round(freq_shift*sig1.size)))
    return np.fft.ifft(np.fft.ifftshift(S1*S2))

def corner_turn_caf(signal1, signal2, max_time_shift, max_freq_shift, num_freqs = 51):
    
    delays = np.arange(0, max_time_shift)
    freqs = np.linspace(-max_freq_shift, max_freq_shift, num_freqs)
    
    filt_len = 100
    t = np.arange(filt_len)
    fc = 0.5
    filt = fc / (2*np.pi)*np.sinc(fc * (t - filt_len // 2) / 2)
    win = signal.windows.bartlett(filt_len)
    filt = filt * win

    L = int(1/fc)
    R = len(signal1) // L
    delay_len = len(delays)
    vjr = np.zeros((delay_len, R), dtype=complex)

    for r in range(R):
        fr = filt * signal1.take(np.arange(r*L - filt_len//2, r*L + filt_len//2, 1),mode='wrap')
        gr = np.conj( signal2.take(np.arange(r*L + delay_len//2, r*L - delay_len//2, -1),mode='wrap') )

        vjr[:,r] = fftconvolve(fr, gr)[filt_len//2:-1*filt_len//2]

    caf = np.fft.fftshift(np.fft.fft(vjr, axis=1), axes=1)
    caf = caf.T
    max_ind = np.unravel_index(np.argmax(np.abs(caf)), caf.shape)
    print(caf.shape)
    print(len(freqs))
    print(len(delays))
    time_shift  = delays[max_ind[1]]
    freq_shift = freqs[max_ind[0]]
    
    plt.imshow(np.abs(caf), aspect=vjr.shape[0]/vjr.shape[1])
    plt.show()

    return caf, time_shift, freq_shift


# def corner_turn_caf(signal1, signal2, max_time_shift, max_freq_shift, sampling_freq = 2, num_freqs = 51):
#     '''
#     corner turn caf

#     Parameters

#         signal1: np.ndarray, first signal
#         signal2: np.ndarray, second signal
#         max_time_shift: int, maximum time shift
#         max_freq_shift: float, maximum frequency shift
#         sampling_freq: float, sampling frequency - if sampling freq is 10kHz then max_freq_shift must be in kHz
#     '''
#     assert len(signal1) == len(signal2), "Signals must be the same length"

#     K = len(signal1)
#     R = 2 * max_freq_shift + 1
#     L = int(K / R)
    
#     print(K)
#     print(L, R)
    
#     time_shifts = np.arange(0, max_time_shift + 1)
#     freq_shifts = np.linspace(-max_freq_shift, max_freq_shift, num_freqs)

#     zoom_fft = ZoomFFT(R, [-max_freq_shift, max_freq_shift], fs = sampling_freq)
  
#     cutoff = 1/L
#     num_coeffs = 100
#     fir_filter = firwin(num_coeffs, cutoff, pass_zero="lowpass")

   
#     v = np.zeros(len(time_shifts), R)
#     F = np.zeros(R)
#     G = np.zeros(R)
    
#     for r in range(R):
#         F[r] = np.array([fir_filter[m] * signal1[r*L - m] for m in range(num_coeffs)])
#         G[r] = np.array([signal2[r*L - j] for j in time_shifts])
    
#     for r in range(R):
#         v[:,r] = np.convolve(F[r], G[r], mode= 'same')

#     caf_vals = np.zeros( (len(time_shifts), len(freq_shifts)), dtype=complex)
#     for r in range(R):
#         caf_vals[:, r] = zoom_fft(v[:, r])

#     return caf_vals


def test_corner_turn_caf():
    sig1 = np.random.randn(1024) + 1j * np.random.randn(1024)
    caf, time_shift, freq_shift = corner_turn_caf(sig1, sig1, 10, 100)
    
    print(time_shift, freq_shift)


def test_caf():
    sig1 = np.random.randn(1024) + 1j * np.random.randn(1024)
    
    caf_peak, tshift, fshift, caf_out1= caf(sig1, sig1, 10, .5)
    print(tshift, fshift)

    sig2 = np.roll(sig1, 2)

    caf_peak, tshift, fshift, caf_out2= caf(sig1, sig2, 10, .5)
    print(tshift, fshift)

    sig3 = sig1 *  np.exp(1j * 2 * np.pi * .1 * np.arange(len(sig2)))

    caf_peak, tshift, fshift, caf_out3= caf(sig1, sig3, 10, .5)
    print(tshift, fshift)

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

if __name__ == '__main__':
    test_corner_turn_caf()