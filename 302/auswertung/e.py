import numpy as np
import matplotlib.pyplot as plt

U_S = 2.08
ny_0 = 1142

ny, U_Br = np.genfromtxt("daten/e.txt", unpack=True)
U_Br /= 1000

q = U_Br / U_S
omega = ny/ny_0

plt.plot(omega, q, 'rx')
plt.xscale('log')
plt.savefig('build/e.pdf')
print(ny)
