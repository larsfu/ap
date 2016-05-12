import numpy as np
import matplotlib.pyplot as plt
import tools

d = np.genfromtxt("daten/a.txt", unpack=True, dtype=object)
f, U_A = d.astype(float)

plt.plot(f, U_A, 'rx')
plt.savefig("build/a.pdf")
plt.clf()

tools.table(d, ("f/kHz", "U_A/mV"), "build/daten_a.tex", "Messdaten a.", "tab:mess_a")
