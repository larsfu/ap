import numpy as np
import matplotlib.pyplot as plt
import tools


delta = .5
d, a = np.genfromtxt('daten/a/1.dat', unpack=True)
plt.figure(figsize=(5.78,2.5))
plt.xlim(-1, 100)
plt.plot(d, a, 'b-')
plt.ylabel(r'echo intensity/arb.\,unit')
plt.xlabel(r'd/\si{\micro\second}')
plt.tight_layout(pad=0)
plt.savefig('build/a.pdf')

bla, t1, t2 = np.genfromtxt('daten/a/a.txt', unpack=True)
d1 = (t1-delta)*1e-6/2
d2 = (t2-delta)*1e-6/2
c = 2730
d1 *= c
d2 *= c
h = 80.04e-3
dia = h - d1 - d2

d_1, d_2 = np.genfromtxt('daten/mech.txt', unpack=True)
dia_ = h*1e3 - d_1 - d_2
la = np.array((b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'10', b'11'), dtype=object)

tools.table((la, 1e3*d2, 1e3*d1, 1e3*dia, d_1, d_2, dia_), (r"\text{Störstelle}", "d_1/mm", "d_2/mm", "2r/mm",  r"d_1^\text{mech}/mm", r"d_2^\text{mech}/mm", r"2r^\text{mech}/mm"), 'build/a.tex', r'Messergebnisse aus dem A-Scan. Neben den abgelesenen und berechneten Daten $d_n$ sind auch die zuvor mittels Messschieber bestimmten Abmessungen $d_n^\text{mech}$ eingetragen.', 'tab:a')


tools.table((la, t1, t2), (r"\text{Störstelle}", "t_1/\micro\second", "t_2/\micro\second"), "build/a_d.tex", "Messdaten zum A-Scan.", "tab:mess_a")

def abw(a, b):
    return 100* np.abs(a-b)/b

tools.table((la, abw(d2 , d_1/1e3), abw(d1, d_2/1e3), abw(dia, dia_/1e3)), (r"\text{Störstelle}", r"\Delta d_1/\percent", r"\Delta d_2/\percent", r"\Delta 2r/\percent"), 'build/diska.tex', 'Abweichungen beim A-Scan.', 'tab:diska', round_figures=(0,2,2,2))
