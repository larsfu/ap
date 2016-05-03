import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

x=np.linspace(-40,20)
x,y=np.genfromtxt('a5.txt',unpack=True) #U_B=400V
x1,y1=np.genfromtxt('a6.txt', unpack=True) #U_B=450V
x2,y2=np.genfromtxt('a7.txt', unpack=True) #U_B=500V


def f(x,a,b):
    return a*x+b
params,covariance = curve_fit(f,x,y)
errors = np.sqrt(np.diag(covariance))
print ('a=',params[0], '±', errors[0])
print ('b=',params[1],'±', errors [1])

plt.plot(x,y,'yx',label="Messwerte für $U_\mathrm{B}=400$")
plt.plot(x,f(x, *params), 'y-')

def f(x1,c,d):
    return c*x1+d
params,covariance = curve_fit(f,x1,y1)
errors = np.sqrt(np.diag(covariance))
print ('c=',params[0], '±', errors[0])
print ('d=',params[1],'±', errors [1])

plt.plot(x1,y1, 'mx',label="Messwerte für $U_\mathrm{B}=450V$")
plt.plot(x1,f(x1, *params), 'm-')

def f(x2,e,f):
    return e*x2+f
params,covariance = curve_fit(f,x2,y2)
errors = np.sqrt(np.diag(covariance))
print ('e=',params[0], '±', errors[0])
print ('f=',params[1],'±', errors [1])

plt.plot(x2,y2, 'cx',label="Messwerte für $U_\mathrm{B}=500V$")
plt.plot(x1,f(x1, *params), 'c-')



plt.xlabel(r'$U_\mathrm{d}/V$')
plt.ylabel('$D/cm$')
plt.legend(loc='best')
plt.savefig('501-a2.pdf')
