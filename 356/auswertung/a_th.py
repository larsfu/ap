import numpy as np

L =  1.5e-3
C1 = 22e-9
C2 = 9.39e-9

f1 = np.sqrt(2)/np.sqrt(L*C1)/(2*np.pi)
print(f1, 49.85e3/f1-1)

f2 = np.sqrt(2/L * (C1+C2)/(C1*C2))/(2*np.pi)
f3 = np.sqrt(2/(L*C2))/(2*np.pi)
f4 = np.sqrt(2/(L*C1))/(2*np.pi)


print(f2, f3, f4)
print(1-64.84e3/f2, 1-55.04e3/f3, 1-35.42e3/f4)
