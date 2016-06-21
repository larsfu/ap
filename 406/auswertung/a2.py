import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

phi,I=np.genfromtxt('auswertung/einzel2b.txt', unpack=True)
l=633e-9 #wellenlänge laser
I*=1e-9

def f(phi, A, b, c):
 return (A**2 * b**2*(l/(np.pi*np.sin(phi+c)))**2 * (np.sin(np.pi*b*np.sin(phi+c)/l))**2) #b**2*(l**2/(np.pi*np.sin(phi)))**2*np.sin(np.pi*b*np.sin(phi)/l)**2
params, covariance = curve_fit(f,phi,I, maxfev=10000000, p0=[1e5, 0.5e-4, 1e-4])
errors = np.sqrt(np.diag(covariance))

print('A=', params[0], '±', errors[0])
print ('b=',params[1], '±', errors[1])

x=np.linspace(-0.015,0.01499,1000)

plt.plot(phi,I*1e9,'rx' ,label="Messwerte")
plt.plot(x, f(x, *params)*1e9, 'b-', label='Fit')

plt.xlabel(r'Winkel $\phi  / \si{\radian}$')
plt.ylabel(r'Intensität als Stromstärke $I(\phi)/\si{nA}$')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/einzel2.pdf')
