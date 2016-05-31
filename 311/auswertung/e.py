import numpy as np
import matplotlib.pyplot as plt

Ihy, Bhy = np.genfromtxt('daten/e.txt', unpack=True)
plt.plot(Ihy, Bhy, 'rx-', markersize=3, linewidth=0.5, label='Hysteresekurve')
plt.xlabel(r'$I/\si{A}$')
plt.ylabel(r'$B/\si{mT}$')
plt.legend(loc='best')
plt.savefig('build/hysterese.pdf')
