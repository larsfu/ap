import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from peakdetect import peakdetect

shit, shit, shit, t, U, shit = np.genfromtxt('daten/a/F0004CH1.CSV', delimiter=',', unpack=True)


start = 427
stop = 2298
t = t[start:stop] - t[start]
U = -U[start:stop]

extrema = peakdetect(U, t, 20)
maxs = np.array(extrema[0])
mins = np.array(extrema[1])
maxs_x = maxs[:,0]
maxs_y = maxs[:,1]
mins_x = mins[:,0]
mins_y = mins[:,1]

def envelope(t, tau, U):
    return U * np.exp(-t*tau)

paramsmax, pcovmax = curve_fit(envelope, maxs_x, maxs_y)
paramsmin, pcovmin = curve_fit(envelope, mins_x, mins_y)

print(paramsmax, paramsmin)

x = np.linspace(0, t[len(t)-1], 1000)
plt.xlim(0, 0.00074)
plt.plot(t, U, 'b-')
plt.plot(x, envelope(x, *paramsmax), 'r-')
plt.plot(x, envelope(x, *paramsmin), 'r-')
plt.plot(maxs[:,0], maxs[:,1], 'rx')
plt.plot(mins[:,0], mins[:,1], 'rx')

plt.savefig('build/a.pdf')
