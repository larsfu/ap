import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from scipy.stats import linregress
from scipy.constants.constants import C2K
from scipy.optimize import curve_fit
import scipy.signal as signal
import peakdetect
import scipy.constants as const
import scipy
'''
data = np.genfromtxt("dynamisch_1.txt", unpack=True)
data[0] /= 2
data2 = np.genfromtxt("dynamisch_2.txt",  usecols=(1,2,3,4), unpack=True)
data2 = C2K(data2)
data[1] = C2K(data[1])
data[2] = C2K(data[2])
data[3] = C2K(data[3])
data[4] = C2K(data[4])

data[1] = data[3]
data[2] = data[4]

#data[1] = np.sin(1/80 * 2*np.pi*data[0]) + 298 + 0.01 * data[0]
#print(data2)
#data =  data, )
#t, T5, T6, T7, T8 = np.genfromtxt("statisch_2.txt", unpack=True)
#print(np.concatenate(data, data2), axis=1)
m=0.8
plt.plot(data[0], data[1], '.', label='T1 (Messing, schmal)', markersize=m)
plt.plot(data[0], data[2], '.', label='T2 (Messing, schmal)', markersize=m)
#plt.plot(data[0], data[2]-data[1]+297, '.', label='T2-T1', markersize=m)
#plt.plot(data[0], data[3], '.', label='T3', markersize=m)
#plt.plot(data[0], data[4], '.', label='T4', markersize=m)
#plt.plot(data[0], data2[0], '.', label='T5', markersize=m)
#plt.plot(data[0], data2[1], '.', label='T6', markersize=m)
#plt.plot(data[0], data2[2], '.', label='T7', markersize=m)
#plt.plot(data[0], data2[3], '.', label='T8', markersize=m)


maxs1 = peakdetect.peakdetect(data[1], data[0], 20)
maxs2 = peakdetect.peakdetect(data[2], data[0], 20)



def f(x, a, b, c):
    return a * np.log(b * x + c)
#    return a * x + b

#def F(x,a,b,c):
#    return a*((b*x+c) * np.log(b*x+c)-b*x)/b

#print(list(zip(*maxs2[0]))[0])
params1_high, pcov = curve_fit(f, list(zip(*maxs2[0]))[0], list(zip(*maxs2[0]))[1], maxfev=10000)
params1_low, pcov = curve_fit(f, list(zip(*maxs2[1]))[0], list(zip(*maxs2[1]))[1], maxfev=10000)
params2_high, pcov = curve_fit(f, list(zip(*maxs1[0]))[0], list(zip(*maxs1[0]))[1], maxfev=10000)
params2_low, pcov = curve_fit(f, list(zip(*maxs1[1]))[0], list(zip(*maxs1[1]))[1], maxfev=10000)
#print(params)

def mitte1(x):
    return (f(x, *params1_high) + f(x, *params1_low)) / 2

def mitte2(x):
    return (f(x, *params2_high) + f(x, *params2_low)) / 2


plt.plot(data[0], mitte1(data[0]), 'g--')
plt.plot(data[0], mitte2(data[0]), 'b--')

x = np.linspace(0, 600, 1000)
#plt.plot(x, f(x, *params1_high), 'g-')
#plt.plot(x, f(x, *params2_high), 'b-')
#plt.plot(data[0], data[1]-f(data[0], *params1_low)+300, 'b-', label='gekippt')
#plt.plot(data[0], data[2]-f(data[0], *params2_low)+300, 'g-')


deltax = 0.03

amplitude1 = F(50, *params1_high) - F(500, *params1_low) / 450
amplitude2 = F(50, *params2_high) - F(500, *params2_low) / 450

mean_amp_ratio = amplitude1/amplitude2


as1 = []
as2 = []
for a in maxs2:
    for b in a:
        as1.append(np.abs(mitte1(b[0])-b[1]))
        plt.plot((b[0], b[0]), (mitte1(b[0]), b[1]), '-', color='0.7')

for a in maxs1:
    for b in a:
        as2.append(np.abs(mitte2(b[0])-b[1]))
        plt.plot((b[0], b[0]), (mitte2(b[0]), b[1]), '-', color='0.7')

'''
deltax = 0.03
as2 = np.array((1.4, 1.9, 1.8, 1.6, 1.9, 1.6, 1.9, 1.8, 1.9, 1.7, 1.9, 1.8, 1.8, 1.75, 1.75, 1.7, 1.7, 1.75, 1.6, 1.85, 1.5))
as1 = np.array((0.25, 0.2, 0.2, 0.175, 0.2, 0.3, 0.2, 0.3, 0.2, 0.25, 0.17, 0.3, 0.2, 0.25, 0.1, 0.3, 0.2, 0.23, 0.2, 0.25, 0.18))
as1 *= (5/2.7)
as2 *= (5/2.7)
a1 = np.mean(as1)
a2 = np.mean(as2)
mean_amp_ratio = a2/a1
ttt = np.array((0.4, 0.35, 0.5, 0.35 ,0.5, 0.4, 0.58, 0.35, 0.5, 0.35, 0.6, 0.4, 0.5, 0.3, 0.5, 0.4, 0.4, 0.35, 0.6, 0.4, 0.4))
ttt *= 242/2
delta_t = np.mean(ttt)
print(a2, np.std(as2), a1, np.std(as1), delta_t, np.std(ttt))

rho = 8000
c = 400
const = rho * c * deltax**2
kappa = const /(2*delta_t * np.log(mean_amp_ratio))
dev = np.sqrt((const/(2*delta_t**2 * np.log(mean_amp_ratio)))**2 * np.std(ttt)**2 +
(const/(2*delta_t*np.log(mean_amp_ratio)**2*a2))**2 * np.std(as2)**2 +
(const/(2*delta_t*np.log(mean_amp_ratio)**2*a1))**2 * np.std(as1)**2)

print('κ=({} ± {}) W/(m K)'.format(kappa, dev))
#print(maxs2)
'''
plt.plot(*zip(*maxs1[0]), 'rx')
plt.plot(*zip(*maxs2[0]), 'rx')
plt.plot(*zip(*maxs1[1]), 'rx')
plt.plot(*zip(*maxs2[1]), 'rx')

plt.xlim(0,1121/2)
plt.xlabel(r'$t/\si{\second}$')
plt.ylabel(r'$T/\si{\kelvin}$')
#plt.yscale('log', basey=np.e, subsy=np.exp(np.log10(np.arange(1,10))))
#plt.xlim(0.0027, 0.00307)
plt.legend(loc='best')
plt.grid(True, which='both')
#plt.yticks([np.e**-14, np.e**-13, np.e**-12, np.e**-11], [r'$\mathrm{e}^{-14}$', r'$\mathrm{e}^{-13}$', r'$\mathrm{e}^{-12}$', r'$\mathrm{e}^{-11}$'])
plt.ylim(297,315.5)

plt.savefig('204_plot1.pdf')
plt.clf()


plt.plot(data[0], data2[2]-data2[3], 'rx', label='T7–T8')
plt.xlabel(r'$t/\si{\second}$')
plt.ylabel(r'$\Delta T/\si{\kelvin}$')
plt.legend(loc='best')
plt.grid(True, which='both')

plt.savefig('204_plot2.pdf')
plt.clf()

plt.plot(data[0], data[2]-data[1], 'rx', label='T2–T1')
plt.xlabel(r'$t/\si{\second}$')
plt.ylabel(r'$\Delta T/\si{\kelvin}$')
plt.legend(loc='best')
plt.grid(True, which='both')

plt.savefig('204_plot3.pdf')
plt.clf()

x = np.linspace(1/C2K(35),1/C2K(105),100)
plt.plot(x, np.exp(x*slope+intercept), 'b-', label='Lineare Regression')
plt.plot(T, np.exp(p), 'rx', label='Messdaten')

plt.xlabel(r'$T^{-1}/\si{\per\kelvin}$')
plt.ylabel(r'$p/\si{\pascal}$')
plt.yscale('log', basey=np.e, subsy=np.exp(np.log10(np.arange(1,10))))
plt.xlim(0.0027, 0.00307)
plt.legend()
plt.grid(True, which='both')
plt.yticks([np.e**9, np.e**10, np.e**11, np.e**12], [r'$\mathrm{e}^{9}$', r'$\mathrm{e}^{10}$', r'$\mathrm{e}^{11}$', r'$\mathrm{e}^{12}$'])
plt.ylim(np.e**9,np.e**12)

plt.savefig('203_plot.pdf')
'''
