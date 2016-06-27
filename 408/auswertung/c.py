import numpy as np
import matplotlib.pyplot as plt
import uncertainties as unc
import uncertainties.unumpy as unp
import tools

def linregress(x, y):
    assert len(x) == len(y)

    x, y = np.array(x), np.array(y)

    N = len(y)
    Delta = N * np.sum(x**2) - (np.sum(x))**2

    A = (N * np.sum(x * y) - np.sum(x) * np.sum(y)) / Delta
    B = (np.sum(x**2) * np.sum(y) - np.sum(x) * np.sum(x * y)) / Delta

    sigma_y = np.sqrt(np.sum((y - A * x - B)**2) / (N - 2))

    A_error = sigma_y * np.sqrt(N / Delta)
    B_error = sigma_y * np.sqrt(np.sum(x**2) / Delta)

    return A, A_error, B, B_error

B, y, z = np.genfromtxt('daten/c.txt', unpack=True)
B *= 1e-2
y *= 1e-2
z *= 1e-2

x = 129.4e-2
G = 2.8e-2

g_ = x-z
b_ = x-y-g_

V = B/G

tools.table((1e2*B, V, 1e2*g_, 1e2*b_), ("B/cm", "V", "g'/cm", "b'/cm"), "build/c.tex", "Messreihe zur Abbe-Methode.", "tab:c", split=2, round_figures=(3,4,4,4))

m1, m1_, n1, n1_ = linregress((1+1/V), g_)
m2, m2_, n2, n2_ = linregress((1+V), b_)
x = np.linspace(1.0, 2.6)

print("f1 = {}+-{}mm, f2 = {}+-{}mm".format(m1*1e3, m1_*1e3, m2*1e3, m2_*1e3))
print("h = {}+-{}cm, h' = {}+-{}cm".format(n1*1e2, n1_*1e2, n2*1e2, n2_*1e2))
f1 = unc.ufloat(m1, m1_)
f2 = unc.ufloat(m2, m2_)
f = (f1+f2)/2
ft = 1/(1/100e-3 + 1/-100e-3 - 6e-2/(100e-3*-100e-3))
print("Bestimmte Brennweite: f = {}mm, Theoretische Brennweite: f_t = {}mm".format(f*1e3, ft*1e3))

plt.figure(figsize=(5.6, 3.2))
plt.xlim(1,2.6)
plt.xlabel(r'$1+\frac{1}{V}$')
plt.ylabel(r"$g'/\si{cm}$")
plt.plot(x, x*m1+n1, 'b-', label='Lineare Regression')
plt.plot((1+1/V), g_, 'rx', label='Messdaten')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig("build/c1.pdf")
plt.clf()
x = np.linspace(1, 6)
plt.xlim(1,6)
plt.xlabel(r'$1+V$')
plt.ylabel(r"$b'/\si{cm}$")
plt.plot(x, x*m2+n2, 'b-',label='Lineare Regression')
plt.plot((1+V), b_, 'rx', label='Messdaten')
plt.legend(loc='best')
plt.tight_layout(h_pad=-1)
plt.savefig("build/c2.pdf")
