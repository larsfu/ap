import matplotlib.pyplot as plt
import numpy as np
x_syn = np.linspace (0, 17, 1000)
x,y =np.genfromtxt('auswertung/Uw.txt',unpack=True)
plt.plot(x,y,'rx',label="Messwerte")
plt.ylabel(r'$U \ \mathrm{in} \mathrm{V}$')
plt.xlabel(r'$n$')
plt.xlim(0,17)
plt.legend(loc='best')

plt.savefig('build/wellenwiderstand.pdf')
