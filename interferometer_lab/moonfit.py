import numpy as np 
import matplotlib.pyplot as plt

def msmooth(air, width): #air is the signal that we smooth
    array = np.array(air) #making a deep copy
    for i in range(width, len(air)-width): #this takes care of the regions where no data exists by ignoring them
        array[i]= np.median(air[i-width:i+width])
    return array
#for this code, we will attempt to use the Fringe amplitude equation to obtain a best fit line for the moon
#all angles will be treated as radians in this code
f = np.load('moon-4_6_2014-24.npz')

x = (2./24)*np.pi*(f['lst']-f['ra']) # changing to radians via 2pi/24, this is also the hour angle
x = x[6200:6360]
y = f['volts'] - np.mean(f['volts']) #to partially take care of the DC offset
q = f['dec'] #fix to be radians 
q = q[6200:6360]
B = 10
c = 3*10**8
v = 1.067*10**10
l = c/v
Y = y[6200:6360]-np.mean(y[6200:6360])
s_sq = []
guess = np.linspace(0, np.pi, 100)
for p in guess: 
    X = np.empty([3.0, len(x)])
    X[0,:] = np.cos(2*np.pi*(B/l)*np.cos((2./360)*np.pi*q)*np.sin(x) + p)
    X[1,:] = x*np.cos(2*np.pi*(B/l)*np.cos((2./360)*np.pi*q)*np.sin(x) + p)
    X[2,:] = x**2*np.cos(2*np.pi*(B/l)*np.cos((2./360)*np.pi*q)*np.sin(x) + p)

    XX = np.dot(X, np.transpose(X))
    XY = np.dot(Y, np.transpose(X))
    XXI = np.linalg.inv(XX)
    a = np.dot(XXI, XY)
    YBAR = np.dot(a, X)
    DELY = YBAR - Y
    #s_sq = np.sum((Y-YBAR)**2)
    s_sq = np.append(s_sq, np.sum((DELY)**2))

dex = np.argmin(s_sq)
Pmin = guess[dex]
plt.plot(guess, s_sq)
plt.xlabel('value of $\phi$ (in radians)', fontsize = 14)
plt.ylabel('value of $\chi^2$', fontsize =14)
plt.title('guessed values $\phi$')
plt.show()

plt.plot(Y)
plt.plot(YBAR)
plt.xlabel('time in seconds', fontsize = 14)
plt.ylabel('power proportional to V^2', fontsize =14)
plt.title('least Squares Fitting for moon Data',fontsize =16)
plt.show()

#Now we take the lowest phi, p that we got and use it
p = 2.7925268
X = np.empty([3.0, len(x)])
X[0,:] = np.cos(2*np.pi*(B/l)*np.cos((2./360)*np.pi*q)*np.sin(x) + p)
X[1,:] = x*np.cos(2*np.pi*(B/l)*np.cos((2./360)*np.pi*q)*np.sin(x) + p)
X[2,:] = x**2*np.cos(2*np.pi*(B/l)*np.cos((2./360)*np.pi*q)*np.sin(x) + p)
XX = np.dot(X, np.transpose(X))
XY = np.dot(Y, np.transpose(X))
XXI = np.linalg.inv(XX)
a = np.dot(XXI, XY)
X[0,:] = 1
X[1,:] = x
X[2,:] = x**2

YBAR = np.dot(a, X)
#YBAR2 = np.dot(-1.*a, X)
DELY = YBAR - Y

#min_val = list(YBAR).index(np.min(YBAR))

s_sq = np.append(s_sq, np.sum((DELY)**2))

plt.plot(Y)
plt.plot(YBAR) #this shows the envelope around the parabolic region
#plt.plot(YBAR2) #so does this one
plt.xlabel('time in seconds', fontsize =14)
plt.ylabel('power proportional to V^2',fontsize = 14)
plt.title('Envelope of the moon data', fontsize =16)
plt.show()
#####################
#Code to find R
N = 1000.
#fR =((B/l)*np.cos(q[1599]))*np.cos(x[1599])*R #x is the hour angle
fR = np.linspace(-4,4, 10000)
MF = np.empty(10000) 
for n in np.arange(-N,N+1):
   MF+= np.sqrt([1-(n/N)**2])*np.cos(2*np.pi*fR*n/N)   
plt.plot(fR, MF)
plt.plot([-4,4],[0,0])
plt.show()
