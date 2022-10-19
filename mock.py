import pylab as plt
import numpy as np
from labellines import labelLines

def getpBub(T):
    return pbar-(pbar-pc)*(T-Tbar)**2/(Tc-Tbar)**2 

def getTDew(p):
    return Ttherm - (Ttherm-Tc)*(p-ptherm)**2/(pc-ptherm)**2 

def get_pqlf(a, b, T):
    return a*T+b

def get_fleft(ql):
    qlf = 0.3
    return (ql - qlf)**2/(1 - qlf)**2

def get_fright(ql):
    qlf = 0.3
    return ql**2/qlf**2


Tc, pc = 1.0,1.0
Tbar, pbar = 0.6, 1.1
Ttherm, ptherm = 1.4, 0.6

Tbub = np.arange(0, Tc+0.05, 0.05)
pbub = [getpBub(T) for T in Tbub]
#print(Tbub)

pdew = np.arange(0, pc+0.05, 0.05)
Tdew = [getTDew(p) for p in pdew]

plt.plot(Tbub, pbub, label='bubble point')
plt.plot(Tdew, pdew, label='dew point')
plt.plot([0, Tc], [0, pc], 'k-')
plt.ylim(0, 1.4)
plt.xlabel('Temperature')
plt.ylabel('Pressure')

Tql = [0,Tc]
pql = [0, pc]
N = len(Tql)
Tavg, pavg = np.mean(Tql), np.mean(pql)

S_xx = 0.0
S_xy = 0.0
for T, p in zip(Tql, pql):
    S_xx += (T-Tavg)*(T-Tavg)
    S_xy += (T-Tavg)*(p-pavg)
S_xx /= N
S_xy /= N

a = S_xy/S_xx
b = pavg - a*pavg

# Contour #############################################
ql_dat = [0.9, 0.8, 0.7, 0.5]
for ql in ql_dat:
    p = [get_fleft(ql)*getpBub(T) + (1-get_fleft(ql))*get_pqlf(a,b,T) for T in Tbub]
    plt.plot(Tbub, p, 'k:', label=str(ql))
ql_dat = [0.3, 0.2, 0.15, 0.1, 0.05]
for ql in ql_dat:
    T = [(1-get_fright(ql))*getTDew(p) + get_fright(ql)*get_pqlf(1/a,-b,p) for p in pdew]
    plt.plot(T, pdew, 'k:', label=str(ql))
labelLines(plt.gca().get_lines(), fontsize=9)
plt.xlabel('Temperature')
plt.ylabel('Pressure')
###################################################
#Q1
# Tres, pres = 0.3, 1.05
# plt.plot(Tres, pres, 'k^')
# plt.text(Tres, pres, r'$T_{res}$, $P_{res}$')

# Tstock, pstock = 0.02, 0.1
# plt.plot(Tstock, pstock, 'k^')
# plt.text(Tstock, pstock, r'$T_{stock}$, $P_{stock}$')

#######################################################
# Q11
Tres, pres = 0.4*Tc, 1.08*pc
plt.plot(Tres, pres, 'k^')
plt.text(Tres, pres, r'$T_{res}$, $P_{res}$')

Tstock = [0.2*Tc, 0.2*Tc, 0.2] 
pstock = [0.7877*pc, 0.6081*pc, 0.4612*pc]
for i, T in enumerate(Tstock):
    label = f'Stock {i+1}'
    plt.plot(T, pstock[i], 'k^')
    plt.text(T, pstock[i], label)
    
# from graph, each oil canbe assigned a ql
ql = [0.9, 0.8, 0.7]
R = [(1-q)/q for q in ql]
z = 0.01
B = [1+z*(1/q-1) for q in ql]



