import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

c = 1480
R = 45.6e-3
d = 48.4-16.2
d *= 0.5e-6
d *= c

V = np.pi / 3 * d**2 * (3 * R - d)

print(d, V*1e6, 1e6*V * 0.64)
c = 1480
d = 44-3
d *= 0.5e-6
d *= c
V = np.pi / 3 * d**2 * (3 * R - d)

print(d, V*1e6, 1e6*V * 0.64)


d = np.genfromtxt('daten/tm/scan.dat', unpack=True)
plt.figure(figsize=(5.78, 2.7))
plt.imshow(d, cmap=cm.inferno_r, extent=(0,25, 100, 0), aspect='auto')
plt.xlabel(r"$t/s$")
plt.ylabel(r"$d/\si{\micro\second}$")
plt.plot((0, 25), (44, 44), 'r--', label='ESV')
plt.plot((0, 25), (3, 3), 'r-.', label='EDV')
plt.colorbar(label='echo intensity / arb.\,unit')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/tm.pdf')
plt.xlim(10,15)
plt.savefig('build/tm_zoom.pdf')
