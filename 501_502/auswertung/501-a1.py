import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

x=np.linspace(-21,9)
x,y=np.genfromtxt('a1.txt',unpack=True) #U_B=200V

def f(x,a,b):
    return a*x+b
params,covariance = curve_fit(f,x,y)
errors = np.sqrt(np.diag(covariance))
print ('a=',params[0], '±', errors[0])
print ('b=',params[1],'±', errors [1])

plt.plot(x,y,'bx',label="Messwerte für $U_\mathrm{B}=200V$")
plt.plot(x,f(x, *params), 'b-', label="Ausgleichsgerade")

plt.xlabel(r' Ablenkspannung $U_d/\mathrm{V}$')
plt.ylabel(r'Ablenkung $D/\mathrm{cm}$')
plt.legend(loc='best')
plt.savefig('501-a1.pdf')
