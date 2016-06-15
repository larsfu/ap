import numpy as np
import matplotlib.pyplot as plt

d, I1, I2, I3 = np.genfromtxt('daten/einzel.txt', unpack=True)
I1/=1e6
I2/=1e9
I3/=1e9
#I2/= I2.max() / I1.max()
#I3/= I3.max() / I1.max()
plt.plot(d, I1, 'rx', markersize=10)
plt.plot(d, I2, 'bx', markersize=10)
plt.plot(d, I3, 'gx', markersize=10)
plt.show()
plt.clf()


d, I = np.genfromtxt('daten/doppel.txt', unpack=True)
I/=1e9
plt.plot(d, I, 'rx', markersize=10)
plt.show()
