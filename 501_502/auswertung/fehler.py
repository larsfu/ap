from uncertainties import ufloat
import numpy as np
a=ufloat(13.308,0.366)
b=ufloat(12.323, 0.274)
c=ufloat(11.326, 0.302)
d=ufloat(10.745, 0.226)
e=ufloat(10.339, 0.220)
f=ufloat(0.080, 0.002)
g=ufloat(0.076, 0.001)
#print((a+b+c+d+e+f)/7)
p=ufloat(0.0001,0.000004)

#print(0.01905/p)
print(8*a**6*250)
print(8*b**6*300)
print(8*c**6*350)
print(8*d**6*400)
print(8*e**6*450)

e1=ufloat(1.11,0.18)*10**(10)
e2=ufloat(8.4,1.1)*10**9
e3=ufloat(5.9, 0,9)*10**9
e4=ufloat(4.9,0.6)*10**9
e5=ufloat(4.4, 0.6)*10**9

e=ufloat(6.9,0.5)*10**9

print((e1+e2+e3+e4+e5)/5)
print((1.75*10**11)/e)
