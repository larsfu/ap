import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import uncertainties as unc
from maketable import maketable

f, U, a, U0 = np.genfromtxt('daten/bc.txt', unpack=True)
a /= 1000

def A(f, RC):
    return 1 / np.sqrt(1+(2*np.pi*f)**2 * RC**2)

def phi(f, RC):
    return np.arctan(f*2*np.pi*RC)

phi_ = a / (1/f) * 2 * np.pi

paramsa, pcova = curve_fit(A, f, U/U0, p0=[1/742])
paramsb, pcovb = curve_fit(phi, f, phi_, p0=[1/742])
paramsa_u = unc.correlated_values(paramsa, pcova)
paramsb_u = unc.correlated_values(paramsb, pcovb)
maketable([paramsa_u], 'build/b1.txt', True)
maketable([paramsb_u], 'build/b2.txt', True )


x = np.linspace(0.2, 1000, 10000)
plt.plot(x, A(x, *paramsa), 'b-', label='Messdaten')
plt.plot(f, U/U0, 'rx', label='Fit')
plt.xlabel(r'$\nu/\si{\hertz}')
plt.ylabel(r'$U/U0$')
plt.ylim(1e-1, 1.1)
plt.legend(loc='best')
plt.yscale('log')
plt.savefig('build/b1.pdf')
plt.clf()

plt.plot(f, phi_, 'rx', label='Messdaten')
plt.plot(x, phi(x, *paramsb), 'b-', label='Fit')
plt.xlabel(r'$\nu/\si{\hertz}')
plt.ylabel(r'$\phi$')
plt.yscale('log')
plt.xlim(0,1000)
plt.legend(loc='lower right')
plt.savefig('build/b2.pdf')
plt.clf()

RC = np.mean((paramsa[0], paramsb[0]))

phi__ = np.linspace(0, 2*np.pi, 10000)
plt.polar(phi(x, *paramsb), A(x, *paramsa), 'b-', label=r'$A(\omega) / U_0')
plt.polar(phi_, U/U0, 'rx')
plt.legend(loc='best')
#plt.xlabel(r'$\phi')
plt.savefig('build/b3.pdf')
