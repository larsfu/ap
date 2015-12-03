import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

t, U1, U2 = np.genfromtxt("daten/d/LWAVE002.csv", unpack=True, delimiter=',')

plt.plot(t, U1*15, 'r-', markersize=0.1, label='U1', linewidth=0.2)
plt.plot(t, U2, 'b-', markersize=1, label='U2', linewidth=0.2)
plt.legend(loc='best')
#Glitches leugnen
plt.xlim(0, 0.0010)
plt.xlabel(r'$t/s$')
plt.ylabel(r'$U/V$')
#plt.plot(x, U(x, params[0], params[1]), 'b-', markersize=1)
plt.savefig('build/einplot.pdf')
