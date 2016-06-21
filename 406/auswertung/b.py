import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

phi,I=np.genfromtxt('doppel1.txt', unpack=True)
l=633*10**-9 #wellenlänge laser
I*=1e-9

def f(phi, A, b, s):
 return (A*(np.cos((np.pi*s*np.sin(phi))/l))**2 *(l/(np.pi*b*np.sin(phi)))**2 * (np.sin(np.pi*b*np.sin(phi)/l))**2)

params, covariance = curve_fit(f,phi,I, p0=[1.5e-6,0.07e-3,0.49e-3])
errors=np.sqrt(np.diag(covariance))

print ('b=',params[1])
print('s=', params[2])
print('A=', params[0])
x=np.linspace(-0.01,0.01,1000)


plt.plot(phi,I,'rx' ,label="Messwerte")
plt.plot(x, f(x, *params), 'b-', label='Fit')
plt.xlabel(r'Winkel $\phi$')
plt.ylabel(r'Intensität als Stromstärke $I(\phi)$/ A')
plt.legend(loc='best')
plt.savefig('doppel.pdf')
