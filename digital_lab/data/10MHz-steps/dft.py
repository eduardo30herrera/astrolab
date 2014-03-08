#This code is to show the DFTs of our data at the sample rate of 10 MHz

import numpy as np
import matplotlib.pyplot as plt

for i in np.arange (1,10):

    N = 256

    f = 10**6
    
    x = np.load('signal-' +str(i) + '.npz')
    
    z = np.fft.fft(x['arr_1'][:256])

    z_2 = np.abs(z)**2

    fqs = np.fft.fftfreq(N, (1./f)*10**3)

    plt.subplot(3,3,i)

    plt.plot(np.fft.fftshift(fqs), np.fft.fftshift(z_2))
    
    plt.xlabel('frequency in kHz')
    plt.ylabel('power in Watts')
    plt.title('P.S. of $V_{sig} = .'+ str(i) + 'V_{samp}$')

plt.tight_layout()
plt.show()
