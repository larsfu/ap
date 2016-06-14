import numpy as np
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp
import uncertainties as unc
import tools

def linregress(x, y):
    assert len(x) == len(y)

    x, y = np.array(x), np.array(y)

    N = len(y)
    Delta = N * np.sum(x**2) - (np.sum(x))**2

    A = (N * np.sum(x * y) - np.sum(x) * np.sum(y)) / Delta
    B = (np.sum(x**2) * np.sum(y) - np.sum(x) * np.sum(x * y)) / Delta

    sigma_y = np.sqrt(np.sum((y - A * x - B)**2) / (N - 2))

    A_error = sigma_y * np.sqrt(N / Delta)
    B_error = sigma_y * np.sqrt(np.sum(x**2) / Delta)

    return A, A_error, B, B_error

Al = np.genfromtxt('daten/{}.txt'.format('Al'), unpack=True, dtype=object)

d, delta_d, t, n = Al.astype(float)

delta_d /= 1e6
N_u = unc.ufloat(324/900, np.sqrt(324)/900)
d = unp.uarray(d, delta_d) * 1e-6
N = unp.uarray(n/t, np.sqrt(n)/t) - N_u

tools.table((Al[0], Al[1], Al[2], N), ("d/mm", "n", "(N-N_U)/\per\second"), "build/Al.tex", "Messdaten von Aluminium.", "tab:datenAl", split=2)

slope1, std_a1, intercept1, std_b1 = linregress(unp.nominal_values(d[:4]), unp.nominal_values(N[:4]))
slope2, std_a2, intercept2, std_b2 = linregress(unp.nominal_values(d[5:]), unp.nominal_values(N[5:]))

print(std_a1, std_a2)

D_max = (unc.ufloat(intercept2, std_b2)-unc.ufloat(intercept1, std_b1))/(unc.ufloat(slope1, std_a1) - unc.ufloat(slope2, std_a2))
R_max = D_max * 2700 * 10
print("D_max = {}µm, R_max = {}g/cm², E_max = {} MeV".format(D_max*1e6, R_max, 1.92*unp.sqrt(R_max**2 - 0.22*R_max)))
#print(unp.nominal_values(d), N)
sd = np.linspace(0, 0.5e-3)


plt.ylim(-5, 50)
plt.plot(1e6*sd, sd*slope2+intercept2, 'b-', label=r"Lineare Regression, $R > R_\text{max}$")
plt.plot(1e6*sd, sd*slope1+intercept1, 'r-', label=r"Lineare Regression, $R < R_\text{max}$")
plt.errorbar(1e6*unp.nominal_values(d[:4]), unp.nominal_values(N[:4]), fmt='rx', yerr=unp.std_devs(N[:4]), label=r"Messdaten, $R < R_\text{max}$")
plt.errorbar(1e6*unp.nominal_values(d[5:]), unp.nominal_values(N[5:]), fmt='bx', yerr=unp.std_devs(N[5:]), label=r"Messdaten, $R > R_\text{max}$")
plt.errorbar(1e6*unp.nominal_values(d[4:5]), unp.nominal_values(N[4:5]), fmt='kx', yerr=unp.std_devs(N[4:5]), label=r"Messdaten, unberücksichtigt")

plt.legend(loc='best')
plt.xlabel(r"$d/\si{\micro\meter}$")
plt.ylabel(r"$N/\si{\per\second}$")
plt.tight_layout(pad=0)
plt.savefig("build/beta.pdf")
plt.clf()
