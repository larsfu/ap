import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

x2,y2=np.genfromtxt('a3.txt', unpack=True) #U_B=300V

def f(x2,e,f):
    return e*x2+f
params,covariance = curve_fit(f,x2,y2)
errors = np.sqrt(np.diag(covariance))
print ('e=',params[0], '±', errors[0])
print ('f=',params[1],'±', errors [1])

plt.plot(x2,y2, 'gx',label="Messwerte für $U_\mathrm{B}=300V$")
plt.plot(x2,f(x2, *params), 'g-', label="Ausgleichsgerade")

plt.xlabel(r' Ablenkspannung $U_d/\mathrm{V}$')
plt.ylabel(r'Ablenkung $D/\mathrm{cm}$')
plt.legend(loc='best')
plt.savefig('501-a-3.pdf')
