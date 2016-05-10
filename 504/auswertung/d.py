import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as const
import scipy.stats as stats
import tools

U_h_, I_h_ = np.genfromtxt("daten/a_heiz.txt", unpack=True, dtype=object)
U_h = U_h_.astype(float)
I_h = I_h_.astype(float)
I_s_ = np.genfromtxt("daten/i_s.txt", dtype=object)
I_s = I_s_.astype(float) / 1e3

f = 0.35e-4
eta = 0.28
T = np.power((U_h*I_h-0.95)/(f*eta*const.sigma), 0.25)
#print(T)
#Tr = T[2:]
#print(Tr)
f = 0.35e-4
phi = - const.Boltzmann * T / const.e * np.log(I_s * const.h**3 / (4*np.pi * f * const.e * const.m_e * const.Boltzmann**2 * T**2))
print(phi.mean(), phi.std())

tools.table([U_h_[::-1], I_h_[::-1], T[::-1], I_s_[::-1], phi[::-1]], ["U_H/V", "I_H/A","T/K", "I_S/mA", "\phi/\electronvolt"], "build/d.tex", "Abgeschätzte Kathodentemperaturen.", "tab:temp")
