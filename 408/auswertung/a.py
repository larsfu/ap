import numpy as np
import matplotlib.pyplot as plt
import tools
import scipy.stats

def auswerten(g, b, name, ignore):
    f = 1/(1/b + 1/g)


    plt.plot((0, b[0]), (g[0], 0), 'r-', label="Strahlen")
    for i in range(1, len(b)):
        if i in ignore:
            plt.plot((0, b[i]), (g[i], 0), '-', color='0.5', label="Strahl, nicht berücksichtigt")
        else:
            plt.plot((0, b[i]), (g[i], 0), 'r-')
    f_clean = np.delete(f, ignore)
    f_ = f_clean.mean()
    f_std = scipy.stats.sem(f_clean)
    print("f{} = ({}+-{})mm".format(name, f_*1e3, f_std*1e3))
    epsilon = 0.03
    plt.plot((f_, f_, 0), (0,f_, f_), 'b:', label="Brennpunkt")

    plt.xlabel(r'$g/\si{cm}$')
    plt.ylabel(r'$b/\si{cm}$')
    plt.legend()

    plt.xlim(f_-epsilon, f_+epsilon)
    plt.ylim(f_-epsilon, f_+epsilon)
    plt.tight_layout(pad=0)
    plt.savefig('build/a{}_zoom.pdf'.format(name))

    plt.xlim(0, 1.2)
    plt.ylim(0, 0.6 if name=='2' else 0.33)
    plt.plot((f_-epsilon, f_+epsilon, f_+epsilon, f_-epsilon, f_-epsilon), (f_-epsilon, f_-epsilon, f_+epsilon, f_+epsilon, f_-epsilon), 'k-', linewidth=0.5, label="Vergrößerter Ausschnitt")
    plt.legend()
    plt.tight_layout(pad=0)
    plt.savefig('build/a{}.pdf'.format(name))
    plt.clf()
    return f

g1, b1, B1, g2, b2 = np.genfromtxt('daten/a.txt', unpack=True)
g1 *= 1e-2
b1 *= 1e-2
B1 *= 1e-2
g2 *= 1e-2
b2 *= 1e-2

f1 = auswerten(g1, b1, '1', [3])
f2 = auswerten(g2, b2, '2', [])

V = b1/g1
print("V_1 = {}+-{}".format(V.mean(), scipy.stats.sem(V)))



V2 = B1/0.028
print("V_2 = {}+-{}".format(V2.mean(), scipy.stats.sem(V2)))

tools.table((1e2*B1, 1e2*g1, 1e2*b1, f1*1e3, V, V2), ("B/cm", "g/cm", "b/cm", "f/mm", "\sfrac{b_1}{g_1}","\sfrac{B}{G}"), "build/a.tex", "Messreihe zur Linse mit $f=\SI{150}{mm}$.", "tab:a1", split=1, round_figures=(3,4,4,4,4,4))
tools.table((1e2*g2, 1e2*b2, f2*1e3), ("g/cm", "b/cm", "f/mm"), "build/a2.tex", "Messreihe zur Linse mit $f=\SI{100}{mm}$.", "tab:a2", split=2)
