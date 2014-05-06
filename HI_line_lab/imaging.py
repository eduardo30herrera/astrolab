import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sci
import scipy.constants as spc

data = np.load('data.npz')
L = data['longitude']
B = data['latitude']
spec = data['spectrum']
freq = data['freqs']

s = 20 #for pixel spacings between each point
img = np.zeros([1000,1000])
wt = np.zeros([1000,1000])
index = 0
for i in B:
    if i > -61.:        
        wt[(i+70)*999/60, (np.cos(i*np.pi/180)*(L[index]-190)*999/60+500)] += 1
        curr_spec = spec[index]
        img[(i+70)*999/60, (np.cos(i*np.pi/180)*(L[index]-190)*999/60+500)] = np.sum(curr_spec[np.where(curr_spec>1.8)])*1.8*10**18*(12000.0/(8192.0*4.73))
    index =index + 1

ker = np.arange(1000).repeat(1000).reshape(1000,1000).transpose()*1.

n = -1
#define the weights first here
for i in ker:
    n += 1
    m = 0
    for j in i:
        ker[n,m] = np.exp(-((n-500)**2+(m-500)**2)/(2.*s**2))
        m = m +1

img = sci.fftconvolve(img, ker, mode = 'same')
wt = sci.fftconvolve(wt, ker, mode = 'same')
img[np.where(wt < 0.001)] = 0
wt[np.where(wt < 0.001)] = 1
img_new = img/wt
#plt.imshow(wt, origin = 'lower', cmap = 'gist_earth', extent = (160,220,-70,-10))
#plt.colorbar()
#plt.show()
#d = # is in cm  
#m_h = spc.m_p + spc.m_e # in kilograms
#mass = (1.8*10**18*12000/(8192*4.73))*(d**2)*(m_h)*1000*np.sum(O*T_a)
#print mass
#print(m, 'this is the mass of the halo we were able to see') 
plt.imshow(img_new, origin ='lower', cmap = 'gist_earth', vmax = 2.0e21, extent = (160,220,-70,-10))
plt.title('Galactic Longitude (Degrees)\n\n', fontsize = 22)
plt.ylabel('Galactic Latitude (Degrees)', fontsize = 22)
plt.xlabel('Image of the Orion SuperBubble',  fontsize= 25)

b1 = np.linspace(-70, -10, 61)
x = np.array([]) 
for i in b1:
    x = np.append(x, (160-190)*np.cos(i*np.pi/180)+190)
plt.plot(x, b1,'k') 

b1 = np.linspace(-70, -10, 61)
x = np.array([]) 
for i in b1:
    x = np.append(x, (170-190)*np.cos(i*np.pi/180)+190)
plt.plot(x, b1,'k')

b1 = np.linspace(-70, -10, 61)
x = np.array([]) 
for i in b1:
    x = np.append(x, (180-190)*np.cos(i*np.pi/180)+190)
plt.plot(x, b1,'k')

b1 = np.linspace(-70, -10, 61)
x = np.array([]) 
for i in b1:
    x = np.append(x, (190-190)*np.cos(i*np.pi/180)+190)
plt.plot(x, b1,'k')

b1 = np.linspace(-70, -10, 61)
x = np.array([]) 
for i in b1:
    x = np.append(x, (200-190)*np.cos(i*np.pi/180)+190)
plt.plot(x, b1,'k')

b1 = np.linspace(-70, -10, 61)
x = np.array([]) 
for i in b1:
    x = np.append(x, (210-190)*np.cos(i*np.pi/180)+190)
plt.plot(x, b1,'k')

b1 = np.linspace(-70, -10, 61)
x = np.array([]) 
for i in b1:
    x = np.append(x, (220-190)*np.cos(i*np.pi/180)+190)
plt.plot(x, b1,'k')

plt.hlines([-10, -20, -30, -40, -50, -60], 160, 220, linestyles='solid')
plt.tick_params(axis='x',labelbottom='off',labeltop='on')
plt.xlim([160,220])
plt.ylim([-70,-10])
#cbar = figcolorbar(cax)
#cbar.set_label('H-1 Column Density (cm^2)', rotation =270)
plt.colorbar()
plt.show()
