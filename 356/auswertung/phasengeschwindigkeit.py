import matplotlib.pyplot as plt
import numpy as np

x,y =np.genfromtxt('auswertung/v-ph.txt',unpack=True)
plt.plot(x,y,'rx',label="Messwerte")
plt.ylabel(r'$v_{\mathrm{ph}} /\ \mathrm{kHz} $')
plt.xlabel(r'$\omega /\ \mathrm{kHz}$')
x = np.linspace (0, 350000, 1000)
plt.xlim(0,350)

L=1.75e-3
C=22e-9
x = x[(1-(L*C*0.5*x**2)) > -1][1:]
print(x/np.arccos((1-(L*C*0.5*x**2))))
plt.plot(x/1000, x/(np.arccos(1-(0.5*x**2*L*C))*1000),'b-', label="Theoriekurve")
#plt.plot(x, (x/(np.arccos()/1000,'b-', label="Theoriekurve")


plt.legend(loc='best')
plt.savefig('build/v-ph.pdf')
