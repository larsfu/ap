import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress


gain = 1000
U_0 = -7.72

r, U = np.genfromtxt("auswertung/photodetektor.txt", unpack=True)

U = U/gain - U_0/gain

r_log = np.log(r)
U_log = np.log(U)

slope, intercept, r_value, p_value, std_dev = linregress(r_log, U_log)

plt.loglog(r, U, 'rx', label='Messdaten')
x = np.linspace(0.06, 2.1, 10000)
plt.xlim(0.06,2.1)
plt.xlabel(r'$r/\si{\meter}$')
plt.ylabel(r'$U_\mathrm{ber}/\si{\volt}$')
plt.loglog(x, np.exp(intercept)* x**slope, 'b-', label='Fit')
plt.savefig('build/plot3.pdf')
print(slope, intercept, std_dev, np.sqrt(std_dev**2 * np.mean(r_log**2)))
