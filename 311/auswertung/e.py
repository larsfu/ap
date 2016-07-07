import numpy as np
import matplotlib.pyplot as plt
import tools

d = np.genfromtxt('daten/e.txt', unpack=True, dtype=object)
Ihy, Bhy = d.astype(float)
plt.figure(figsize=(5.78,3.4))
plt.plot(Ihy, Bhy, 'rx-', markersize=3, linewidth=0.5, label='Hysteresekurve')
plt.xlabel(r'$I/\si{A}$')
plt.ylabel(r'$B/\si{mT}$')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/hysterese.pdf')

tools.table(d, ('I/A', 'B/mT'), 'build/e.tex', 'Messdaten, Hysteresekurve.', 'de', split=3)
