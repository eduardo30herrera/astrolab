import numpy as np
import matplotlib.pyplot as plt

f = np.load('ay121_lsq_data.npz')

x=f['x']
y=f['y']

Y= y
X = np.empty([1000.0, 2.0])
X[:,0]= np.ones(1000)
X[:,1] = x
#X[:,2] =

 


XX = np.dot(np.transpose(X),X)
XY = np.dot(np.transpose(X),Y)
XXI = np.linalg.inv(XX)
a = np.dot(XXI,XY)
YBAR =np.dot(X,a)
DELY = Y - YBAR
s_sq = np.dot(np.transpose(DELY),DELY/(1000-2))
#diag_elems = np.dot(np.identity(2),2by2_matrix)
#vardc = s_sq*diag_elems


plt.plot(f['x'], YBAR)
plt.plot(f['x'], f['y'], '.')
plt.plot(f['x'], DELY, 'k.')
plt.show()