import numpy as np
import matplotlib.pyplot as plt
import uncertainties as unc
from scipy.stats import linregress
from scipy.optimize import curve_fit

def t(f, R, L, C):
    omega = 2 * np.pi * f
    return 1/np.sqrt((1-L*C*omega**2)**2 + omega**2 * R**2 * C**2)

f, U, U_C, a = np.genfromtxt('daten/c.txt', unpack=True)
a /= 1e6
phi = a / (1/f) * 2 * np.pi

params, pcov = curve_fit(t, f, U_C/U, p0=[1e2, 1e-3, 1e-4], maxfev=1000000)
x = np.linspace(1e2, 1e6, 10000)
print(params)

plt.plot(f, U_C/U, 'rx')
plt.plot(x, t(x, *params), 'b-')
plt.xlabel(r'$f / \si{\hertz}$')
plt.ylabel(r'$U_C / U$')
plt.xscale('log')
plt.yscale('log')
plt.savefig('build/c.pdf')

plt.xscale('linear')
plt.yscale('linear')
plt.xlim(0.6e4, 0.6e5)
plt.savefig('build/c_linear.pdf')


plt.clf()
plt.plot(f, phi, 'rx')
plt.savefig('build/d.pdf')
