from uncertainties import ufloat
import numpy as np
a=ufloat(9.218,0.197)*10**3
b=ufloat(8.945, 0.382)*10**3
c=ufloat(7.849, 0.162)*10**3
d=ufloat(7.389, 0.121)*10**3
e=ufloat(7.110, 0.115)*10**3
f=ufloat(0.080, 0.002)
g=ufloat(0.076, 0.001)
#print((a+b+c+d+e+f)/7)
p=ufloat(0.0001,0.000004)

#print(0.01905/p)
print(8*a**2*250)
print(8*b**2*300)
print(8*c**2*350)
print(8*d**2*400)
print(8*e**2*450)

e1=ufloat(1.7,0.07)*10**(11)
e2=ufloat(1.92,0.16)*10**11
e3=ufloat(1.72, 0.07)*10**11
e4=ufloat(1.75,0.06)*10**11
e5=ufloat(1.82, 0.06)*10**11

e=ufloat(1.78,0.04)*10**11

print((e1+e2+e3+e4+e5)/5)
print((1.75*10**11)/e)

A=0.438
A1=ufloat(0.34147,0.00972)

#print(A/A1)
