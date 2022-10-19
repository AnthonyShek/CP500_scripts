import pandas as pd
import numpy as np
import pylab as plt

def residue(df, A):
    dE = [0]
    usage = 1.8*1e7/365 # kJ
    for i, rad in enumerate(df['rads'].values):
        dE.append(dE[i-1] + rad*A - usage)
    del dE[0]
    batcap =-min(dE) 
    dE_cor = [batcap]
    for i, rad in enumerate(df['rads'].values):
        dE_cor.append(dE_cor[i-1] + rad*A - usage)
    del dE_cor[0]
    # print([batcap, dE_cor[-1]])
    res = abs((dE_cor[-1] - batcap) / dE_cor[-1])
    #print(res)
    return res

def getA(df):
    res = 1
    A = 35 # inital guess for area
    dA = A/2
    I = 5 # iterations for stochastic estimate
    for i in range(I):
        for j in range(100):
            A_tmp = A + dA*(2 * np.random.rand() - 1)
            res_tmp = residue(df, A_tmp)
            #print([A_tmp, res_tmp])
            if res_tmp < res:
                res = res_tmp
                A = A_tmp
        dA = dA/10
    # while res > 0.01 or iteration < 100:
    #     A_tmp = A + dA*(2 * np.random.rand() - 1)
    #     res_tmp = residue(df, A_tmp)
    #     #print([A_tmp, res_tmp])
    #     if res_tmp < res:
    #         res = res_tmp
    #         A = A_tmp
    #     iteration += 1
    
    print(f'area: {A}. residue percentage: {res}')
    return A


df = pd.read_csv('datadaily.csv')
df.rename(columns={'Unnamed: 0' : 'County'}, inplace=True)
counties = df.County.values
dat= {}
for county in counties:    
    df_tmp = df[df['County']==county].T[1::]
    df_tmp = df_tmp.reset_index()
    df_tmp.columns = ['date', 'rads']
    #df_tmp['date'] = pd.to_datetime(df_tmp['date'], format='%d/%m/%Y')
    print(county)
    dat[county] = getA(df_tmp)
    
plt.bar(dat.keys(), dat.values())
plt.xticks(rotation=45, size=6)
# why plot over each other? also how to sort into descending order?
plt.ylim(min(dat.values())-1, max(dat.values())+1)
plt.ylabel(r'Required Solar Panel Area ($m^2$)')