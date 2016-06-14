import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import uncertainties.unumpy as unp
import uncertainties as unc
import scipy.constants as const
import tools

def fit(x, a, b):
    return a * np.exp(b * x)

def auswerten(name, d, n, t, z, V_mol, eps, raw):
    d *= 1e-3
    N = unp.uarray(n/t, np.sqrt(n)/t) - N_u

    if name=="Cu":
        tools.table((raw[0], raw[1], N), ("d/mm", "n", "(N-N_U)/\per\second"), "build/{}.tex".format(name), "Messdaten von {}.".format(name), "tab:daten{}".format(name), split=2, footer=r"$\Delta t = \SI{60}{s}$")#"(N-N_U)/\per\second"
    else:
        tools.table((raw[0], raw[1], raw[2], N), ("d/mm", "n", "\Delta t/s", "(N-N_U)/\per\second"), "build/{}.tex".format(name), "Messdaten von {}.".format(name), "tab:daten{}".format(name), split=2)
    mu = z * const.N_A / V_mol * 2 * np.pi * (const.e**2 / (4 * np.pi * const.epsilon_0 * const.m_e * const.c**2))**2 * ((1+eps)/eps**2 * ((2 * (1+eps))/(1+2*eps) - 1/eps * np.log(1+2*eps)) + 1/(2*eps) * np.log(1+ 2*eps) - (1+ 3*eps)/(1+2*eps)**2)

    params, pcov = curve_fit(fit, d, unp.nominal_values(N), sigma=unp.std_devs(N))
    params_ = unc.correlated_values(params, pcov)
    print("{}: N(0) = {}, µ = {}, µ_com = {}".format(name, params_[0], -params_[1], mu))

    sd = np.linspace(0, .07, 1000)

    valuesp = (fit(sd, *(unp.nominal_values(params_) + 10*unp.std_devs(params_)))).astype(float)
    valuesm = (fit(sd, *(unp.nominal_values(params_) - 10*unp.std_devs(params_)))).astype(float)

    #plt.xlim(0,7)
    plt.xlabel(r"$d/\si{mm}$")
    plt.ylabel(r"$N/\si{\per\second}$")
    plt.plot(1e3*sd, fit(sd, *params), 'b-', label="Fit")
    plt.fill_between(1e3*sd, valuesm, valuesp, facecolor='blue', alpha=0.125, edgecolor='none', label=r'$1\sigma$-Umgebung ($\times 10$)')
    plt.errorbar(1e3*d, unp.nominal_values(N), yerr=unp.std_devs(N), fmt='rx', label="Messdaten")
    plt.legend(loc='best')
    plt.yscale('linear')
    plt.tight_layout(pad=0)
    plt.savefig("build/{}.pdf".format(name))
    plt.yscale('log')
    plt.savefig("build/{}_log.pdf".format(name))
    plt.clf()

Cu = np.genfromtxt('daten/{}.txt'.format('Cu'), unpack=True, dtype=object)
Pb = np.genfromtxt('daten/{}.txt'.format('Pb'), unpack=True, dtype=object)

d1, n1 = Cu.astype(float)
t2, d2, n2 = Pb.astype(float)
N_u = unc.ufloat(917/900, np.sqrt(917)/900)

auswerten('Cu', d1, n1, 60, 29, 7.11e-6, 1.295, (Cu[0], Cu[1]))
auswerten('Pb', d2, n2, t2, 82, 18.26e-6, 1.295, (Pb[1], Pb[2], Pb[0]))
