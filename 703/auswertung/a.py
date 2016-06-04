import numpy as np
import matplotlib.pyplot as plt

U, N, I = np.genfromtxt('daten/a.txt', unpack=True)
plt.plot(U, N, 'rx')
plt.xlabel("")
plt.savefig("build/a.pdf")
