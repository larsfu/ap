import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

(x,y)=np.genfromtxt('b4.txt', unpack=True)
(x1,y1)=np.genfromtxt('b5.txt', unpack=True)
#(x2,y2)=np.genfromtxt('b6.txt', unpack=True)

def f(x,a,b):
    return a*x+b
params,covariance = curve_fit(f,x,y)
errors = np.sqrt(np.diag(covariance))
print ('a=',params[0], '±', errors[0])
print ('b=',params[1],'±', errors [1])
plt.plot(x,y,'kx',label="Messwerte für $U_\mathrm{B}=400V$")
plt.plot(x,f(x, *params),'k-')

def f(x1,a,b):
    return a*x1+b
params,covariance = curve_fit(f,x1,y1)
errors = np.sqrt(np.diag(covariance))
print ('a=',params[0], '±', errors[0])
print ('b=',params[1],'±', errors [1])

plt.plot(x1,y,'bx',label="Messwerte für $U_\mathrm{B}=450V$")
plt.plot(x1,f(x1, *params), 'b-')


plt.xlabel('Magnetfeld $B/\mathrm{mT}$')
plt.ylabel(r'$\frac{D}{L^2+D^2}/\frac{1}{\mathrm{m}}$')
plt.legend(loc='best')
plt.savefig('502-a2.pdf')
