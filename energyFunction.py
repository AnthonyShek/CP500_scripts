import pandas as pd
import pylab as plt
from labellines import labelLines

df = pd.read_csv('datadaily.csv')
df.rename(columns={'Unnamed: 0' : 'County'}, inplace=True)
df = df[df['County']=='Aberdeenshire'].T[1::]
df = df.reset_index()
df.columns = ['date', 'rads']
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

# Energy differential system ##################################################
dE = [0]
usage = 1.8*1e7/365 # kJ
A= 33 # arbitrary guess value for optimised area
for i, rad in enumerate(df['rads'].values):
    dE.append(dE[i-1] + rad*A - usage)
del dE[0]
offset =abs(min(dE)) 
batcap = offset+max(dE)
print(f'Battery size: {batcap/3600:.2f} kWh. I.e. {batcap/usage:.2f} days of electricity')
plt.plot(df['date'], dE, label='Initial')
plt.xticks(rotation=45)
date_bounds = [df.date.dt.date[0], df.date.dt.date[df.shape[0]-1]]
plt.plot(date_bounds, [0,0], 'k:', linewidth=1)
plt.xlim(date_bounds)
plt.xlabel('Date')
plt.ylabel('Stored Energy (kJ)')


# corrected energy function ###################################################
dE_cor = [offset]
for i, rad in enumerate(df['rads'].values):
    dE_cor.append(dE_cor[i-1] + rad*A - usage)
del dE_cor[0]
print(f'{(dE_cor[-1]-offset)/3600} kWh end year residue ')
plt.plot(df['date'], dE_cor, label='Corrected')
min_idx = dE_cor.index(min(dE_cor))
max_idx = dE_cor.index(max(dE_cor))
plt.errorbar(df.date[min_idx], dE[min_idx]/2, yerr=abs(dE[min_idx]/2), color='k', capsize = 10, elinewidth=2)
plt.errorbar(df.date[max_idx], dE_cor[max_idx]/2, yerr=abs(dE_cor[max_idx]/2), color='k', capsize = 10, elinewidth=2)
labelLines(plt.gca().get_lines(), align=False ,fontsize=11)
plt.savefig('dE.png', dpi=300, bbox_inches='tight')