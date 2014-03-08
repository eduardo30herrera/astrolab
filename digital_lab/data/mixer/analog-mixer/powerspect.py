# This code is for the pwere spectra of our two analog signals

import numpy as np
import matplotlib.pyplot as plt

for i in np.arange (1,3):
    N = 2048

    f = 200*10**6

    x = np.load('roach-lo-10MHz-0' +str(i) + '-numeric.npz')

    z = np.fft.fft(x['arr_1'][:2048])

    z_2 = np.abs(z)**2
    
    fqs = np.fft.fftfreq(N, (1./f))

    plt.subplot(1,2,i)

    plt.plot(np.fft.fftshift(fqs), np.fft.fftshift(z_2))

    plt.xlabel('frequency (in Hz)')
    plt.ylabel('Power in Watts')
    if i == 1:
        plt.title('Power Spectrum of $v_{sig} = v_{lo}+\delta v$')
    if i == 2:
        plt.title('Power Spectrum of $v_{sig} = v_{lo}-\delta v$')

plt.tight_layout()
plt.show() 
