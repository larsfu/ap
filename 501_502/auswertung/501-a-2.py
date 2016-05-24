import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

x1,y1=np.genfromtxt('a2.txt', unpack=True) #U_B=250V
def f(x1,c,d):
    return c*x1+d
params,covariance = curve_fit(f,x1,y1)
errors = np.sqrt(np.diag(covariance))
print ('c=',params[0], '±', errors[0])
print ('d=',params[1],'±', errors [1])

plt.plot(x1,y1, 'rx',label="Messwerte für $U_\mathrm{B}=250V$")
plt.plot(x1,f(x1, *params), 'r-')

plt.xlabel(r'$U_\mathrm{d}/V$')
plt.ylabel('$D/cm$')
plt.legend(loc='best')
plt.savefig('501-a-2.pdf')
