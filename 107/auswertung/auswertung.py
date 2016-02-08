import numpy as np
import uncertainties as unc
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.constants.constants import C2K
from scipy.stats import linregress
from maketable import maketable


K_k = 0.07640e-6
m_k = 4.43e-3
m_g = 4.95e-3
d_k = 15.319e-3
d_g = 15.492e-3
rho_w = 998.21

t_klein, t_groß = np.genfromtxt('daten/a.txt', unpack=True)
maketable((t_klein, t_groß), 'build/d1.tex')
t_k = unc.ufloat(t_klein.mean(), t_klein.std())
t_g = unc.ufloat(t_groß.mean(), t_groß.std())

print("t_kquer = {}, t_gquer = {}".format(t_k, t_g))

V_k = 4/3 * np.pi*(d_k/2)**3
V_g = 4/3 * np.pi*(d_g/2)**3

print("rho = {}, {}".format(m_k/V_k, m_g/V_g))

eta_k = K_k * (m_k/V_k - rho_w) * t_k
print("ηₖ = {}".format(eta_k*1e3))

K_g = eta_k/((m_g/V_g - rho_w) * t_g)
print("Kg = {}".format(K_g))

T_ref, rho_ref = np.genfromtxt('daten/rho.txt', unpack=True)
T_ref = C2K(T_ref)
maketable((T_ref, rho_ref), 'build/dichte.tex')
z = np.polyfit(T_ref, rho_ref, 2)
rho = np.poly1d(z)
T_ = np.linspace(C2K(15), C2K(70), 1000)

plt.plot(T_ref, rho_ref, 'rx', label='Literaturdaten')
plt.plot(T_, rho(T_), 'b-', label='Quadratischer Fit')
plt.xlim(C2K(15),C2K(70))
plt.xlabel(r'$T / \si{\kelvin}$')
plt.ylabel(r'$\rho_\text{Wasser} / \si{\kilogram\per\cubic\meter}$')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/dichte.pdf')
plt.clf()

T, t1, t2 = np.genfromtxt('daten/b.txt', unpack=True)
T = C2K(T)
t = unp.uarray(np.mean([t1, t2], 0), np.std([t1, t2], 0))
maketable((T, t1, t2, t), 'build/d1.tex')

eta = K_g * (m_g/V_g - rho(T)) * t

Re = rho_w * 100e-3 / t * d_g / eta

print(eta)
maketable((T, t1, t2, t, rho(T), 1e3*eta, Re), 'build/erg.tex')
print('Re_max = {}'.format(Re[-1]))

def eta_th(T, A, B):
    return A * np.exp(B/T)

params, pcov = curve_fit(eta_th, T, unp.nominal_values(eta), sigma=unp.std_devs(eta), p0=[np.exp(-6.944), 2036], maxfev=100000000)
params = unc.correlated_values(params, pcov)
print("A = {}, B = {}".format(*params))

T_ = np.linspace(C2K(25), C2K(65), 1000)
valuesp = (eta_th(T_, *(unp.nominal_values(params) + unp.std_devs(params)))).astype(float)
valuesm = (eta_th(T_, *(unp.nominal_values(params) - unp.std_devs(params)))).astype(float)

plt.errorbar(T, 1000*unp.nominal_values(eta), yerr=1000*unp.std_devs(eta), fmt='rx', label='Messdaten', markersize=3)
plt.plot(T_, 1000*eta_th(T_, *unp.nominal_values(params)), 'b-', label='Fit')
plt.fill_between(T_, 1000*valuesm, 1000*valuesp, facecolor='blue', alpha=0.125, edgecolor='none', label=r'$1\sigma$-Umgebung')
plt.xlim(C2K(26),C2K(65))
plt.xlabel(r'$T / \si{\kelvin}$')
plt.ylabel(r'$\eta / \si{\milli\pascal\second}$')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/viskosität.pdf')
plt.clf()

T_r = 1/T
T_r_ = 1/T_
lneta = unp.log(eta)
slope, intercept, r_value, p_value, std_err = linregress(T_r, unp.nominal_values(lneta))
print(slope, intercept, r_value**2)

B = unc.ufloat(slope, std_err)
A = unp.exp(unc.ufloat(intercept, std_err * T_r.mean()))
print("A = {}, B = {}".format(A, B))

valuesp = (slope + std_err) * T_r_ + intercept + std_err * T_r.mean()
valuesm = (slope - std_err) * T_r_ + intercept - std_err * T_r.mean()

plt.errorbar(T_r, unp.nominal_values(lneta), yerr=unp.std_devs(lneta), fmt='rx', label='Messdaten', markersize=3)
plt.plot(T_r_, slope*T_r_ + intercept, 'b-', label='Lineare Regression')
plt.fill_between(T_r_, valuesm, valuesp, facecolor='blue', alpha=0.125, edgecolor='none', label=r'$1\sigma$-Umgebung')
plt.xlim(0.00297, 0.00333)
plt.xlabel(r'$T^{-1} / \si{\per\kelvin}$')
plt.ylabel(r'$\ln(\eta / \si{\milli\pascal\second})$')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/viskosität_linear.pdf')
plt.clf()

T_ref, eta_ref = np.genfromtxt('daten/eta.txt', unpack=True)
T_ref = C2K(T_ref)
eta_ref /= 1e6
z = np.polyfit(T_ref, eta_ref, 2)
eta_ = np.poly1d(z)
T_ = np.linspace(300, C2K(70), 1000)

plt.plot(T_ref, 1000*eta_ref, 'rx', label='Literaturdaten')
plt.plot(T_, 1000*eta_(T_), 'b-', label='Quadratischer Fit')
plt.xlim(300,C2K(70))
plt.xlabel(r'$T / \si{\kelvin}$')
plt.ylabel(r'$\eta / \si{\milli\pascal\second}$')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('build/eta.pdf')
plt.clf()

maketable((T, eta*1e3, eta_(T)*1e3, eta/eta_(T)), 'build/disk.tex')
