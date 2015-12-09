import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import linregress
import uncertainties as unc
from maketable import maketable

t, U1, U2 = np.genfromtxt("daten/a/LWAVE003.csv", unpack=True, delimiter=',')

U_0 = -5.6

start = 1695
#end = 3299
end = 3586
plt.plot(t, U1, 'r-', markersize=0.1, label='U1', linewidth=0.2)
plt.plot(t[start]*np.ones(2), (-10,10), 'k-')
plt.plot(t[end]*np.ones(2), (-10,10), 'k-')
plt.legend(loc='best')
plt.xlabel(r'$t/s$')
plt.ylabel(r'$U/V$')
plt.xlim(0, 0.01)
plt.savefig('build/a1.pdf')
plt.clf()

U_ber = U1[start:end] - U_0
U_ber = np.log(U_ber)
t_ber = t[start:end]

slope, intercept, r_value, p_value, std_err = linregress(t_ber, U_ber)
maketable([-1/unc.ufloat(slope, std_err)], "build/a.txt", True)

x = np.linspace(0.003, 0.0075)
plt.plot(t_ber, U_ber, 'rx', label='Messwerte', markersize=3)
plt.plot(x, slope * x + intercept, 'b-', label='Lineare Regression')

plt.legend(loc='best')
plt.xlabel(r'$t/\si{\second}$')
plt.ylabel(r'$ln(U/\si{\volt})$')
plt.savefig('build/a2.pdf')
