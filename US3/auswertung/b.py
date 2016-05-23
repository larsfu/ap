import numpy as np
import matplotlib.pyplot as plt

d = np.genfromtxt("daten/b.txt", unpack=True, dtype=object)

t, delta_f1, I1, delta_f2, I2 = d.astype(float)
#plt.plot(t, delta_f1, 'x')
#plt.plot(t, delta_f2, 'x')
plt.plot(t, I1, 'x')
plt.plot(t, I2, 'x')
plt.savefig('build/b.pdf')
