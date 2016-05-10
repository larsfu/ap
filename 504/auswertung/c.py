import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as const
import scipy.stats as stats
import tools

d = np.genfromtxt('daten/c.txt', unpack=True, dtype=object)
Ur, I = d.astype(float)
innenwiderstand = 1e6
I /= 1e9
U = Ur - I*innenwiderstand
print(U)
def anlaufstrom(U, C, T):
    j = C * np.exp((const.elementary_charge * U)/(const.k * T))
    return j * 0.35e-4

params, cov = curve_fit(anlaufstrom, U, I, maxfev=1000000, p0=[1, 1000])
print(params)

u = np.linspace(-1,0.05,1e6)
plt.plot(u, 1e9*anlaufstrom(u, *params), 'b-', label='Fit')
plt.plot(U, 1e9*I, 'rx', label='Daten')
plt.xlim(-1, 0.05)
plt.xlabel(r"$U_G/\si{V}$")
plt.ylabel(r"$I/\si{nA}$")
plt.tight_layout()
plt.legend(loc='best')
plt.savefig('build/c.pdf')

tools.table((d[0], U, d[1]), ("U_G/V",r"U_\text{korr}/V", "I/nA"), "build/fqfepoijfewoij.tex", "Daten der Messreihe für das Anlaufstromgebiet.", "tab:anlauf", round_figures=(2,2,3), split=2)
