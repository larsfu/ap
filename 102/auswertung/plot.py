import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

x_=np.linspace(0.5,2.5)
plt.xlim(0.5,2.4)
x,y=np.genfromtxt('auswertung/daten.txt',unpack=True)

def f(x,a,b):
    return a*x+b
params,covariance = curve_fit(f,x,y)
errors = np.sqrt(np.diag(covariance))
print ('a=',params[0], '±', errors[0])
print ('b=',params[1],'±', errors [1])

plt.plot(x,y,'rx',label="Messwerte")
plt.plot(x_,f(x_, *params), 'b-',label="Ausgleichsgerade")
plt.xlabel(r'$T^{-2}/\SI{1e-2}{\per\second\squared}$')
plt.ylabel(r'$B/\si{\milli\tesla}$')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('build/magn-moment.pdf')
