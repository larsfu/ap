import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

f, U, a, U0 = np.genfromtxt('daten/bc.txt', unpack=True)
a /= 1000

def A(f, RC):
    return 1 / np.sqrt(1+(2*np.pi*f)**2 * RC**2)

def phi(f, RC):
    return np.arctan(f*2*np.pi*RC)

phi_ = a / (1/f) * 2 * np.pi

paramsa, pcova = curve_fit(A, f, U/U0, p0=[1/742])
paramsb, pcovb = curve_fit(phi, f, phi_, p0=[1/742])

print(paramsa[0], paramsb[0])

x = np.linspace(0, 1000, 10000)
plt.plot(x, A(x, *paramsa), 'b-')
plt.plot(f, U/U0, 'rx')
plt.ylim(1e-1, 1.1)
plt.yscale('log')
plt.savefig('build/b1.pdf')
plt.clf()

plt.plot(f, phi_, 'rx', label='Phi')
plt.plot(x, phi(x, *paramsb), 'b-')
plt.legend()
plt.savefig('build/b2.pdf')
