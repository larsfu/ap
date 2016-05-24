import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

x3,y3=np.genfromtxt('a4.txt',unpack=True) #U_B=350V


def f(x3,g,h):
    return g*x3+h
params,covariance = curve_fit(f,x3,y3)
errors = np.sqrt(np.diag(covariance))
print ('g=',params[0], '±', errors[0])
print ('h=',params[1],'±', errors [1])

plt.plot(x3,y3, 'kx',label="Messwerte für $U_\mathrm{B}=350V$")
plt.plot(x3,f(x3, *params), 'k-', label="Ausgleichsgerade")

plt.xlabel(r' Ablenkspannung $U_d/\mathrm{V}$')
plt.ylabel(r'Ablenkung $D/\mathrm{cm}$')
plt.legend(loc='best')
plt.savefig('501-a4.pdf')
