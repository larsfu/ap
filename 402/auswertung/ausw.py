import numpy as np
import matplotlib.pyplot as plt

def n(eta):
    return np.sin ((np.deg2rad(60) + np.deg2rad(180-eta))/2)/np.sin(np.deg2rad(30))

l, r, la = np.genfromtxt('daten/daten.txt', unpack=True)
n_ = n(r-l)
print(n_)
plt.plot(la, n_**2, 'rx', markersize=10)
plt.show()
