import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

phi,I=np.genfromtxt('einzel1.txt', unpack=True)
l=633*10**-9 #wellenlänge laser
I*=1e-6

def f(phi, A, b):
 return (A**2 * b**2*(l/(np.pi*np.sin(phi)))**2 * (np.sin(np.pi*b*np.sin(phi)/l))**2) #b**2*(l**2/(np.pi*np.sin(phi)))**2*np.sin(np.pi*b*np.sin(phi)/l)**2

params, covariance = curve_fit(f,phi,I, p0=[27.5, 3.8*1e-4])
errors = np.sqrt(np.diag(covariance))

print('A=', params[0], '±', errors[0])
print ('b=',params[1], '±', errors[1])

x=np.linspace(-0.015,0.015,1000)

plt.plot(phi,I,'rx' ,label="Messwerte")
plt.plot(x, f(x, *params)*1e6, 'b-', label='Fit')

plt.xlabel(r'Winkel $\phi$')
plt.ylabel(r'Intensität als Stromstärke $I(\phi)$/ A')
plt.legend(loc='best')
plt.savefig('einzel3.pdf')
