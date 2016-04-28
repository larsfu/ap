import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as const
import scipy.stats as stats
import tools

U_h, I_h = np.genfromtxt("daten/a_heiz.txt", unpack=True)
I_s = np.genfromtxt("daten/i_s.txt")

f = 0.35e-4
eta = 0.28
T = np.power((U_h*I_h-0.9)/(f*eta*const.sigma), 0.25)
print(T)
Tr = T[2:]
print(Tr)
f = 0.35e-4
phi = - const.Boltzmann * Tr / const.e * np.log(I_s * const.h**3 / (4*np.pi * f * const.e * const.m_e * const.Boltzmann**2 * Tr**2))
print(phi.mean(), phi.std())

tools.table([U_h[::-1], I_h[::-1], T[::-1], I_s[::-1], phi[::-1]], ["U_H/V", "I_H/A","T/K", "I_S/mA", "\phi/\electronvolt"], "build/temp.tex", "tab:temp", "Abgeschätzte Kathodentemperaturen.")
