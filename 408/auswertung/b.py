import numpy as np
import matplotlib.pyplot as plt
import tools
import scipy.stats

def auswerten(blende, linse1, linse2, schirm, name):
    e = blende-schirm
    d = linse2-linse1
    f = (e**2-d**2)/(4*e)
    print("{}: f = ({}+-{})mm".format(name, f.mean()*1e3, scipy.stats.sem(f)*1e3))
    return f

l1, l2, s = np.genfromtxt('daten/b1_o.txt', unpack=True)
l1 *= 1e-2
l2 *= 1e-2
s *= 1e-2

f1 = auswerten(129.9e-2, l1, l2, s, '100mm weiß')


s2, l3, l4, l5, l6 = np.genfromtxt('daten/b2.txt', unpack=True)
l3 *= 1e-2
l4 *= 1e-2
l5 *= 1e-2
l6 *= 1e-2
s2 *= 1e-2
x1 = 129.9e-2
x2 = 130.1e-2

lc = np.concatenate((l3, l5))
lb = np.concatenate((l4, l6))
e = np.concatenate((x1-s, np.tile(x2-s2, 2)))
b1 = np.concatenate((l1-x1, lb-x2))+e
b2 = np.concatenate((l2-x1, lc-x2))+e
g1 = e-b1
g2 = e-b2

f2 = auswerten(130.1e-2, l3, l4, s2, '100mm rot')
f3 = auswerten(130.1e-2, l5, l6, s2, '100mm blau')

tools.table((1e2*e, 1e2*b1, 1e2*g1, 1e2*b2, 1e2*g2, 1e3*np.concatenate((f1, f2, f3))), ("e/cm", "b_1/cm", "g_1/cm", "b_2/cm", "g_2/cm", "f/mm"), "build/b.tex", "Messreihe zur Bessel-Methode", "tab:b", interrows = {0:"Ohne Filter", 10:"Roter Filter", 15:"Blauer Filter"})
