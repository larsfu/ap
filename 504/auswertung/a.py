import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as const
import scipy.stats as stats
import tools

d = np.genfromtxt('daten/a.txt', unpack=True)
U = d[0]
I = d[1:6]

for i in zip(I, range(5)):
    plt.plot(U, i[0], 'x', label=r'$I_H = \SI{' + str(2.5-i[1]*0.1) + r'}{A}$')

plt.plot((0,250), (0.82, 0.82), 'c')
plt.plot((0,250), (0.38, 0.38), 'm')
plt.plot((0,250), (1.6, 1.6), 'r')


plt.xlabel(r"$U/\si{V}$")
plt.ylabel(r"$I/\si{mA}$")
plt.legend(loc='best')
plt.savefig("build/kennlinien.pdf")
tools.table(d, ("U/V", *["I_{}/mA".format(i) for i in range(1,6)]), "build/kennlinien.tex", "tab:kennlinien", "Messdaten der Kennlinien.", round_figures=(2, 3, 3, 3, 3, 3), round=False)
tools.table(((2.1, 2.2, 2.3), (0.82, 0.38, 1.6)), ("I_H/A", "I_S/mA"), "build/saett.tex", "tab:sätt", "Sättigungsströme bei verschiedenen Heizleistungen.", round_figures=(2, 3))
plt.clf()
i = I[0]/1e3

def langmuir_schottkysches_raumladungsgesetz_ist_ein_toller_methodenname(U, exp, asquared):
    j = 4/9 * const.epsilon_0 * np.sqrt(2*const.e/const.m_e) * np.power(U, exp) / asquared
    return j * 0.35e-4

#params, cov = curve_fit(langmuir_schottkysches_raumladungsgesetz_ist_ein_toller_methodenname, U[1:], i[1:], maxfev=1000000000)
#print(U[np.all((U>0, U<200), axis=0)])
slope, intercept, r_value, p_value, std_err = stats.linregress(np.log10(U[np.all((U>0, U<200), axis=0)]), np.log10(i[np.all((U>0, U<200), axis=0)]))

print(slope, std_err)
u = np.linspace(0, 250, 1e5)

plt.plot(u, u**slope*10**intercept*1e3, label='Regression')
#plt.plot(u, langmuir_schottkysches_raumladungsgesetz_ist_ein_toller_methodenname(u, *params)*1e3, 'k-')
plt.plot(U, i*1e3, 'rx', label='Messdaten')
plt.xlabel(r"$U/\si{V}$")
plt.ylabel(r"$I/\si{mA}$")
plt.legend(loc='best')
plt.savefig('build/b.pdf')
