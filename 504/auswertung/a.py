import numpy as np
import matplotlib.pyplot as plt

d = np.genfromtxt('daten/a.txt', unpack=True)
U = d[0]
I = d[1:6]

for i in I:
    plt.plot(U, i, 'x')
plt.xlabel("U/V")
plt.ylabel("I/mA")
plt.savefig("build/kennlinien.pdf")
