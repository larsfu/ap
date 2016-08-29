import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy.stats
import uncertainties as unc
import uncertainties.unumpy as unp
import tools

t = np.array((1.2, 2.7, 4.2, 5.8, 7.3, 8.7, 10.2, 11.8, 13.4, 15, 16.5, 18, 19.6, 21.1, 22.7, 24.2))
zeit = np.array((2, 2.5,  2.7,   3,   3,   3.1,   3.2,    3,    2.8,    2.7,  3.1,    3.1,  2.3,    2.7,    2.9,    2.9))

dt = np.diff(t)
f = 1/unc.ufloat(np.mean(dt), scipy.stats.sem(dt))
print("f = {}/min = {} Hz".format(f*60, f))

c = 1480
R = 45.6e-3
d = 48.4-16.2
d *= 0.5e-6
d *= c

V = np.pi / 3 * d**2 * (3 * R - d)

print(d, V*1e6, 1e6*V * f)
c = 1480



d = 44-unc.ufloat(zeit.mean(), scipy.stats.sem(zeit))
d *= 0.5e-6
d *= c
V = np.pi / 3 * d**2 * (3 * R - d)
tools.table((t, zeit), ('t/s', 'd/µs'), 'build/tm.tex', 'Messergebnisse des Herzmodells.', 'tab:tm', split=2)
print(unc.ufloat(zeit.mean(), scipy.stats.sem(zeit)), d*1e2, V*1e6, 1e6*V * f)

d = np.genfromtxt('daten/tm/scan.dat', unpack=True)
#plt.figure(figsize=(5.78, 2.7))
plt.imshow(d, cmap=cm.inferno_r, extent=(0,25, 100, 0), aspect='auto')
plt.ylim(100, -0.5)
plt.xlabel(r"$t/s$")
plt.ylabel(r"$d/\si{\micro\second}$")

for siegmannistdoof in zip(t, zeit):
    plt.plot((siegmannistdoof[0], siegmannistdoof[0]), (0, siegmannistdoof[1]), 'r_')
    plt.plot((siegmannistdoof[0], siegmannistdoof[0]), (0, siegmannistdoof[1]), 'r-')


plt.plot((),(), 'r-', label='Gemessene Längen')
plt.plot((0, 25), (44, 44), 'r:', alpha=0.7, label='ESV')
#plt.plot((0, 25), (3, 3), 'r-.', label='EDV')
plt.colorbar(label='echo intensity / arb.\,unit')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/tm.pdf')
plt.xlim(10,15)
plt.savefig('build/tm_zoom.pdf')
