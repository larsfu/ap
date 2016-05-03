import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

(x,y)=np.genfromtxt('b1.txt', unpack=True)
(x1,y1)=np.genfromtxt('b2.txt', unpack=True)
(x2,y2)=np.genfromtxt('b3.txt', unpack=True)

def f(x,a,b):
    return a*x+b
params,covariance = curve_fit(f,x,y)
errors = np.sqrt(np.diag(covariance))
print ('a=',params[0], '±', errors[0])
print ('b=',params[1],'±', errors [1])
plt.plot(x,y,'rx',label="Messwerte für $U_\mathrm{B}=250V$")
plt.plot(x,f(x, *params),'r-')

def f(x1,a,b):
    return a*x1+b
params,covariance = curve_fit(f,x1,y1)
errors = np.sqrt(np.diag(covariance))
print ('a=',params[0], '±', errors[0])
print ('b=',params[1],'±', errors [1])

plt.plot(x1,y,'mx',label="Messwerte für $U_\mathrm{B}=300V$")
plt.plot(x1,f(x1, *params), 'm-')

def f(x2,c,d):
    return c*x2+d
params,covariance = curve_fit(f,x2,y2)
errors = np.sqrt(np.diag(covariance))
print ('c=',params[0], '±', errors[0])
print ('d=',params[1],'±', errors [1])
plt.plot(x2,y, 'gx', label="Messwerte für $U_\mathrm{B}=350V$")
plt.plot(x2,f(x2, *params), 'g-')




plt.xlabel('$B/mT$')
plt.ylabel(r'$\frac{D}{L^2+D^2}/\frac{1}{m}$')
plt.legend(loc='best')
plt.savefig('502-a.pdf')
