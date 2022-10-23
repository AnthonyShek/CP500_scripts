import pandas as pd
import numpy as np
import pylab as plt

def residue(df, A):
    dE = [0]
    usage = 1.8*1e7/365 # kJ
    for i, rad in enumerate(df['rads'].values):
        dE.append(dE[i-1] + rad*A - usage)
    del dE[0]
    offset =abs(min(dE)) 
    batcap = offset+max(dE)
    dE_cor = [offset]
    for i, rad in enumerate(df['rads'].values):
        dE_cor.append(dE_cor[i-1] + rad*A - usage)
    del dE_cor[0]
    # print([batcap, dE_cor[-1]])
    res = abs((dE_cor[-1] - offset) / dE_cor[-1])
    #print(res)
    return res, batcap

def getA(df):
    res = 1
    A = 35 # inital guess for area
    dA = A/2
    I = 5 # iterations for stochastic estimate
    for i in range(I):
        for j in range(100):
            A_tmp = A + dA*(2 * np.random.rand() - 1)
            res_tmp, batcap = residue(df, A_tmp)
            #print([A_tmp, res_tmp])
            if res_tmp < res:
                res = res_tmp
                A = A_tmp
        dA = dA/10
    print(f'area: {A}. residue percentage: {res}')
    return A, batcap


df = pd.read_csv('datadaily.csv')
df.rename(columns={'Unnamed: 0' : 'County'}, inplace=True)
counties = df.County.values
dat= {}
datBat ={}
for county in counties:    
    df_tmp = df[df['County']==county].T[1::]
    df_tmp = df_tmp.reset_index()
    df_tmp.columns = ['date', 'rads']
    print(county)
    dat[county], datBat[county] = getA(df_tmp)

import matplotlib as mp
data_normalizer = mp.colors.Normalize()
color_map = mp.colors.LinearSegmentedColormap(
    "my_map",
    {
        "red": [(0, 1.0, 1.0),
                (1.0, .5, .5)],
        "green": [(0, 0.5, 0.5),
                  (1.0, 0, 0)],
        "blue": [(0, 0.50, 0.5),
                 (1.0, 0, 0)]
    }
)
dat = dict(sorted(dat.items(), key=lambda item: item[1])) #sort to ascending order
plt.bar(dat.keys(), dat.values(), color=color_map(data_normalizer(np.array(list(dat.values())))))
plt.xticks(rotation=45, size=6, ha='right')
plt.ylim(min(dat.values())-1, max(dat.values())+1)
plt.ylabel(r'Required Solar Panel Area ($m^2$)')
plt.savefig('area.png', dpi=300, bbox_inches='tight')

# color_map = mp.colors.LinearSegmentedColormap(
#     "my_map",
#     {
#         "blue": [(0, 1.0, 1.0),
#                 (1.0, .5, .5)],
#         "green": [(0, 0.5, 0.5),
#                   (1.0, 0, 0)],
#         "red": [(0, 0.50, 0.5),
#                  (1.0, 0, 0)]
#     }
# )

# datBat = dict(sorted(datBat.items(), key=lambda item: item[1])) #sort to ascending order
# plt.bar(datBat.keys(), datBat.values(), color=color_map(data_normalizer(np.array(list(datBat.values())))))
# plt.xticks(rotation=45, size=6, ha='right')
# plt.ylim(min(datBat.values())-1e5, max(datBat.values())+1e5)
# plt.ylabel(r'Required Battery Capacity (kJ)')
# plt.savefig('batcap.png', dpi=300, bbox_inches='tight')