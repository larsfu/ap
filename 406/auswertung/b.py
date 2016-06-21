import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import uncertainties as unc
import uncertainties.unumpy as unp

phi,I=np.genfromtxt('auswertung/doppel1.txt', unpack=True)
l=633*10**-9 #wellenlänge laser
I*=1e-9

def f(phi, A, b, s, c):
 return (A*(np.cos((np.pi*s*np.sin(phi+c))/l))**2 *(l/(np.pi*b*np.sin(phi+c)))**2 * (np.sin(np.pi*b*np.sin(phi+c)/l))**2)

params, covariance = curve_fit(f,phi,I, p0=[1.5e-6,0.07e-3,0.49e-3, 1e-4], maxfev=1000000)
params =unc.correlated_values(params, covariance)

print ('b=',params[1])
print('s=', params[2])
print('A=', params[0])
x=np.linspace(-0.01,0.0099,1000)


plt.plot(phi,I*1e9,'rx' ,label="Messwerte")
plt.plot(x, f(x, *unp.nominal_values(params))*1e9, 'b-', label='Fit')
plt.xlabel(r'Winkel $\phi  / \si{\radian}$')
plt.ylabel(r'Intensität als Stromstärke $I(\phi)/\si{nA}$')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/doppel.pdf')
