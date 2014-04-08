import numpy as np 
import matplotlib.pyplot as plt

def msmooth(air, width): #air is the signal that we smooth
    array = np.array(air) #making a deep copy
    for i in range(width, len(air)-width): #this takes care of the regions where no data exists by ignoring them
        array[i]= np.median(air[i-width:i+width])
    return array

##for this code, we will attempt to use the Fringe amplitude equation to obtain a best fit declination for the crab nebula
##all angles will be treated as radians in this code
f = np.load('3C144-4_3_2014-23.npz')

x = f['lst']-5.576 #right ascension is in hours which must be changed to radians
y = f['volts']

#A = np.cos(2*np.pi*v*t) these (A&B) won't be used because they are what we are fitting for!
#B = np.sin(2*np.pi*v*t) see above comment ^
#now we have to make a guess about what the value of (B/l)*np.cos(q) is as well as adopt a value for r (the right ascension (alpha))
# we have to make guesses for q now.
B = 10 #here we assume the baseline to be 10 meters
c = 3*10**8 #in meters per second
v = 1.067*10**10 #in reciprical seconds
l = c/v #our wavelength
#C = [2*np.pi*(B/l)*np.cos(q)]
Y = y - msmooth(y,75) #this removes the DC offset
Y = Y[75:-75]
x = x[75:-75]
s_sq = []
guess = np.linspace(19,24,120)
for q in guess:
    X = np.empty([2.0, len(x)])
    X[0,:] = np.cos(2*np.pi*B/l*np.cos(q)*np.sin((2./24)*np.pi*(x)))
    X[1,:] = np.sin(2*np.pi*B/l*np.cos(q)*np.sin((2./24)*np.pi*(x)))
    XX = np.dot(X, np.transpose(X))
    XY = np.dot(Y, np.transpose(X))
    XXI = np.linalg.inv(XX)
    a  = np.dot(XXI,XY) #our coeffs
    YBAR = np.dot(a,X)
    DELY = YBAR - Y
    s_sq = np.append(s_sq, np.sum(DELY**2))

dex = np.argmin(s_sq)
Dmin = guess[dex] 
plt.plot(guess, s_sq)
plt.xlabel('The Guessed Declination (in radians)',fontsize= 14)
plt.ylabel('Residuals $\chi^2$',fontsize = 14)
plt.title('Least Squares Approximation for Our Declination',fontsize = 16)
