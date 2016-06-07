import numpy as np
import matplotlib.pyplot as plt

U, N, I = np.genfromtxt('daten/a.txt', unpack=True)
plt.plot(U, N, 'rx',label="Messwerte")
plt.xlabel(r'Spannung $U$/V')
plt.ylabel(r'Impulszahl $n_\mathrm{Impulse}$')
plt.savefig("build/a.pdf")
