import numpy as np
import uncertainties as unc
from maketable import maketable
from scipy.constants.constants import C2K

def T(U):
    return 25.157*U - 0.19*U**2

c_w = 4.18e3
M = np.array([12.0, 118.7, 118.7, 118.7])/1e3
rho = np.array([2.25,7.28,7.28,7.28])*1e3
alpha = np.array([8,27,27,27])/1e6
kappa = np.array([33,55,55,55])*1e9
R = unc.ufloat(8.3144598, 0.0000048)

U_k, U_w, U_m, m_k, m_Deckel, m_WG = np.genfromtxt('daten/daten.txt', unpack=True)

maketable((("Graphit", "Zinn", "", ""), U_k, U_w, U_m, m_k, m_Deckel, m_WG), 'build/daten.tex')

m_k /= 1e3
m_Deckel /= 1e3
m_WG /= 1e3

m_Glas = 187.63e-3
m_WG0 = 729.12e-3
U_vorher = 0.84
U_nachher = 2.25
U_wasser = 4.13
m_x = m_y = (m_WG0 - m_Glas)/2


gerät = (c_w*m_y*(T(U_wasser) - T(U_nachher)) - c_w*m_x*(T(U_nachher) - T(U_vorher)))/(T(U_nachher)-T(U_vorher))
print(gerät)

c_k = (c_w * (m_WG-m_Glas) + gerät)*(T(U_m)-T(U_w))/((m_k-m_Deckel)*(T(U_k) - T(U_m)))
print(c_k[0], c_k[1:].mean(), '+-' ,c_k[1:].std(), c_k[1:].std()/c_k[1:].mean()*100, '%')


C_p = c_k*M
print(C_p[0], C_p[1:].mean(), '+-' ,C_p[1:].std(), C_p[1:].std()/C_p[1:].mean()*100, '%')


C_v = -9*alpha**2 * kappa * (M/rho) * C2K(T(U_m)) + C_p
print(C_v[0], C_v[1:].mean(), '+-' ,C_v[1:].std(), C_v[1:].std()/C_v[1:].mean()*100, '%')

a = C_v/(3*R)
print(a[0], a[1:].mean())#, '+-' ,a[1:].std())#, a[1:].std()/a[1:].mean()*100, '%')
