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

f, U, U_C, a = np.genfromtxt('daten/c.txt', unpack=True)
a /= 1e6
phi = a / (1/f) * 2 * np.pi

maketable((f, U, U_C, a*1e6, phi), 'build/daten.txt')

#print('Fit 1:')
params, pcov = curve_fit(t, f, U_C/U, p0=[1e2, 10e-3, 1e-9], maxfev=10000)
x = np.linspace(0, 1e6, 1000000)
y = t(x, *params)
q = y.max()

writevalue(q, 'build/q.txt')
q_t = 1/R_ges * unp.sqrt(L/C)
writevalue(q_t , 'build/q_t.txt')
print(q, q_t)

drüber = np.where(y > 1/np.sqrt(2) * q)[0]
ny_minus = x[drüber[0]]
ny_plus = x[drüber[-1]]

breite = ny_plus - ny_minus
writevalue(breite, 'build/breite.txt')
breite_t = R_ges / L / (2*np.pi)
writevalue(breite_t, 'build/breite_t.txt')
print(breite, breite_t)

plt.plot(f, U_C/U, 'rx', label='Messwerte')
plt.plot(x, y, 'b-', label='Fit')
plt.plot((ny_minus, ny_minus), (0,y[drüber[0]]), 'k--', label='Breite der RK')
plt.plot((ny_plus, ny_plus), (0,y[drüber[-1]]), 'k--')
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

def t2(f,a,b,c,f0):
    omega = 2 * np.pi * (f-f0)
    #return a * np.arctan((- omega*R*C)/(1-L*C*omega**2)) + b
    return a * np.arctan(b*(f-f0)) + c


#f = f[6:]
#phi = phi[6:]

f_, U_, U_C_, a_ = np.genfromtxt('daten/c.txt', unpack=True, skip_header=5)
a_ /= 1e6
phi_ = a_ / (1/f_) * 2 * np.pi

paramsphi, pcovphi = curve_fit(t2, f_, phi_, maxfev=100000000)
#print(paramsphi)
x = np.linspace(0, 1e6, 1000000)

phi_t = t2(x, *paramsphi)
res = x[np.where(phi_t > np.pi/2)[0][0]]
eins = x[np.where(phi_t > 3*np.pi/4)[0][0]]
zwei = x[np.where(phi_t > np.pi/4)[0][0]]

writevalue(res, 'build/nu_res.txt')
writevalue(eins, 'build/nu_1.txt')
writevalue(zwei, 'build/nu_2.txt')

res_t = unp.sqrt(1/(L*C))/2*np.pi
eins_t = (R_ges/(2*L) + unp.sqrt(R_ges**2 / (4 * L**2) + 1 / (L*C)))/(2*np.pi)
zwei_t = (-R_ges/(2*L) + unp.sqrt(R_ges**2 / (4 * L**2) + 1 / (L*C)))/(2*np.pi)

print(res, res_t, eins, eins_t, zwei, zwei_t)
writevalue(res_t, 'build/nu_res_t.txt')
writevalue(eins, 'build/nu_1_t.txt')
writevalue(zwei, 'build/nu_2_t.txt')


#plt.ylim(0,7)
plt.plot(f, phi, 'rx', label='Messwerte')
plt.plot(x, t2(x, *paramsphi), 'b-', label='Fit')
plt.plot((res, res), (0, np.pi/2), '-.', label=r'$\nu_\text{res}')
plt.plot((eins, eins), (0, 3*np.pi/4), '-.', label=r'$\nu_\text{2}')
plt.plot((zwei, zwei), (0, np.pi/4), '-.', label=r'$\nu_\text{1}')
plt.legend(loc='best')
plt.xlabel(r'$\nu / \si{\hertz}$')
plt.ylabel(r'$\phi / \si{\radian}$')
plt.xscale('log')
plt.savefig('build/d.pdf')

plt.xscale('linear')
plt.yscale('linear')
plt.xlim(0.6e4, 0.6e5)
plt.savefig('build/d_linear.pdf')
