import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as const
import scipy.stats as stats
import tools

d = np.genfromtxt('daten/a.txt', unpack=True, dtype=object)

tools.table(d, ("U/\,V", *["I_{{{}}}/mA".format(["2,5", "2,4", "2,3", "2,2", "2,1"][i]) for i in range(0,5)]), "build/kennlinien.tex", "Messdaten der Kennlinien.", "tab:kennlinien")
U = d[0].astype(float)
I = d[1:6].astype(float)

for i in zip(I, range(5)):
    plt.plot(U, i[0], 'x', label=r'$I_H = \SI{' + str(2.5-i[1]*0.1) + r'}{A}$')

plt.plot((0,250), (0.82, 0.82), 'c')
plt.plot((0,250), (0.38, 0.38), 'm')
plt.plot((0,250), (1.6, 1.6), 'r')
plt.plot((0,250), (2.6, 2.6), 'g')
plt.plot((0,250), (3.3, 3.3), 'b')


plt.xlabel(r"$U/\si{V}$")
plt.ylabel(r"$I/\si{mA}$")
plt.legend(loc='best')
plt.savefig("build/kennlinien.pdf")

tools.table((np.array((b"2.1",b"2.2", b"2.3",b"2.4",b"2.5"), dtype=object), np.array((b"0.82", b"0.38", b"1.60",b"2.60",b"3.30"), dtype=object)), ("I_H/A", "I_S/mA"), "build/saett.tex", "Sättigungsströme bei verschiedenen Heizleistungen.", "tab:sätt")
plt.clf()

i = I[0]/1e3

U_red = U[np.all((U>0, U<200), axis=0)]
i_red = i[np.all((U>0, U<200), axis=0)]
U_f = U[U>=200]
i_f = i[U>=200]

def langmuir_schottkysches_raumladungsgesetz_ist_ein_toller_methodenname(U, exp, asquared):
    j = 4/9 * const.epsilon_0 * np.sqrt(2*const.e/const.m_e) * np.power(U, exp) / asquared
    return j * 0.35e-4

#params, cov = curve_fit(langmuir_schottkysches_raumladungsgesetz_ist_ein_toller_methodenname, U[1:], i[1:], maxfev=1000000000)
#print(U[np.all((U>0, U<200), axis=0)])
slope, intercept, r_value, p_value, std_err = stats.linregress(np.log10(U_red), np.log10(i_red))

print(slope, std_err)
u = np.linspace(0, 250, 1e5)

plt.plot(u, u**slope*10**intercept*1e3, label='Regression')
#plt.plot(u, langmuir_schottkysches_raumladungsgesetz_ist_ein_toller_methodenname(u, *params)*1e3, 'k-')
plt.plot(U_red, i_red*1e3, 'rx', label='Messdaten, berücksichtigt')
plt.plot(U_f, i_f*1e3, 'x', label='Messdaten, unberücksichtigt (Sättigung)')
plt.xlabel(r"$U/\si{V}$")
plt.ylabel(r"$I_{2,5}/\si{mA}$")
plt.legend(loc='best')
plt.savefig('build/b.pdf')
