import numpy as np
import matplotlib.pyplot as plt
import uncertainties as unc
from scipy.stats import linregress
from scipy.optimize import curve_fit

def A(f, R, L, C):
    omega = 2*np.pi*f
    return 1 / np.sqrt(omega**4 * L**2 * C**2 + omega**2 * R**2 * C**2 - 2*omega**2 *L*C +1)

def analyze(f, x, y, pixels_per_unit, offset, first_value_x, name, index):
    slope, intercept, p_value, r_value, std_dev = linregress(np.linspace(0, len(f)-1, len(f)), np.log(f))

    x_fixed = (x - offset - first_value_x) / pixels_per_unit
    x_fixed = np.exp(intercept) * np.exp(slope * x_fixed / np.log(np.e))
    y = y / np.amax(y) * 1.1
    print()
    x_fixed /= 1000

    a = len(y)-np.argmax(y[::-1] >= 1/np.sqrt(2))
    print('Resonanzfrequenz {}: {}kHz'.format(name, x_fixed[a]))

    plt.plot(x_fixed, y, 'r-', label='Durchlasskurve')
    plt.plot((x_fixed[a], x_fixed[a]), (0, y[a]), 'k-', label='Resonanzfrequenz')
    plt.legend(loc='best')
    plt.ylim(0,1.1)
    plt.xlim(np.min(x_fixed), (60, 72)[index])
    plt.xlabel('f/kHz')
    plt.ylabel('U / willk. Einh.')
    plt.savefig('build/'+name+'.pdf')
    plt.clf()

f1, f2 = np.genfromtxt('daten/a.txt', unpack=True)
f1 *= 1000
f2 *= 1000
x1, y1 = np.genfromtxt('daten/a1_raw.txt', unpack=True)
x2, y2 = np.genfromtxt('daten/a2_raw.txt', unpack=True)

analyze(f1, x1, y1, 473, 52, 188, 'a1', 0)
analyze(f2, x2, y2, 2359/5, 0, 262, 'a2', 1)
