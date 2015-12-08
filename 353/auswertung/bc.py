import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import uncertainties as unc
import uncertainties.unumpy as unp
from maketable import maketable

f, U, a, U0 = np.genfromtxt('daten/bc.txt', unpack=True)
a = unp.uarray(a, 0.05*a)
a /= 1000
U = unp.uarray(U, 0.05*U)
U0 = unp.uarray(U0, 0.05*U0)

def A(f, RC):
    return 1 / np.sqrt(1+(2*np.pi*f)**2 * RC**2)

def phi(f, RC):
    return np.arctan(f*2*np.pi*RC)

phi_ = a / (1/f) * 2 * np.pi
A_ = U/U0

maketable((f.astype(int),unp.nominal_values(U),unp.nominal_values(U0),A_,unp.nominal_values(a*1000),phi_), 'build/daten.txt')

paramsa, pcova = curve_fit(A, f, unp.nominal_values(A_), p0=[1/742], sigma=unp.std_devs(A_), absolute_sigma=True)
paramsb, pcovb = curve_fit(phi, f, unp.nominal_values(phi_), p0=[1/742], sigma=unp.std_devs(phi_), absolute_sigma=True)
paramsa_u = unc.correlated_values(paramsa, pcova)
paramsb_u = unc.correlated_values(paramsb, pcovb)
maketable([paramsa_u], 'build/b1.txt', True)
maketable([paramsb_u], 'build/b2.txt', True )


x = np.linspace(0.2, 10000, 100000)
plt.fill_between(x, A(x, paramsa_u[0].n - paramsa_u[0].s*10), A(x, paramsa_u[0].n + paramsa_u[0].s*10), facecolor='blue', alpha=0.25, edgecolor='none', label=r'$1\sigma$-Umgebung ($\times 10$)')
plt.plot(x, A(x, *paramsa), 'b-', label='Messdaten')
plt.errorbar(f, unp.nominal_values(A_), yerr=unp.std_devs(A_), fmt='rx', label='Fit')
plt.xlabel(r'$\nu/\si{\hertz}')
plt.ylabel(r'$U/U0$')
plt.xlim(4, 11000)
plt.legend(loc='best')
plt.xscale('log')
plt.savefig('build/b1.pdf')
plt.clf()

plt.errorbar(f, unp.nominal_values(phi_), yerr=unp.std_devs(phi_), fmt='rx', label='Messdaten')
plt.plot(x, phi(x, *paramsb), 'b-', label='Fit')
plt.fill_between(x, phi(x, paramsb_u[0].n - paramsb_u[0].s*10), phi(x, paramsb_u[0].n + paramsb_u[0].s*10), facecolor='blue', alpha=0.25, edgecolor='none', label=r'$1\sigma$-Umgebung ($\times 10$)')
plt.xlabel(r'$\nu/\si{\hertz}')
plt.ylabel(r'$\phi$')
plt.xscale('log')
plt.xlim(4,11000)
plt.legend(loc='lower right')
plt.savefig('build/b2.pdf')
plt.clf()

RC = np.mean((paramsa[0], paramsb[0]))

phi__ = np.linspace(0, 2*np.pi, 10000)
plt.polar(phi(x, *paramsb), A(x, *paramsa), 'b-', label=r'$A(\omega) / U_0')
plt.polar(unp.nominal_values(phi_), unp.nominal_values(A_), 'rx')
plt.legend(loc='best')
#plt.xlabel(r'$\phi')
plt.savefig('build/b3.pdf')
