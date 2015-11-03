import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.constants.constants import C2K

t, T1, T2, pa, pb, P = np.genfromtxt("daten.txt", unpack = True)

T1 = C2K(T1)
T2 = C2K(T2)

def T(t, A, B, C, α):
    return A * t ** α / (1 + B * t ** α) + C

params1, pcov1 = curve_fit(T, t, T1, maxfev = 1000000, p0 = (1, 1e-2, 295, 1.5))
params2, pcov2 = curve_fit(T, t, T2, maxfev = 1000000, p0 = (-0.01, 1e-2, 295, 1.5))

print(params1, params2)

x = np.linspace(0, 1800, 1000)

plt.plot(t, T1, 'rx', label='$T_1$', markersize = 4)
plt.plot(t, T2, 'bx', label='$T_2$', markersize = 4)
plt.plot(x, T(x, *params1), 'r-')
plt.plot(x, T(x, *params2), 'b-')


plt.xlabel(r'$t / \si{\second}$')
plt.ylabel(r'$T / \si{\kelvin}$')
plt.legend(loc='best')

# in matplotlibrc leider (noch) nicht möglich
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/plot.pdf')
