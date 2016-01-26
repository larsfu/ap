import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

x=np.linspace(0,3)
plt.xlim(0.5,2.4)
x,y=np.genfromtxt('daten.txt',unpack=True)

def f(x,a,b):
    return a*x+b
params,covariance = curve_fit(f,x,y)
errors = np.sqrt(np.diag(covariance))
print ('a=',params[0], '±', errors[0])
print ('b=',params[1],'±', errors [1])

plt.plot(x,y,'rx',label="Messwerte")
plt.plot(x,f(x, *params), 'b-',label="Ausgleichsgerade")

plt.xlabel(r'$\frac{1}{T^2}/10^{-2}\frac{1}{s^2}$')
plt.ylabel(r'$B/10^{-3}T$')
plt.legend(loc='best')
plt.savefig('magn-moment.pdf')
