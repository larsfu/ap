import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.constants.constants import C2K
from scipy.stats import linregress
import uncertainties as unc
import uncertainties.unumpy as unp
from maketable import maketable


#
##
###
####   TODO:
###
##
#

#Konstanten definieren (CODATA 2014)
R = unc.ufloat(8.3144598, 0.0000048)

#Variablen definieren
κ = 1.139
ρ0 = 5.51
T0 = 273.15
p0 = 100000
sigma_T = 0.1
p_offset = 1
v = unc.ufloat(4/1000, 0.0004)
c_w = unc.ufloat((4219 + 4180)/2, 40)
rho_wasser = unc.ufloat((999.84 + 988.5)/2, 10)
M = 120.913
print(c_w)

#Messdaten laden
t, T1, T2, pa, pb, P = np.genfromtxt("daten.txt", unpack = True)

#Dampfdruckkurve laden
dampf_p, dampf_T = np.genfromtxt("dampfdruck.txt", unpack = True)

#Temperaturen in Kelvin konvertieren
T1 = C2K(T1)
T2 = C2K(T2)
dampf_T = C2K(dampf_T)

#Druck-Offset anwenden
pa += p_offset
pb += p_offset
dampf_p += p_offset

#Fehler auf Drücke anwenden
pa = unp.uarray(pa, 0.2)
pb = unp.uarray(pb, 1.0)
dampf_p = unp.uarray(dampf_p, np.append(np.ones(15)*0.2, np.ones(15)*1))

#Drücke in Pascal umrechnen
pa *= 100000
pb *= 100000
dampf_p *= 100000

#Fit-Funktion für die Temperaturkurve (siehe 5b)
#def T(t, A, B, C, α):
#    return A * t ** α / (1 + B * t ** α) + C
def T(t, A, B, C):
    return A * t ** 2 + B * t  + C

#Ableitung der Fit-Funktion für die Differentialquotienten
#def dTdt(t, A, B, C, α):
#    return ((A * α * t ** (α - 1) * (1 + B * t ** α)) - (A * t ** α) * (B * α * t ** (α - 1))) / (1 + B * t ** α) ** 2
def dTdt(t, A, B, C):
    return 2 * A * t + B

#Curve Fits an die Messwerte mit ausprobierten Anfangswerten
params1, pcov1 = curve_fit(T, t, T1, maxfev = 1000000, p0 = (1, 1e-2, 295), sigma = sigma_T)
params2, pcov2 = curve_fit(T, t, T2, maxfev = 1000000, p0 = (-0.01, 1e-2, 295), sigma = sigma_T)

#Parameter mit Standardfehler aus Kovarianzmatrix berechnen
params1_u = unc.correlated_values(params1, pcov1)
params2_u = unc.correlated_values(params2, pcov2)

maketable(params1_u, "build/coefficients1.tex", True)
maketable(params2_u, "build/coefficients2.tex", True)

#4 Testzeitpunkte in der Messung
test_points = np.array([120, 600, 990, 1590])

#Bestimmung des Differentialquotienten der Fit-Funktion zu den Testzeitpunkten
test_T1 = dTdt(test_points, *params1_u)
test_T2 = dTdt(test_points, *params2_u)

#Wärmeleistung ins warme Reservoir bestimmen
print("c_w")
print(v*rho_wasser*c_w)
wärmekapazität = (unc.ufloat(750, 10) + c_w*v*rho_wasser)
test_T1 *= wärmekapazität
test_T2 *= wärmekapazität

#Quotient aus Wärmeleistung und gemittelter elektrischer Leistung (= Gütezahl)
ν = test_T1 / np.mean(P)

#Gütezahlen ausgeben
#print(ν)

#Wirkungsgrade einer idealen Wärmepumpe bei den Temperaturniveaus der Testzeitpunkte bestimmen
ν_ideal = T(test_points, *params1_u)/(T(test_points, *params1_u) - T(test_points, *params2_u))
#Ideale Wirkungsgrade ausgeben
#print(ν_ideal)

#Verhältnis bestimmen
verhältnis = ν / ν_ideal

#Auswertung der Dampfdruckkurve
dampf_p_log = unp.log(dampf_p)
dampf_T_reziprok = 1 / dampf_T

#Lineare Regression des logarithmierten Drucks über der reziproken Temperatur
result = linregress(dampf_T_reziprok, unp.nominal_values(dampf_p_log)) # (slope, intercept, r_value, p_value, std_err)
print(-unc.ufloat(result[0], result[4]))
L = -unc.ufloat(result[0], result[4]) * R
maketable([-unc.ufloat(result[0], result[4]),L], "build/table_verdampfungswärme.tex", False)

#Massendurchsatz berechnen
m = -test_T2 / L
m *= M
#Massendurchsätze ausgeben
print(m)

#Berechnung der mechanischen Kompressorleistung
test_pa = pa[test_points//30]
test_pb = pb[test_points//30]

ρ = ρ0 * T0 * test_pa / (T2[test_points//30] * p0)
N = 1 / (κ - 1) * (test_pb * (test_pa / test_pb) ** (1 / κ) - test_pa) / ρ * (m / 1000)

#Mechanische Kompressorleistung berechnen
#print(N)

#Tabelle der Ergebnisse generieren und speichern
maketable((test_points, test_T1, ν, ν_ideal, verhältnis), "build/table_guete.tex", False)
maketable((test_points, m), "build/table_massendurchsatz.tex", False)
maketable((test_points, ρ, N), "build/table_kompressorleistung.tex", False)
#Selbiges für die Messdaten
maketable((np.int_(t), T1, T2, np.int_(unp.nominal_values(pa)/1000), np.int_(unp.nominal_values(pb)/1000), np.int_(P)), "build/table_data.tex", False)
#Und die Dampfdruckkurve
maketable((dampf_T, np.int_(unp.nominal_values(dampf_p)/1000)), "build/table_dampfdruck.tex", False)

#Auswerte-Stellen für die Fits generieren
x = np.linspace(0, 1800, 1000)

#Temperaturen plotten
#plt.errorbar(t, T1, yerr=np.ones(len(t)) * sigma_T, fmt = 'r.', label='$T_1$')
#plt.errorbar(t, T2, yerr=np.ones(len(t)) * sigma_T, fmt = 'b.', label='$T_2$')
plt.plot(t, T1, 'rx', label='$T_1$')
plt.plot(t, T2, 'bx', label='$T_2$')

#Temperatur-Fits plotten
plt.plot(x, T(x, *params1), 'r-', label='Fit für $T_1$')
plt.plot(x, T(x, *params2), 'b-', label='Fit für $T_2$')

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
plt.errorbar(dampf_T_reziprok, unp.nominal_values(dampf_p_log), fmt='r.', yerr=unp.std_devs(dampf_p_log), label='Dampfdruckkurve')
plt.plot(x, result[0] * x + result[1], 'b-', label='Lineare Regression')
plt.xlim(0.00265, 0.0039)

#Achsenbeschriftung
plt.xlabel(r'$T^{-1} / \si{\per\kelvin}$')
plt.ylabel(r'$\ln(p / \si{\Pa})$')

#Legende, Layout, speichern
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/plot_dampfdruck.pdf')
