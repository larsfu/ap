
import matplotlib.pyplot as plt
import numpy as np
x = np.linspace (0, 360)
x,y =np.genfromtxt('auswertung/ohnerauschen.txt',unpack=True)
plt.plot(x,y,'rx',label="Messwerte")
plt.xlabel(r'$\phi /\mathrm{°}$')
plt.ylabel(r'$U \ /\ \mathrm{V}$')

plt.plot (x,(2/np.pi)*22.8*np.cos(np.pi*x/180),'b-',label="Ausgangsspannung")
plt.legend(loc='best')
plt.savefig('build/plot.pdf')
