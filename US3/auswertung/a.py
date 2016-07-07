import numpy as np
import matplotlib.pyplot as plt
import tools
import uncertainties.unumpy as unp

d = np.genfromtxt('daten/a.txt', dtype=object, unpack=True)
d_ = np.concatenate((d[1:4].T, d[4:7].T, d[7:10].T), axis=0).T

tools.table((np.tile(d[0], 3), *d_), ("\dot V / \percent", r"\Delta f_{\SI{30}{\degree}}/Hz", r"\Delta f_{\SI{15}{\degree}}/Hz", r"\Delta f_{\SI{60}{\degree}}/Hz"), "build/datena.tex", "Messdaten zum ersten Aufgabenteil.", "datena", interrows={0:r"$d=\SI{16}{mm}$", 5:r"$d=\SI{10}{mm}$", 10:r"$d=\SI{7}{mm}$"})

d_ = d.astype(float)
V = d_[0]
f = np.absolute(np.array([d_[1:4], d_[4:7], d_[7:10]]))
V /= 10
theta = np.radians(np.array((30, 15, 60)))
alpha = np.pi/2 - np.arcsin(np.sin(theta) * 18/27)

c_l = 1800
nu_0 = 2e6
v = f * c_l / nu_0 / 2 / np.cos(alpha)[np.newaxis, :, np.newaxis]

v_ = np.concatenate((v[0].T, v[1].T, v[2].T), axis=0).T
tools.table((np.tile(V, 3), *v_, unp.uarray(v_.mean(axis=0), v_.std(axis=0))), (r"\dot V/ \liter\per\minute", r"v_{\SI{30}{\degree}}/\meter\per\second", r"v_{\SI{15}{\degree}}/\meter\per\second", r"v_{\SI{60}{\degree}}/\meter\per\second", r"\bar v / \meter\per\second"), "build/a.tex", "Ergebnisse.", "tab:erg", round_figures=(1,3,3,3,3), interrows={0:r"$d=\SI{16}{mm}$", 5:r"$d=\SI{10}{mm}$", 10:r"$d=\SI{7}{mm}$"})

print((v_.std(axis=0) / v_.mean(axis=0)).mean() * 100)

for i in range(0, 3):
    plt.plot(v[:,i,:], f[:,i,:]/np.cos(alpha)[i], 'rx')
    plt.xlabel(r'$v/\si{\meter\per\second}$')
    plt.ylabel(r'$\Delta \nu / \cos \alpha / \si{\per\second}$')
    plt.tight_layout()
    plt.savefig('build/a{}.pdf'.format(i))
    plt.clf()
