import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

x1,y1=np.genfromtxt('a6.txt', unpack=True) #U_B=450V
def f(x1,c,d):
    return c*x1+d
params,covariance = curve_fit(f,x1,y1)
errors = np.sqrt(np.diag(covariance))
print ('c=',params[0], '±', errors[0])
print ('d=',params[1],'±', errors [1])

plt.plot(x1,y1, 'mx',label="Messwerte für $U_\mathrm{B}=450V$")
plt.plot(x1,f(x1, *params), 'm-', label="Ausgleichsgerade")

plt.xlabel(r' Ablenkspannung $U_d/\mathrm{V}$')
plt.ylabel(r'Ablenkung $D/\mathrm{cm}$')
plt.legend(loc='best')
plt.savefig('501-a6.pdf')
