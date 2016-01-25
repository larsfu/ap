
import matplotlib.pyplot as plt
import numpy as np
x = np.linspace (0, 5, 1000)
x,y =np.genfromtxt('auswertung/dispersion1.txt', unpack=True)
plt.plot(x,y,'rx',label="Messwerte")
plt.ylabel(r'$\omega  /\ \mathrm{kHz} $')
plt.xlabel(r'$\theta$')
plt.xlim(0,2.5)

L=1.75*10**-3
C=22*10**-9
plt.plot (x,(227921.1529*(1-np.cos(x))**(1/2)/1000),'b-',label="Theoriekurve")
plt.legend(loc='best')
plt.savefig('build/dispersion1.pdf')
