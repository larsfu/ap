import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import tools

def draw_lines(x, d, black=False):
    for e in zip(x, d):
        if black==False:
            plt.plot((e[0], e[0]), (0, e[1]), 'r-')
        else:
            plt.plot((e[0], e[0]), (0, e[1]), 'k-', linewidth=2)


d = np.genfromtxt('daten/b/1.dat', unpack=True)
plt.figure(figsize=(5.78, 3.3))
plt.imshow(d, cmap=cm.inferno, extent=(0,1, 100, 0), aspect='auto')
plt.ylim(60, 0)
plt.xlabel(r'$x/$arb.\,unit')
plt.ylabel(r"$t/\si{\micro\second}$")


x = (0.08, 0.10, 0.18, 0.27, 0.39, 0.47, 0.6, 0.7, 0.8, 0.93, 0.9)
d1 = np.array((14.5 , 13.,  45.,  39.5, 34,  28.8, 22.5,17.2, 11, 5.2,  41))
plt.plot((), (), 'r-', label='Abgemessene Längen')
draw_lines(x, d1)
plt.legend(loc='best')
plt.colorbar(label='echo intensity / arb.\,unit')
plt.tight_layout(pad=0)
plt.savefig('build/b1.pdf')
plt.clf()

d = np.genfromtxt('daten/b/2.dat', unpack=True)
plt.figure(figsize=(5.78, 3.3))
plt.imshow(d, cmap=cm.inferno, extent=(0,1, 100, 0), aspect='auto')
plt.ylim(60, 0)
plt.xlabel(r'$x/$arb.\,unit')
plt.ylabel(r"$t/\si{\micro\second}$")

x = (0.08, 0.10, 0.17, 0.27, 0.36, 0.45, 0.53, 0.62, 0.71, 0.81, 0.87)
d2 = np.array((44,   45,   10,   16,   22,   28.5,   34.5,   40,   46, 52.5,   11))

plt.plot((), (), 'r-', label='Abgemessene Längen')
draw_lines(x, d2)
plt.legend(loc='best')
plt.colorbar(label='echo intensity / arb.\,unit')
plt.tight_layout(pad=0)
plt.savefig('build/b2.pdf')
plt.clf()

plt.imshow(d, cmap=cm.flag, extent=(0,1, 100, 0), aspect='auto')
plt.ylim(60, 0)
draw_lines(x, d2, black=True)
plt.xlabel(r'$x/$arb.\,unit')
plt.ylabel(r"$d/\si{\micro\second}$")
plt.colorbar(label='echo intensity / arb.\,unit')
plt.plot((), (), 'k-', linewidth=2, label='Abgemessene Längen')
plt.legend(loc='best')
plt.tight_layout(pad=0)
plt.savefig('build/b3.pdf')


d1 = (d1)*1e-6/2
d2 = (d2)*1e-6/2
c = 2730
d1 *= c
d2 *= c
h = 80.04e-3
dia = h - d1 - d2
la = np.array((b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'10', b'11'), dtype=object)

d_1, d_2 = np.genfromtxt('daten/mech.txt', unpack=True)
dia_ = h*1e3 - d_1 - d_2

tools.table((la, 1e3*d1, 1e3*d2, 1e3*dia, d_1, d_2, dia_), (r"\text{Störstelle}", "d_1/mm", "d_2/mm", "2r/mm",  r"d_1^\text{mech}/mm", r"d_2^\text{mech}/mm", r"2r^\text{mech}/mm"), 'build/b.tex', r'Messergebnisse aus dem B-Scan.', 'tab:b')


def abw(a, b):
    return 100* np.abs(a-b)/b

tools.table((la, abw(d1 , d_1/1e3), abw(d2, d_2 /1e3), abw(dia, dia_/1e3)), (r"\text{Störstelle}", r"\Delta d_1/\percent", r"\Delta d_2/\percent", r"\Delta 2r/\percent"), 'build/diskb.tex', 'Abweichungen beim B-Scan.', 'tab:diskb', round_figures=(0,2,2,2))
