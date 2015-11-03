import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.constants.constants import C2K

#
##
###
####   TODO: Fehlerrechnung, Massedurchsatz und Kompressorleistung
###
##
#

#Daten laden
t, T1, T2, pa, pb, P = np.genfromtxt("daten.txt", unpack = True)

#Temperaturen in Kelvin konvertieren
T1 = C2K(T1)
T2 = C2K(T2)

#Fit-Funktion für die Temperaturkurve (siehe 5b)
def T(t, A, B, C, α):
    return A * t ** α / (1 + B * t ** α) + C

#Ableitung der Fit-Funktion für die Differentialquotienten
def dTdt(t, A, B, C, α):
    return ((A * α * t ** (α - 1) * (1 + B * t ** α)) - (A * t ** α) * (B * α * t ** (α - 1))) / (1 + B * t ** α) ** 2

#Curve Fits an die Messwerte mit ausprobierten Anfangswerten
params1, pcov1 = curve_fit(T, t, T1, maxfev = 1000000, p0 = (1, 1e-2, 295, 1.5))
params2, pcov2 = curve_fit(T, t, T2, maxfev = 1000000, p0 = (-0.01, 1e-2, 295, 1.5))

#4 Testzeitpunkte in der Messung
test_points = [100, 600, 1000, 1600]

#Bestimmung des Differentialquotienten der Fit-Funktion zu den Testzeitpunkten
test_T1 = dTdt(test_points, *params1)
test_T2 = dTdt(test_points, *params2)

#Wärmeleistung ins warme Reservoir bestimmen
dQ1 *= (750 + 16719) #TODO: Wärmekapazität von Wasser korrigieren

#Quotient aus Wärmeleistung und gemittelter elektrischer Leistung (= Gütezahl)
ν = dQ1 / np.mean(P)

#Gütezahlen ausgeben
print(ν)

#Wirkungsgrade einer idealen Wärmepumpe bei den Temperaturniveaus der Testzeitpunkte bestimmen
ν_ideal = T(test_points, *params1)/(T(test_points, *params1) - T(test_points, *params2))
#Ideale Wirkungsgrade ausgeben
print(ν_ideal)

#Auswerte-Stellen für die Fits generieren
x = np.linspace(0, 1800, 1000)

#Messwerte plotten
plt.plot(t, T1, 'rx', label='$T_1$', markersize = 4)
plt.plot(t, T2, 'bx', label='$T_2$', markersize = 4)

#Fits plotten
plt.plot(x, T(x, *params1), 'r-')
plt.plot(x, T(x, *params2), 'b-')

#Achsenbeschriftung
plt.xlabel(r'$t / \si{\second}$')
plt.ylabel(r'$T / \si{\kelvin}$')

#Legende
plt.legend(loc='best')

#Layout
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

#Plot speichern
plt.savefig('build/plot.pdf')
