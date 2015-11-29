import numpy as np
import matplotlib.pyplot as plt

U_S = 2.08
ny_0 = 1142

ny, U_Br = np.genfromtxt("daten/e.txt", unpack=True)
U_Br /= 1000

q = U_Br / U_S

def q_th(omega):
    return np.sqrt(1/9 * ((omega**2-1)**2)/((1-omega**2)**2 + 9 * omega**2))

omega = ny/ny_0

x = np.linspace(0.01, 100, 1000000)
plt.plot(x, q_th(x), 'b-')
plt.plot(omega, q, 'rx')
plt.xscale('log')
plt.xlabel(r'$\Omega$')
plt.ylabel(r'$\frac{U_\mathrm{Br}}{U_\mathrm{S}}$')
plt.savefig('build/e1.pdf')

plt.plot(x, q_th(x), 'b-')
plt.plot(omega, q, 'rx')
plt.xlabel(r'$\Omega$')
plt.xlim(0.9,1.12)
plt.ylim(0, 0.03)
plt.xscale('log', subsx=[2, 3, 4, 5, 6, 7, 8, 9])
plt.ylabel(r'$\frac{U_\mathrm{Br}}{U_\mathrm{S}}$')
plt.savefig('build/e2.pdf')


print(ny)
