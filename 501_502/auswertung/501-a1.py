import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

x=np.linspace(-21,9)
x,y=np.genfromtxt('a1.txt',unpack=True) #U_B=200V
x1,y1=np.genfromtxt('a2.txt', unpack=True) #U_B=250V
x2,y2=np.genfromtxt('a3.txt', unpack=True) #U_B=300V
x3,y3=np.genfromtxt('a4.txt',unpack=True) #U_B=350V


def f(x,a,b):
    return a*x+b
params,covariance = curve_fit(f,x,y)
errors = np.sqrt(np.diag(covariance))
print ('a=',params[0], '±', errors[0])
print ('b=',params[1],'±', errors [1])

plt.plot(x,y,'bx',label="Messwerte für $U_\mathrm{B}=200V$")
plt.plot(x,f(x, *params), 'b-')

def f(x1,c,d):
    return c*x1+d
params,covariance = curve_fit(f,x1,y1)
errors = np.sqrt(np.diag(covariance))
print ('c=',params[0], '±', errors[0])
print ('d=',params[1],'±', errors [1])

plt.plot(x1,y1, 'rx',label="Messwerte für $U_\mathrm{B}=250V$")
plt.plot(x1,f(x1, *params), 'r-')

def f(x2,e,f):
    return e*x2+f
params,covariance = curve_fit(f,x2,y2)
errors = np.sqrt(np.diag(covariance))
print ('e=',params[0], '±', errors[0])
print ('f=',params[1],'±', errors [1])

plt.plot(x2,y2, 'gx',label="Messwerte für $U_\mathrm{B}=300V$")
plt.plot(x1,f(x1, *params), 'g-')

def f(x3,g,h):
    return g*x3+h
params,covariance = curve_fit(f,x3,y3)
errors = np.sqrt(np.diag(covariance))
print ('g=',params[0], '±', errors[0])
print ('h=',params[1],'±', errors [1])

plt.plot(x3,y3, 'kx',label="Messwerte für $U_\mathrm{B}=350V$")
plt.plot(x3,f(x3, *params), 'k-')


plt.xlabel(r'$U_\mathrm{d}/V$')
plt.ylabel('$D/cm$')
plt.legend(loc='best')
plt.savefig('501-a1.pdf')
