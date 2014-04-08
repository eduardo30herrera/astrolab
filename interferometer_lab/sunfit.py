import numpy as np 
import matplotlib.pyplot as plt

#for this code, we will attempt to use the Fringe amplitude equation to obtain a best fit line for the sun
#all angles will be treated as radians in this code
f = np.load('sun-4_3_2014-22.npz')

x = (2./24)*np.pi*(f['lst']-f['ra']) # changing to radians via 2pi/24, this is also the hour angle
x = x[1700:3300]
y = f['volts'] - np.mean(f['volts']) #to partially take care of the DC offset
q = f['dec'] #fix to be q[radians 
q = q[1700:3300]
B = 10
c = 3*10**8
v = 1.067*10**10
l = c/v
Y = y[1700:3300]-np.mean(y[1700:3300])
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
plt.title('least Squares Fitting for Sun Data',fontsize =16)
plt.show()

#Now we take the lowest phi, p that we got and use it
p = Pmin
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

#YBAR = np.dot(a, X)
YBAR = np.dot(-1.*a, X)
#DELY = YBAR - Y



lst = f['lst'][1700:3300]
alp = f['ra'][1700:3300]
dec = f['dec'][1700:3300]
a_m = np.argmin(YBAR)
print lst[a_m]-alp[a_m]
print dec[a_m]

min_val = list(YBAR).index(np.min(YBAR))



s_sq = np.append(s_sq, np.sum((DELY)**2))

plt.plot(Y)
#plt.plot(YBAR) #this shows the envelope around the parabolic region
plt.plot(YBAR) #so does this one
plt.xlabel('time in seconds', fontsize =14)
plt.ylabel('power proportional to V^2',fontsize = 14)
plt.title('Envelope of the Sun data', fontsize =16)
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
plt.xlabel('Rf')
plt.ylabel('MF')
plt.title('looking for zeros')
plt.show()

