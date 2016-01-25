import matplotlib.pyplot as plt
import numpy as np
x_syn = np.linspace (0, 18, 1000)
x,y =np.genfromtxt('auswertung/U2.txt',unpack=True)
plt.plot(x,y,'rx',label="Messwerte")
plt.ylabel(r'$U \ /\ \mathrm{V}$')
plt.xlabel(r'$n$')
plt.xlim(0,18)
plt.ylim(0,1.9)
plt.legend(loc='best')

plt.savefig('build/eigenschwingung2.pdf', format='PDF')
