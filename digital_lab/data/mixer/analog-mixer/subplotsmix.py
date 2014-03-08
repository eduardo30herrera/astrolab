# here we plot the mixed signals for + and - delta v

import numpy as np
import matplotlib.pyplot as plt

for i in np.arange(1,3):
    x = np.load('roach-lo-10MHz-0' + str(i) + '-numeric.npz')

    plt.subplot(1,2,i)
    plt.plot(x['arr_1'][:1000])

    plt.xlabel('time')
    plt.ylabel('Voltage')
    if i == 1:
        plt.title('$v_{sig} = v_{lo} + \delta v$')
    if i == 2:
        plt.title('$v_{sig} = v_{lo} - \delta v$')

    
plt.tight_layout()
plt.show()
