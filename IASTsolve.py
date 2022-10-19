import numpy as np
from scipy.optimize import fsolve
import pylab as plt

def func(sp, p):
    # uggo eqn
    f = 0
    for i, pi in enumerate(p):
        f += pi * b[i]/(np.exp(sp/tau[i])-1)
    return 1- f

def getx(y):
    y.append(1-y[0])
    p = [yi*P for yi in y]
    sp_sol = fsolve(func, tau[0], args=p)
    print(f'spreading pressure: {sp_sol} J/m2') 
    x = []
    for i, pi in enumerate(p):
        x.append(pi*b[i]/(np.exp(sp_sol/tau[i])-1))
    return x[0]

def getDiff(func, var):
    return sp.diff(func, var)


#b = [545.313, 1427.5] # [B, A]
#nm = [1.146131805, 1.167542323] # [B, A]
langCst = {
    'stnd' : {'b' : [545.313, 1427.5], 'nm' : [1.146131805, 1.167542323]},
    'pos' : {'b' : [573.4666667, 1412.166667], 'nm' : [1.162520344, 1.180219521]},
    'neg' : {'b' : [553.25, 1459.833333], 'nm' : [1.129688206, 1.141682841]}
    }


P = 0.002
kb = 1.380649e-23
T= 1.0
A = 64 # A = 37 for silly looking graph
coef = 1 # ~1e10 gives best fit with experimental data
coef2 = 1 # the value of this, hence order of magnitude of nm does not at all influence the R2 value
ydat = np.arange(0,1.01,0.01)
xdat=[]
for dat in langCst.values():
    nm = dat['nm']
    b = [coef*b for b in dat['b']]
    tau = [kb*T*coef2*n/A for n in nm]
    xdat.append([getx([y]) for y in ydat])
plt.plot(xdat[0],ydat, label='IAST model')
plt.plot(xdat[1],ydat, ':', color='grey', label='Error bounds')
plt.plot(xdat[2],ydat, ':', color='grey')
plt.plot(ydat,ydat, '-k', linewidth=0.8) #diagonal 
plt.xlim(0,1.015)
plt.ylim(0,1.015)


################################################################################
import sympy as sp
expdat = {
    'nA' : [0.0009513, 0.3007, 0.4029, 0.5659, 0.6228, 0.6707, 0.7139, 0.7881, 0.811, 0.854],
    'nA_er' : [0.00034, 0.011, 0.012, 0.0072, 0.0044, 0.008, 0.012, 0.0065, 0.0091, 0.0095],
    'nB' : [0.7073, 0.4504, 0.3548, 0.2402, 0.1736, 0.1395, 0.09891, 0.04409, 0.01972, 0.0000259],
    'nB_er' : [0.015, 0.0068, 0.015, 0.011, 0.0069, 0.0049, 0.0069, 0.0062, 0.0037, 0.000014],
    'yB' : [0.999499064, 0.88818423, 0.776154575, 0.671240581, 0.557311634, 0.442688366, 0.328759419, 0.223845425, 0.11181577, 0.000500936]
    }

expdat['xB'] = [nB/(nA + nB) for nA, nB in zip(expdat['nA'], expdat['nB'])]

nA_sp, nB_sp = sp.symbols('nA nB')
variables = [nA_sp, nB_sp]
xb_sp = nB_sp/(nA_sp + nB_sp)

diffs = []
for var in variables:
    diffs.append(getDiff(xb_sp, var))

xB_er = []
for nA, nB, nA_er, nB_er in zip(expdat['nA'], expdat['nB'], expdat['nA_er'], expdat['nB_er']):
    errors = [nA_er, nB_er]
    err_prop=0
    for diff, error in zip(diffs, errors):
        err_prop += diff**2*error**2  
    err_prop = sp.lambdify([nA_sp, nB_sp], sp.sqrt(err_prop))
    xB_er.append(err_prop(nA, nB))
expdat['xB_er'] = xB_er
#perer = [er/xB*100 for er,xB in zip(xB_er, expdat['xB'])] # Percentage error


#xb = [0.998656833, 0.599653841, 0.468259205, 0.297977918, 0.217980914, 0.172179709, 0.121688956, 0.05298069, 0.023738444, 3.03269E-05]
#plt.plot(expdat['xB'], expdat['yB'], '*', label='Experimental')
plt.errorbar(expdat['xB'], expdat['yB'], xerr=expdat['xB_er'], label='Experimental', color='orange', fmt = 'o' , markersize=3, capsize = 3)
plt.xlabel(r'$x_B$')
plt.ylabel(r'$y_B$')

###      get R^2      ########################################################
tau = [kb*T*coef2*n/A for n in langCst['stnd']['nm']]
b = [coef*b for b in langCst['stnd']['b']]
xhat = [getx([y]) for y in expdat['yB']]
xbar = np.mean(expdat['xB'])

SSR = 0
SST = 0
for i, x in enumerate(expdat['xB']):
    SSR += (x-xhat[i])**2
    SST += (x-xbar)**2
R2 = 1- SSR/SST
R2_str = r'$R^2$: ' + str(np.around(R2, decimals=4)) 
plt.text(0.03, 0.69, R2_str)
plt.legend()

