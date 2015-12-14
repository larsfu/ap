
import matplotlib.pyplot as plt
import numpy as np

x,y =np.genfromtxt('auswertung/dispersion2.txt',unpack=True)
plt.plot(x,y,'rx',label="Messwerte")
plt.ylabel(r'$\omega /\ \mathrm{Hz} $')
plt.xlabel(r'$\theta$')
x = np.linspace (0, 5, 1000)
plt.xlim(0,2.5)

L=1.75e-3
C=22e-9
D=9.39e-9

plt.plot(x,np.sqrt((1/L)*(1/C+1/D)+(1/L)*np.sqrt((1/C+1/D)**2-(4*np.sin(x)**2)/(C*D))) ,'g-',label="oberer Ast der Theoriekurve")

plt.plot(x,np.sqrt((1/L)*(1/C+1/D)-(1/L)*np.sqrt((1/C+1/D)**2-(4*np.sin(x)**2)/(C*D))) ,'b-',label="unterer Ast der Theoriekurve")



plt.legend(loc='best')
plt.savefig('build/dispersion2.pdf')
