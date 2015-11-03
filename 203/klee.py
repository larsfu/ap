import matplotlib.pyplot as plt
import numpy as np



x = np.linspace(0, 2*np.pi, 1000)
x2 = np.linspace(0, 1.5*np.pi, 1000)
x3 = np.linspace(0,1, 2)


def sp(rad, offset):
    return np.linspace(np.pi/2 - 1/2*np.arcsin(rad) + offset, 1/2*np.arcsin(rad) + offset, 1000)


plt.polar(x, np.abs(np.sin(2*x)), 'g-', label='Glücksklee')
plt.polar(x2, (x2-np.pi/2)/2.2, 'g-')
plt.polar(np.repeat(np.pi/4, 2), x3, 'g-')
plt.polar(np.repeat(3*np.pi/4, 2), x3, 'g-')
plt.polar(np.repeat(1.25*np.pi, 2), x3, 'g-')
plt.polar(np.repeat(1.75*np.pi, 2), x3, 'g-')

for offset in range(0,4):
    for radius in range(1,5):
        plt.polar(sp(radius*0.2, offset*np.pi/2), np.repeat(radius*0.2, 1000), 'g-')


#plt.xlabel(r'$T^{-1}/\si{\per\kelvin}$')
#plt.ylabel(r'$p/\si{\pascal}$')
#plt.yscale('log', basey=np.e, subsy=np.exp(np.log10(np.arange(1,10))))
#plt.xlim(0.0027, 0.00307)
plt.legend()
#plt.grid(True, which='both')
#plt.yticks([np.e**-14, np.e**-13, np.e**-12, np.e**-11], [r'$\mathrm{e}^{-14}$', r'$\mathrm{e}^{-13}$', r'$\mathrm{e}^{-12}$', r'$\mathrm{e}^{-11}$'])
#plt.ylim(np.e**-14,np.e**-11)

plt.savefig('klee.png')
