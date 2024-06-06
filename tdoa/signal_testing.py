import numpy as np
import matplotlib.pyplot as plt
from signal_generator import ADSBEncoder


def main():
    encoder = ADSBEncoder()

    flag = 'test_tdoa'

    starting_message = 'Hello!'
    binary_message = ''.join(format(ord(i), '08b') for i in starting_message)

    if flag == 'test_mod_demod':
    
        modulated_wave = encoder.modulate(binary_message)
        noisy = modulated_wave + (np.random.normal(0, .1, len(modulated_wave)))

        decoded_message = encoder.demodulate(modulated_wave)
        noisy_decoded_message = encoder.demodulate(noisy)

        print('Original message: ', binary_message)
        print('Ideal decoded message: ', decoded_message)
        print('Noisy decoded message: ', noisy_decoded_message)
        print('Noisy message == original message?: ', noisy_decoded_message == binary_message)

        fig, ax = plt.subplots(3, 1)
        ax[0].plot(modulated_wave[:800], label = 'mod-no-noise', color = 'red')
        ax[1].plot(noisy[:800], label = 'mod-noisy', color = 'blue')
        ax[2].plot(noisy, label = 'full-signal', color= 'green')

        labels = [line.get_label() for axs in ax for line in axs.get_lines()]
        handles = [line for axs in ax for line in axs.get_lines()]
        fig.legend(handles, labels, loc='lower center', ncol=3)

        plt.tight_layout(rect = [0, 0.1, 1, 1])
        plt.show()

    if flag == "test_tdoa":
        receiver1_delay = np.random.uniform(0, 1e-4)
        receiver2_delay = np.random.uniform(0, 1e-4)

        true_delay = receiver2_delay - receiver1_delay

        receiver1_signal = encoder.modulate(binary_message, noisy=True, time_delay=receiver1_delay)
        receiver2_signal = encoder.modulate(binary_message, noisy=True, time_delay=receiver2_delay)

        receiver1_start, receiver1_correlation = encoder.find_signal_start(receiver1_signal)
        receiver2_start, receiver2_correlation = encoder.find_signal_start(receiver2_signal)

        estimated_delay = (receiver2_start - receiver1_start) / encoder.sample_rate

        print(f"True delay: {true_delay}, \nEstimated delay: {estimated_delay}, \nError: {true_delay - estimated_delay}")

        fig, ax = plt.subplots(5, 1)
        ax[0].plot(receiver1_correlation, label = 'receiver1-correlation', color = 'red')
        ax[1].plot(receiver2_correlation, label = 'receiver2-correlation', color = 'blue')
        ax[2].plot(receiver1_signal, label = 'receiver1-signal', color = 'green')
        ax[3].plot(receiver2_signal, label = 'receiver2-signal', color = 'orange')
        ax[4].plot(receiver1_signal[receiver1_start:], color = 'purple')
        ax[4].plot(receiver2_signal[receiver2_start:], label= 'aligned-signals', color = 'pink')

        labels = [line.get_label() for axs in ax for line in axs.get_lines()]
        handles = [line for axs in ax for line in axs.get_lines()]
        fig.legend(handles, labels, loc='lower center', ncol=3)

        plt.tight_layout(rect = [0, 0.1, 1, 1])
        plt.show()

if __name__ == "__main__":
    main()