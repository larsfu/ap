import matplotlib.pyplot as plt
import numpy as np

x,y =np.genfromtxt('auswertung/v-ph.txt',unpack=True)
plt.plot(x,y,'rx',label="Messwerte")
plt.ylabel(r'$v_{\mathrm{ph}} /\ \mathrm{kHz} $')
plt.xlabel(r'$\omega /\ \mathrm{kHz}$')
x = np.linspace (0, 350000, 1000)
plt.xlim(0,350)

L=1.75*10**-3
C=22*10**-9

plt.plot(x, x/(np.arccos(1-(0.5*x**2*L*C))*1000),'b-', label="Theoriekurve")

plt.legend(loc='best')
plt.savefig('build/v-ph.pdf')
