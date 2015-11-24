import matplotlib.pyplot as plt
import numpy as np
x = np.linspace (0, 360, 1000)
x,y =np.genfromtxt('auswertung/mitrauschen.txt',unpack=True)
plt.plot(x,y,'rx',label="Messwerte")
plt.xlabel(r'$\phi /\mathrm{°}$')
plt.ylabel(r'$U \ /\ \mathrm{V}$')
plt.legend(loc='best')
plt.plot (x,2*(2/np.pi)*22.8*np.cos(np.pi*x/180),'g-',label="Ausgangsspannung")
plt.legend(loc='best')
plt.savefig('build/plot2.pdf')
