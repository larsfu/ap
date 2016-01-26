import numpy as np
import matplotlib.pyplot as plt
import uncertainties as unc
import uncertainties.unumpy as unp
from scipy.stats import linregress
from scipy.optimize import curve_fit
from peakdetect import peakdetect
from maketable import writevalue
from maketable import maketable


L = unc.ufloat(10.11e-3, 0.03e-3)
C = unc.ufloat(2.098e-9, 0.006e-9)
R_ges = unc.ufloat(509.5 + 50 , 0.5)

def t(f, R, L, C):
    omega = 2 * np.pi * f
    return 1/np.sqrt((1-L*C*omega**2)**2 + omega**2 * R**2 * C**2)

def t2(f, R, L, C):
    omega = 2 * np.pi * f
    return 1/unp.sqrt((1-L*C*omega**2)**2 + omega**2 * R**2 * C**2)

f, U, U_C, a = np.genfromtxt('daten/c.txt', unpack=True)
a /= 1e6

phi = a / (1/f) * 2 * np.pi

maketable((f[:36], U[:36], U_C[:36], (a*1e6)[:36], phi[:36], f[35:], U[35:], U_C[35:], (a*1e6)[35:], phi[35:]), 'build/daten.txt')

U = unp.uarray(U, 0.05*U)
U_C = unp.uarray(U_C, 0.05*U_C)
a = unp.uarray(a, 0.05*a)

phi = a / (1/f) * 2 * np.pi
rel = U_C / U

#print('Fit 1:')
params, pcov = curve_fit(t, f[3:-3], unp.nominal_values(rel)[3:-3],   p0=[1e2, 10e-3, 1e-9], maxfev=1000000000)
params = unc.correlated_values(params, pcov)

x = np.linspace(0, 1e6, 10000)
y_e = t2(x, *params)
y = unp.nominal_values(y_e)
q = y_e.max()

y_e = unp.std_devs(y_e)

writevalue(q, 'build/q.txt')
q_t = 1/R_ges * unp.sqrt(L/C)
writevalue(q_t , 'build/q_t.txt')
#print(q, q_t)

drüber = np.where(y > 1/np.sqrt(2) * q)[0]
drüber_p = np.where(y + y_e > 1/np.sqrt(2) * q)[0]
drüber_m = np.where(y - y_e > 1/np.sqrt(2) * q)[0]

#print(drüber_p[0], drüber_p[-1])
#print(drüber_m[0], drüber_m[-1])


ny_minus = unc.ufloat(x[drüber[0]], np.abs(x[drüber_p[0]]-x[drüber_m[0]]))
ny_plus = unc.ufloat(x[drüber[-1]], np.abs(x[drüber_p[-1]]-x[drüber_m[-1]]))

breite = ny_plus - ny_minus
writevalue(breite, 'build/breite.txt')
breite_t = R_ges / L / (2*np.pi)
writevalue(breite_t, 'build/breite_t.txt')
#print(breite, breite_t)

valuesp = (t2(x, *(unp.nominal_values(params) + unp.std_devs(params)))).astype(float)
valuesm = (t2(x, *(unp.nominal_values(params) - unp.std_devs(params)))).astype(float)


plt.errorbar(f[:3], unp.nominal_values(rel)[:3], yerr=unp.std_devs(rel)[:3], fmt='kx', label='Messwerte, unberücksichtigt', markersize=2.2)
plt.errorbar(f[-3:], unp.nominal_values(rel)[-3:], yerr=unp.std_devs(rel)[-3:], fmt='kx', markersize=2.2)
plt.errorbar(f[3:-3], unp.nominal_values(rel)[3:-3], yerr=unp.std_devs(rel)[3:-3], fmt='rx', label='Messwerte', markersize=2.2)
plt.plot(x, y, 'b-', label='Fit')
#plt.fill_between(x, valuesm, valuesp, facecolor='blue', alpha=0.25, edgecolor='none', label=r'$1\sigma$-Umgebung ($\times 10$)')
#plt.plot((ny_minus, ny_minus), (0,y[drüber[0]]), 'k--', label='Breite der RK')
#plt.plot((ny_plus, ny_plus), (0,y[drüber[-1]]), 'k--')
plt.xlabel(r'$\nu / \si{\hertz}$')
plt.ylabel(r'$U_C / U$')
plt.xscale('log')
plt.yscale('log')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('build/c.pdf')

plt.xscale('linear')
plt.yscale('linear')
plt.xlim(0.6e4, 0.6e5)
plt.savefig('build/c_linear.pdf')
plt.clf()

def t3(f,a,b,c,f0):
    #omega = 2 * np.pi * (f-f0)
    #return a * np.arctan((- omega*R*C)/(1-L*C*omega**2)) + b
    return a * unp.arctan(b*(f-f0)) + c

def t4(f,a,b,c,f0):
    #omega = 2 * np.pi * (f-f0)
    #return a * np.arctan((- omega*R*C)/(1-L*C*omega**2)) + b
    return a * np.arctan(b*(f-f0)) + c

fnicht = f[:5]
phinicht = phi[:5]
#print(fnicht, phinicht)
f = f[5:]
phi = phi[5:]

#f_, U_, U_C_, a_ = np.genfromtxt('daten/c.txt', unpack=True, skip_header=5)
#a_ /= 1e6
#phi_ = a_ / (1/f_) * 2 * np.pi

paramsphi, pcovphi = curve_fit(t4, f, unp.nominal_values(phi), maxfev=100000000)
x = np.linspace(0, 1e6, 1000000)

phi_t = t3(x, *paramsphi)
#res = unc.ufloat(x[np.where(phi_t > np.pi/2)[0][0]], np.abs(x[np.where(phi_t > np.pi/2)[0][0]] - x[np.where(phi_t > np.pi/2)[0][0]]))

a, b, c, f0 = unc.correlated_values(paramsphi, pcovphi)
#res = x[np.where(phi_t > np.pi/2)[0][0]]
res = (1/unp.tan(c/a)) / b + f0
eins = (1/unp.tan(c/a) - np.pi/4 ) / b + f0 #x[np.where(phi_t > 3*np.pi/4)[0][0]]
zwei = (1/unp.tan(c/a) + np.pi/4 ) / b + f0#x[np.where(phi_t > np.pi/4)[0][0]]

writevalue(res, 'build/nu_res.txt')
writevalue(eins, 'build/nu_1.txt')
writevalue(zwei, 'build/nu_2.txt')

res_t = unp.sqrt(1/(L*C))/(2*np.pi)
eins_t = (R_ges/(2*L) + unp.sqrt(R_ges**2 / (4 * L**2) + 1 / (L*C)))/(2*np.pi)
zwei_t = (-R_ges/(2*L) + unp.sqrt(R_ges**2 / (4 * L**2) + 1 / (L*C)))/(2*np.pi)

#print(res, res_t, eins, eins_t, zwei, zwei_t)
writevalue(res_t, 'build/nu_res_t.txt')
writevalue(eins_t, 'build/nu_1_t.txt')
writevalue(zwei_t, 'build/nu_2_t.txt')


#plt.ylim(0,7)
plt.errorbar(fnicht, unp.nominal_values(phinicht), yerr=unp.std_devs(phinicht), fmt='kx', label='Messwerte, unberücksichtigt', markersize=2.2)
plt.errorbar(f, unp.nominal_values(phi), yerr=unp.std_devs(phi), fmt='rx', label='Messwerte', markersize=2.2)
plt.plot(x, unp.nominal_values(t3(x, *paramsphi)), 'b-', label='Fit')
plt.plot((res.n, res.n), (0, np.pi/2), '-.', label=r'$\nu_\text{res}')
plt.plot((eins.n, eins.n), (0, 3*np.pi/4), '-.', label=r'$\nu_\text{2}')
plt.plot((zwei.n, zwei.n), (0, np.pi/4), '-.', label=r'$\nu_\text{1}')
plt.legend(loc='best')
plt.xlabel(r'$\nu / \si{\hertz}$')
plt.ylabel(r'$\phi / \si{\radian}$')
plt.xscale('log')
plt.savefig('build/d.pdf')

plt.xscale('linear')
plt.yscale('linear')
plt.xlim(0.6e4, 0.6e5)
plt.savefig('build/d_linear.pdf')
