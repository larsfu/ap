import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.constants.constants import C2K
from scipy.stats import linregress


#
##
###
####   TODO: Fehlerrechnung, ρ bestimmen
###
##
#

#Konstanten definieren
R = 8.3144598
κ = 1.139
ρ0 = 5.51 #T = 0°C, p = 1bar

#Messdaten laden
t, T1, T2, pa, pb, P = np.genfromtxt("daten.txt", unpack = True)

#Dampfdruckkurve laden
dampf_p, dampf_T = np.genfromtxt("dampfdruck.txt", unpack = True)

#Temperaturen in Kelvin konvertieren
T1 = C2K(T1)
T2 = C2K(T2)
dampf_T = C2K(dampf_T)

#Drücke in Pascal umrechnen
pa *= 100000
pb *= 100000
dampf_p *= 100000

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
test_points = np.array([120, 600, 990, 1590])

#Bestimmung des Differentialquotienten der Fit-Funktion zu den Testzeitpunkten
test_T1 = dTdt(test_points, *params1)
test_T2 = dTdt(test_points, *params2)

#Wärmeleistung ins warme Reservoir bestimmen
test_T1 *= (750 + 16719) #TODO: Wärmekapazität von Wasser korrigieren
test_T2 *= (750 + 16719)

#Quotient aus Wärmeleistung und gemittelter elektrischer Leistung (= Gütezahl)
ν = test_T1 / np.mean(P)

#Gütezahlen ausgeben
print(ν)

#Wirkungsgrade einer idealen Wärmepumpe bei den Temperaturniveaus der Testzeitpunkte bestimmen
ν_ideal = T(test_points, *params1)/(T(test_points, *params1) - T(test_points, *params2))
#Ideale Wirkungsgrade ausgeben
print(ν_ideal)

#Auswertung der Dampfdruckkurve
dampf_p = np.log(dampf_p)
dampf_T = 1 / dampf_T

#Lineare Regression des logarithmierten Drucks über der reziproken Temperatur
result = linregress(dampf_T, dampf_p) # (slope, intercept, r_value, p_value, std_err)
L = -result[0] * R

#Massendurchsatz berechnen
#TODO: Ist das Minus korrekt?
m = -test_T2 / L

#Massendurchsätze ausgeben
print(m)

#Berechnung der mechanischen Kompressorleistung
test_pa = pa[test_points//30]
test_pb = pb[test_points//30]

#TODO: ρ aus ρ0 mit idealem Gasgesetz bestimmen
ρ = ρ0 * 3
N = 1 / (κ - 1) * (test_pb * (test_pa / test_pb) ** (1 / κ) - test_pa) / ρ * m

print(N)

#Auswerte-Stellen für die Fits generieren
x = np.linspace(0, 1800, 1000)

#Temperaturen plotten
plt.plot(t, T1, 'rx', label='$T_1$')
plt.plot(t, T2, 'bx', label='$T_2$')

#Temperatur-Fits plotten
plt.plot(x, T(x, *params1), 'r-')
plt.plot(x, T(x, *params2), 'b-')

#Achsenbeschriftung
plt.xlabel(r'$t / \si{\second}$')
plt.ylabel(r'$T / \si{\kelvin}$')

#Legende, Layout, speichern
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/plot.pdf')

#Plot leeren
plt.clf()

#Dampfdruckkurve plotten (+ Lineare Regression)
x = np.linspace(0.0025, 0.004, 10)
plt.plot(dampf_T, dampf_p, 'rx', label='Dampfdruckkurve')
plt.plot(x, result[0] * x + result[1], 'b-', label='Lineare Regression')
plt.xlim(0.00265, 0.0039)

#Achsenbeschriftung
plt.xlabel(r'$T^{-1} / \si{\per\kelvin}$')
plt.ylabel(r'$\ln(p / \si{\Pa})$')

#Legende, Layout, speichern
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/plot_dampfdruck.pdf')
