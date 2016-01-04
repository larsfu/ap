import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from peakdetect import peakdetect
import uncertainties as unc
import uncertainties.unumpy as unp
from maketable import writevalue

shit, shit, shit, t, U, shit = np.genfromtxt('daten/a/F0004CH1.CSV', delimiter=',', unpack=True)

L = unc.ufloat(10.11e-3, 0.03e-3)
C = unc.ufloat(2.098e-9, 0.006e-9)

start = 427
stop = 2298
t = t[start:stop] - t[start]
U = -U[start:stop]

extrema = peakdetect(U, t, 20)
maxs = np.array(extrema[0])
mins = np.array(extrema[1])
maxs_x = maxs[:,0]
maxs_y = maxs[:,1]
mins_x = mins[:,0]
mins_y = mins[:,1]

def envelope(t, tau, U):
    return U * np.exp(-t*tau)

paramsmax, pcovmax = curve_fit(envelope, maxs_x, maxs_y)
paramsmin, pcovmin = curve_fit(envelope, mins_x, mins_y)

tau, U0 = unc.correlated_values(paramsmax, pcovmax)
T_ex = 1 / tau
R_eff =  2 * L / T_ex
writevalue(T_ex*1e6, 'build/T_ex.txt')
writevalue(R_eff, 'build/R_eff.txt')

#print(T_ex*1e6, R_eff)
R_ap = unp.sqrt(4*L**2 / (L*C))
print(R_ap)
writevalue(R_ap, 'build/R_ap_t.txt')

x = np.linspace(0, t[len(t)-1], 1000)
plt.xlim(0, 0.74)
plt.xlabel(r't/\si{\milli\second}')
plt.ylabel(r'U/\si{\volt}')
plt.plot(t*1000, U, 'b-', label='Spannnugsverlauf')
plt.plot(x*1000, envelope(x, *paramsmax), 'r-', label='Einhüllende')
plt.plot(x*1000, envelope(x, *paramsmin), 'r-')
plt.plot(maxs[:,0]*1000, maxs[:,1], 'rx')
plt.plot(mins[:,0]*1000, mins[:,1], 'rx')

plt.savefig('build/a.pdf')
