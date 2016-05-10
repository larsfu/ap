import numpy as np
import matplotlib.pyplot as plt
import uncertainties as unc
import scipy.constants as const
from scipy.stats import linregress
import tools

d = np.genfromtxt("daten/a.txt", unpack=True, dtype=object)
lambd, gamma = d.astype(float)
lambd /= 1e9
gamma = np.deg2rad(400-gamma)
alpha = np.deg2rad(400-337.8)
beta = np.pi/2 - alpha/2

phi = gamma - alpha/2 - np.pi/2

g = lambd / (np.sin(beta) + np.sin(phi))

tools.table((*d, phi, g*1e9), ("\lambda/nm", "\gamma/\degree", "\phi/rad", "g/nm"), "build/a.tex", "Messdaten und Ergebnisse aus dem ersten Aufgabenteil.", "tab:a")

print (np.rad2deg(phi))
g = unc.ufloat(g.mean(), g.std())
print(g*1e9)

slope, intercept, r_value, p_value, std_err = linregress(lambd, np.sin(phi))
lambda_synth = np.linspace(400/1e9, 750/1e9)
print(1/unc.ufloat(slope, std_err)*1e9)
print(-intercept, beta)
#g = unc.ufloat(1/slope, 1/std_err)

plt.plot(lambda_synth*1e9, slope*lambda_synth + intercept, label="Lineare Regression")
plt.plot(lambd*1e9, np.sin(phi), 'rx', label="Messdaten")
plt.legend(loc='best')
plt.xlabel(r"$\lambda/\si{nm}$")
plt.ylabel(r"$\sin \phi$")
plt.savefig('build/a.pdf')


delta_lambda, delta_t = np.genfromtxt('daten/b.txt', unpack=True)
delta_lambda /= 1e9
phi12 = np.array([np.mean(phi[3:5]), np.mean(phi[7:9])])
eich = delta_lambda / (delta_t * np.cos(phi12))
tools.table((delta_lambda*1e9, delta_t, phi12, eich), (r"\Delta\lambda/nm", r"\Delta t/Skt.", r"\overline{\phi_{1,2}}/rad", r"\Delta\lambda/(\Delta t \cos \overline{\phi_{1,2}})"), "build/b.tex", "Eichmessung des Okularmikrometers.", "tab:b", round_figures=(2,3,4,4))
eich = unc.ufloat(eich.mean(), eich.std())
print("Eichgröße b) : {}".format(eich))

d = np.genfromtxt('daten/cd.txt', unpack=True, dtype=object)
gammab, delta_s, z, n, l = d.astype(float)

gammab = np.deg2rad(400-gammab)
phib = gammab - alpha/2 - np.pi/2
lambdab = g * (np.sin(beta) + np.sin(phib))
print(lambdab)

delta_lambd = eich * delta_s * np.cos(phib)
print(delta_lambd)

delta_E_D = const.h * const.c * delta_lambd/(lambdab**2) / const.e
print(delta_E_D)

sigma_2 = z - (l*(l+1) * delta_E_D * n**3 / (const.Rydberg * const.h * const.c / const.e * const.alpha**2))**0.25
print(sigma_2)

tools.table((gammab, phib, lambdab*1e9, delta_lambd*1e9, delta_E_D*1e3, sigma_2), (r"\gamma/rad", r"\phi/rad", r"\lambda/nm", r"\Delta\lambda/nm", "\Delta E_D/\milli\electronvolt", "\sigma_2"), "build/erg.tex", "Tabelle der Messergebnisse.", "tab:erg", round_figures=(4,4,3,3,3,4), interrows={0:"Natrium", 4:"Kalium", 7:"Rubidium"})
