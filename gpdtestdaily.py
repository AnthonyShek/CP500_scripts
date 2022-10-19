import geopandas as gpd
from matplotlib.animation import FuncAnimation
import pandas as pd
import pylab as plt


dfUK = gpd.read_file('counties.json')
#ctypes = list(dfUK.ENGTYPE_2)
#countries = dfUK.NAME_1.unique().tolist()
isScot = dfUK['NAME_1']=='Scotland'
shape = dfUK[isScot]
shape = shape[['NAME_2', 'geometry']]
#shape = shape.drop(columns=['id', 'ISO', 'NAME_0', 'ID_1', 'NAME_1', 'ID_2', 'TYPE_2', 'ENGTYPE_2', 'VARNAME_2'])
shape = shape[~shape['NAME_2'].isin(['Orkney Islands', 'Shetland Islands', 'Eilean Siar'])]
counties = list(shape.NAME_2)


dat = pd.read_csv('datadaily.csv')
dat.rename(columns={'Unnamed: 0' : 'County'}, inplace=True)

shape = pd.merge(
        left = shape,
        right = dat,
        left_on = 'NAME_2',
        right_on = 'County', #column head of dat dataframe
        how = 'left'
    )

#shape = shape.dropna() # to exclude counties with no data


#fig = shape.boundary.plot(color='white', edgecolor='white', linewidth=1, figsize=(10,5))

# fig = shape.plot(ax=ax, column='Nov', cmap='RdBu_r', legend=True, 
#                  legend_kwds={'shrink': 0.8, 'orientation' : 'vertical'})
# ax.set_title('Average Daily Solar Radiation kJ/m2 in November 2021', size=14, weight='bold')
first = True
# Figure out how to plot boundary lines of counties without data

def animate(date):
    ax.clear()
    global first
    if first:
        # print('is Jan')
        #print(first)# for some reason this function is called three times with the argument 'Jan', using this crap condition to make sure only one colorbar is displayed
        fig = shape.plot(
            ax=ax, column=date, edgecolor='black', linewidth=0.5, 
            cmap='RdYlBu_r',figsize=(10,5), norm=plt.Normalize(vmin=0, vmax=30000),
            legend=True, legend_kwds={'shrink': 0.8, 'orientation' : 'vertical'}
            )
        first = False
    else:
        fig = shape.plot(ax=ax, column=date, edgecolor='black', linewidth=0.5, 
                          cmap='RdYlBu_r',figsize=(10,5), norm=plt.Normalize(vmin=0, vmax=30000))
    #sm = plt.cm.ScalarMappable(cmap='RdBu_r', norm=plt.Normalize(vmin=0, vmax=1000))
    #fig.colorbar(sm)
    ax.axis('off')
    ax.set_title(f'Average Daily Solar Radiation, {date}', size=14, weight='bold')

fig, ax = plt.subplots()
dates = shape.columns.T
dates = dates[3::]
anim = FuncAnimation(fig, animate, frames=dates, interval=100)
anim.save('testanim.gif')