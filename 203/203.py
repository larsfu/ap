import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from scipy.stats import linregress
from scipy.constants.constants import C2K
from scipy.optimize import curve_fit
import scipy.constants as const
import scipy
import math
import uncertainties

T, p = np.genfromtxt("teil1.txt", unpack=True)
T2, p2 = np.genfromtxt("teil2.txt", unpack=True)

#T = T[1:]
#81p = p[1:]
p*=100000
p2*=100000
p=np.log(p)
T2 = C2K(T2)
T = C2K(T)
T = 1/T

print(list(zip(T2, p2/1000)))
slope, intercept, r_value, p_value, std_err = linregress(T, p)
print(linregress(T, p))

def f(x):
    return slope*x + intercept

#print(np.std(p - f(T)))
m = (np.mean(T*p) - np.mean(T) * np.mean(p))/ (np.mean(T**2) - np.mean(T)**2)
b = np.mean(p) - m * np.mean(T)
#print(b)
N = len(p)
MSE = np.sqrt(1/(N-2) * np.sum((p-b -m*T)**2))
#D = N * sum(T**2) - sum(T)**2
#sigma_m_squared = np.sqrt(N * sigma_squared / D)
SE = MSE / np.sqrt(np.sum((T-np.mean(T))**2))
SER = np.sqrt((np.sum(p))/(N-2))


#print(r_value**2)
#print(np.std(p)**2 / (len(p) *(np.mean(p**2) - np.mean(p)**2)))
R = 8.3144598
L = -slope * R
delta_R = 0.0000048
print('{}±{}'.format(L, np.sqrt(slope**2 * delta_R**2 + R**2 * SE**2)))

L = uncertainties.ufloat(L, np.sqrt(slope**2 * delta_R**2 + R**2 * SE**2))

L /= 6.022140857e23
La = uncertainties.ufloat(8.3144598, 0.0000048) * 373 / 6.022140857e23
Li = L - La
print(Li / 1.6021766208e-19)

'''
def pol(x, a, b, c, d):
    return a*x**3 + b*x**2 + c*x + d

params, pcov = curve_fit(pol, T2, p2)
print('{:G}x³ + {:G}x² + {:g}x + {:g}'.format(*params))
x = np.linspace(370,440)
plt.plot(x, pol(x, *params), 'b-', label='Ausgleichspolynom dritten Grades')
plt.plot(T2, p2, 'rx', label='Messdaten')

plt.xlabel(r'$T/\si{\kelvin}$')
plt.ylabel(r'$p/\si{\pascal}$')
#plt.yscale('log', basey=np.e, subsy=np.exp(np.log10(np.arange(1,10))))
#plt.xlim(0.0027, 0.00307)
plt.legend(loc='best')
plt.grid(True, which='both')
#plt.yticks([np.e**-14, np.e**-13, np.e**-12, np.e**-11], [r'$\mathrm{e}^{-14}$', r'$\mathrm{e}^{-13}$', r'$\mathrm{e}^{-12}$', r'$\mathrm{e}^{-11}$'])
#plt.ylim(np.e**-14,np.e**-11)

plt.savefig('203_plot2.pdf')
plt.clf()


x = np.linspace(1/C2K(35),1/C2K(105),100)
plt.plot(x, np.exp(x*slope+intercept), 'b-', label='Lineare Regression')
plt.plot(T, np.exp(p), 'rx', label='Messdaten')

plt.xlabel(r'$T^{-1}/\si{\per\kelvin}$')
plt.ylabel(r'$p/\si{\pascal}$')
plt.yscale('log', basey=np.e, subsy=np.exp(np.log10(np.arange(1,10))))
plt.xlim(0.0027, 0.00307)
plt.legend()
plt.grid(True, which='both')
plt.yticks([np.e**9, np.e**10, np.e**11, np.e**12], [r'$\mathrm{e}^{9}$', r'$\mathrm{e}^{10}$', r'$\mathrm{e}^{11}$', r'$\mathrm{e}^{12}$'])
plt.ylim(np.e**9,np.e**12)

plt.savefig('203_plot.pdf')
'''
