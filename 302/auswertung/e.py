import numpy as np
import matplotlib.pyplot as plt
import uncertainties as unc
import uncertainties.unumpy as unp
import pickle
from maketable import maketable

U_S = 2.08
ny_0 = 1142
R = unc.ufloat(332, 332*0.002)

ny, U_Br = np.genfromtxt("daten/e.txt", unpack=True)
C3 = pickle.load(open('build/c3.pickle', 'rb')) * 1e-9
ny_0_th = 1/(2*np.pi*C3*R)

maketable((R, C3*1e9, ny_0, ny_0_th, ny_0/ny_0_th), 'build/e.txt')
maketable((ny[:18].astype(int), U_Br[:18], ny[18:].astype(int), U_Br[18:]), 'build/e_mess.txt')

U_Br /= 1000

q = U_Br / U_S

def q_th(omega):
    return np.sqrt(1/9 * ((omega**2-1)**2)/((1-omega**2)**2 + 9 * omega**2))

omega = ny/ny_0

#Klirrfaktor
k = (U_Br[17] / q_th(2)) / U_S
print(k)



x = np.linspace(0.01, 100, 1000000)
plt.plot(x, q_th(x), 'b-', label='Theoretischer Wert')
plt.plot(omega, q, 'rx', label='Messwerte')
plt.xscale('log')
plt.xlabel(r'$\Omega$')
plt.ylabel(r'$U_\mathrm{Br}/U_\mathrm{S}$')
plt.legend(loc='best')
plt.savefig('build/e1.pdf')

plt.xticks([10**(x/100) for x in range(-10, 10)], [r"$10^{"+str(x/100)+r"}" for x in range(-10, 10)])
plt.xlim(0.9,1.12)
plt.ylim(0, 0.03)
plt.savefig('build/e2.pdf')
