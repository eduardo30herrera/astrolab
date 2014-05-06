#code run on our test data to do whatever the hell we needed to do to it, oh yeah, cleaning it.
import numpy as np
import matplotlib.pyplot as plt
import readspec_mod as rsm
import scipy.constants as spc

n_off = rsm.readSpec('test_220_0_noise_off0.log') #noise on data
n_on = rsm.readSpec('test_220_0_noise_on0.log') #noise off data
#n_off_lo = 
#n_on_lo = 
index = [] 
value = 0
x = x - x[0] 
fc = 1272.4+150
f_range = np.linspace(fc-6, fc+6, n_off.shape[0])
radius = 100
#x_mean = average(x, y) 
x_avg = n_off[100:-100] - x_mean

for i in range (x_avg.size):
    if i == len(x_avg):
        break
    if x_avg[i] < -.0023: #a placeholder number
        index.append(i+100)
    if y_avg[i] > .0023:
        index.append(i+100)

d = np.delete(x, index)
#y = np.delete(y, index)

def boxcar(array, radius): #here we take the average of the data in order to clean it
    radius = 100
    n = 0 #or 100?
    new = np.array([]) #a different name for 'new'  may be needed
    for i in array[radius, -radius]:
        new = np.append(new, np.mean(array[n-radius:n+radius]))
        n = n+1
    return new

def avg_graph(data1, data2):
    radius = 100
    n = 100 #different?
    y_mean = average (data1, data2)
    plt.plot(data1, data2, linewidth=1, color='b')
    plt.plot(data1[radius:-radius], y_mean, linewidth=2, color='r')
    #plt.xlabel('Time (s)', fontsize =18)
    #plt.ylabel('Power', fontsize = 18)
    
#this part will serve to remove the bad data points
index = [] 
for i in range (n_off.size): #this filename can/will change
    if i == len(n_off):
        break
    if x_data[i] >3326 and x_data[i] <3373:
        index.append(i)
    if x_data[i] >6732 and x_data[i] <6853:
        index.append(i)
    #reapeat the above for as many time necessary    
    if x_data[i] > 18.373 and x_data[i]<17.63:
        index.append(i)
    if x_data[i] > 31.85 and x_data[i]< 30.256:
        index.append(i)
    if x_data[i]>29.05 and x_data[i]<27.85:
        index.append(i)
    
        
plt.plot(f_range, new)
#plt.plot(f_range, new2) #together we will see the data cleaned of those spikes, therefore making it easier to take data
plt.title('title') #tentative titles
plt.xlabel('x')
plt.ylabel('y')
#plt.show()
