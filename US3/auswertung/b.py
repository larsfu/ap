import numpy as np
import matplotlib.pyplot as plt
import tools

d = np.genfromtxt("daten/b.txt", unpack=True, dtype=object)
tools.table(d, (r"d/µs", r"\Delta f_1/Hz", r"I_1", r"\Delta f_2/Hz", r"I_2"), "build/datenb.tex", "Messdaten zum zweiten Versuchsteil.", "label", split=2)


t, delta_f1, I1, delta_f2, I2 = d.astype(float)

t/=1e6
alpha = np.pi/2 - np.arcsin(np.sin(15) * 18/27)
c_l = 1800
c_p = 2700

prism_time = 30.7e-3 / c_p
print(prism_time)
depth = np.zeros(len(t))
depth[t < prism_time] = t[t < prism_time] * c_p
depth[t >= prism_time] = prism_time * c_p + (t[t >= prism_time] - prism_time) * c_l


nu_0 = 2e6
v1 = -delta_f1 * c_l / nu_0 / 2 / np.cos(alpha)
v2 = -delta_f2 * c_l / nu_0 / 2 / np.cos(alpha)



plt.plot(depth*1e3, v1, 'x', label="70% Pumpenleistung")
plt.plot(depth*1e3, v2, 'x', label="45% Pumpenleistung")
plt.ylabel(r'$v/\si{\meter\per\second}$')
plt.xlabel(r'$d/\si{mm}$')
plt.legend(loc='best')
plt.savefig('build/b1.pdf')
plt.clf()

plt.plot(depth*1e3, I1, 'x', label="70% Pumpenleistung")
plt.plot(depth*1e3, I2, 'x', label="45% Pumpenleistung")
plt.ylabel(r'$I/1000\si{\volt\squared\per\second}$')
plt.xlabel(r'$d/\si{mm}$')
plt.legend(loc='best')
plt.savefig('build/b2.pdf')
plt.clf()
