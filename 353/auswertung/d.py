import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

data = (np.genfromtxt("daten/d/LWAVE001.csv", delimiter=','),
    np.genfromtxt("daten/d/LWAVE002.csv", delimiter=','),
    np.genfromtxt("daten/d/LWAVE003.csv", delimiter=','))

for i in range(0,3):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ln1 = ax1.plot(data[i].T[0], data[i].T[1], 'r-', markersize=0.1, label='$U_1$', linewidth=0.2)
    ln2 = ax2.plot(data[i].T[0], data[i].T[2], 'b-', markersize=1, label='$U_2$', linewidth=0.2)
    lns = ln1+ln2
    labs = [l.get_label() for l in lns]
    plt.legend(lns, labs, loc='upper right')
    #Glitches leugnen
    plt.xlim(0, (0.0010, 0.001, 0.0008)[i])
    ax1.set_xlabel(r'$t/s$')
    ax1.set_ylabel(r'$U_1/V$')
    ax2.set_ylabel(r'$U_2/V$')
    #plt.plot(x, U(x, params[0], params[1]), 'b-', markersize=1)
    plt.savefig('build/d'+str(i+1)+'.pdf')
    plt.clf()
