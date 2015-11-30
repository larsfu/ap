import numpy as np
import uncertainties.unumpy as unp
import uncertainties as unc
from maketable import maketable
import pickle

def mittel(arr):
    #TODO: FEHLERRECHNUNG?!
    return unc.ufloat(np.mean(unp.nominal_values(arr)), np.std(unp.nominal_values(arr)))

#Genauigkeiten (relativ)
uncertainty_r3r4 = 0.0005
uncertainty_2 = 0.0002
uncertainty_r2 = 0.03

a = np.genfromtxt("daten/a.txt", unpack=True)
b = np.genfromtxt("daten/b.txt", unpack=True)
b[0] *= 1e-9
c = np.genfromtxt("daten/c.txt", unpack=True)
c[0] *= 1e-3
d = np.genfromtxt("daten/d.txt", unpack=True)
d[0] *= 1e-9

#Daten exportieren
maketable((a[0][:3], a[1][:3], a[2][:3], a[1][3:], a[2][3:]), 'build/a_mess.txt')
maketable((b[0][:3]*1e9, b[1][:3], b[2][:3], b[3][:3], b[0][3:]*1e9, b[1][3:], b[2][3:], b[3][3:]), 'build/b_mess1.txt')
maketable((b[0][6:]*1e9, b[1][6:], b[2][6:], b[3][6:]), 'build/b_mess2.txt')
maketable((c[0]*1e3, *c[1:]), 'build/c_mess.txt')
maketable((d[0]*1e9, *d[1:]), 'build/d_mess.txt')


#### Wheatstone-Brücke
R3R4 = unp.uarray(a[1] / a[2], a[1]/a[2] * uncertainty_r3r4)
R2 = unp.uarray(a[0], a[0]*uncertainty_2)
Rx = R2 * R3R4

#TODO: Fehlerrechnung?
R10 = mittel(Rx[0:3])
R12 = mittel(Rx[3:6])

maketable((R2, R3R4[0:3], Rx[0:3], R3R4[3:6], Rx[3:6]), 'build/a1.txt')
maketable((R10, r'\multicolumn{2}{c}{}', R12), 'build/a2.txt')

### Kapazitätsmessbrücke
R3R4 = unp.uarray(b[2] / b[3], b[2]/b[3] * uncertainty_r3r4)
C2 = unp.uarray(b[0], b[0] * uncertainty_2)
R2 = unp.uarray(b[1], uncertainty_r2 * b[1])

Rx = R2 * R3R4
Cx = C2 * 1/(R3R4)

#TODO: Fehlerrechnung?
R1 = mittel(Rx[0:3])
R3 = mittel(Rx[3:6])
R9 = mittel(Rx[6:9])
C1 = mittel(Cx[0:3])*1e9
C3 = mittel(Cx[3:6])*1e9
C9 = mittel(Cx[6:9])*1e9

#C3 für die Auswertung der Wien-Robinson-Brücke gesondert speichern
pickle.dump(C3, open('build/c3.pickle', 'wb'))

maketable((C2[0:3]*1e9, R2[0:3], R3R4[0:3], Rx[0:3], Cx[0:3]*1e9), 'build/b1.txt')
maketable((C2[3:6]*1e9, R2[3:6], R3R4[3:6], Rx[3:6], Cx[3:6]*1e9), 'build/b2.txt')
maketable((C2[6:9]*1e9, R2[6:9], R3R4[6:9], Rx[6:9], Cx[6:9]*1e9), 'build/b3.txt')
maketable((('Wert 1', 'Wert 3', 'Wert 9'),(R1, R3, R9),(C1, C3, C9)), 'build/b4.txt')

#Induktivitätsmessbrücke
R3R4 = unp.uarray(c[2] / c[3], c[2]/c[3] * uncertainty_r3r4)
L2 = unp.uarray(c[0], c[0] * uncertainty_2)
R2 = unp.uarray(c[1], uncertainty_r2 * c[1])

Rx = R2 * R3R4
Lx = L2 * R3R4

R16 = mittel(Rx)
L16 = mittel(Lx)

maketable((L2*1e3, R2, R3R4, Rx, Lx*1e3), 'build/c1.txt')
maketable((R16, L16*1e3), 'build/c2.txt')

#Maxwellbrücke
R3 = unp.uarray(d[2], d[2] * uncertainty_r2)
R4 = unp.uarray(d[3], d[3] * uncertainty_r2)
C4 = unp.uarray(d[0], d[0] * uncertainty_2)
R2 = unp.uarray(d[1], uncertainty_r2 * d[1])

Rx = R2 * R3 / R4
Lx = R2 * R3 * C4

R16 = mittel(Rx)
L16 = mittel(Lx)

maketable((C4*1e9, R2, R3, R4, Rx, Lx*1e3), 'build/d1.txt')
maketable((R16, L16*1e3), 'build/d2.txt')
