import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import uncertainties.unumpy as unp
from uncertainties import ufloat

x=np.linspace(0.0015, 0.0055)
x=[1/200, 1/250, 1/300, 1/350, 1/400, 1/450, 1/500]
y=[0.177, 0.140, 0.116, 0.099, 0.089, 0.080, 0.076]
e=[0.001, 0.001, 0.001, 0.001, 0.001, 0.002, 0.001]

def f(x, a, b):
  return a*x+b
params,covariance=curve_fit(f,x,y)
params, covariance = curve_fit(f, x, y, sigma=e)
print ('a=',params[0], '±', covariance[0,0]**0.5)
print ('b=',params[1], '±', covariance[1,1]**0.5)
e=[0.001, 0.001, 0.001, 0.001, 0.001, 0.002, 0.001]
plt.errorbar(x,y,yerr=e, fmt='None')
xfine=np.linspace(0.002 ,0.005,100)
plt.plot(xfine, f(xfine, params[0], params[1]), 'r-')

a=ufloat(34.147,0.972)
print ((a/35.75)*100)
plt.xlabel(r'$\frac{1}{U_\mathrm{B}}}/\frac{1}{V}$')
plt.ylabel(r'$\frac{D}{U_\mathrm{d}}/\frac{cm}{V}$')
plt.savefig('501-a3.pdf')