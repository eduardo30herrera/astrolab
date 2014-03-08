#This code is to take our data regarding nyquist sampling and plot it as a function of voltage and time

import numpy as np
import matplotlib.pyplot as plt

for x in np.arange(1,10): 

    a = np.load('signal-' + str(x) + '.npz')

    plt.subplot(3,3,x)
    plt.plot(a['arr_1'][:20], '-*')
             
    plt.xlabel('time (in .1 microseconds)')
    plt.ylabel('sampled signal amplitude')
    plt.title('$V_{sig} = .'+ str(x) + '*V_{sample}$')

plt.tight_layout()   
plt.show()
