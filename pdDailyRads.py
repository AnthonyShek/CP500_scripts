import pandas as pd

def getrads(URL):
    df = pd.read_csv(URL, skiprows=range(75))
    df = df.drop(df.index[df.shape[0]-1]) # delete last row
    #df = df[df.ob_hour_count == 1] # exclude rows for 24hr data, which begins in oct
    df = df[['ob_end_time', 'glbl_irad_amt']]
    df.columns = ['time', 'rads'] # rename headers
    
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M')
    df['time_date'] = df['time'].dt.strftime('%d/%m/%Y')
    dates = pd.date_range(start=str(df.time.dt.date[0]), 
                          end=str(df.time.dt.date[df.shape[0]-1])).strftime('%d/%m/%Y')
    # months = pd.date_range(start=str(df.time.dt.date[0]), 
    #                        end=str(df.time.dt.date[df.shape[0]-1]), 
    #                        freq='MS').strftime('%m/%Y')
    # date_range kwarg: freq='MS' for month start, freq='M' month end
    meanRads=[]
    for date in dates:
        meanRads.append(df.loc[df['time_date']==date, 'rads'].sum()*0.15)
        
    global dates_str
    global first
    if first:
        dates_str = dates.T
        first = False
    return meanRads

dates_str = 0
first = True

dat = { 
        #'Argyll and Bute' : getrads('dunstaffnage2021.csv'),
        'Aberdeenshire' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_aberdeenshire_55827_braemar-no-2_qcv-1_2021.csv'),
        'Aberdeen' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_aberdeenshire_00161_dyce_qcv-1_2021.csv'),
        'Argyll and Bute' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_argyll-in-strathclyde-region_00918_dunstaffnage_qcv-1_2021.csv'),
        'Angus' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_kincardineshire_00177_inverbervie-no-2_qcv-1_2021.csv'),
        'East Ayrshire' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_ayrshire_01005_auchincruive_qcv-1_2021.csv'),
        'South Ayrshire' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_ayrshire_01007_prestwick-gannet_qcv-1_2021.csv'),
        'North Ayshire' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_ayrshire_01007_prestwick-gannet_qcv-1_2021.csv'),
        'Scottish Borders' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_berwickshire_00268_charterhall_qcv-1_2021.csv'),
        'Dumfries and Galloway' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_dumfriesshire_01023_eskdalemuir_qcv-1_2021.csv'),
        'Fife' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_fife_00235_leuchars_qcv-1_2021.csv'),
        'Highland' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_inverness-shire_00105_tulloch-bridge_qcv-1_2021.csv'),
        'Midlothian' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_midlothian-in-lothian-region_19260_edinburgh-gogarbank_qcv-1_2021.csv'),
        'West Lothian' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_midlothian-in-lothian-region_19260_edinburgh-gogarbank_qcv-1_2021.csv'),
        'East Lothian' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_midlothian-in-lothian-region_19260_edinburgh-gogarbank_qcv-1_2021.csv'),
        'Edinburgh' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_midlothian-in-lothian-region_19260_edinburgh-gogarbank_qcv-1_2021.csv'),
        'Moray' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_moray-in-grampian-region_00132_kinloss_qcv-1_2021.csv'),
        'Perthshire and Kinross' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_perthshire-in-tayside-region_00212_strathallan-airfield_qcv-1_2021.csv'),
        'Renfrewshire' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_renfrewshire_24125_glasgow-bishopton_qcv-1_2021.csv'),
        'East Renfrewshire' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_renfrewshire_24125_glasgow-bishopton_qcv-1_2021.csv'),
        'Inverclyde' : getrads('rawdata\midas-open_uk-radiation-obs_dv-202207_renfrewshire_24125_glasgow-bishopton_qcv-1_2021.csv')
        }
#north and south Ayrshire modelled with same data set
# same w/ mid, east, west lothian & edinburgh
# limited data for mid scotland

dfout = pd.DataFrame(dat).T
dfout.columns = dates_str
dfout.to_csv('datadaily.csv')


#daily=[]
#for date in dates:
#    df_tmp = df[df['time'].dt.date.between(date,date)]
#    daily.append(0.15*df_tmp['rads'].sum())
#plt.plot(dates, daily)
#plt.xlabel('day')
#plt.ylabel('Available Energy KJ/m2')

#gridDmd = pd.read_csv('gridwatch.csv')
# gridDmd = gridDmd.drop(gridDmd['id']) 


#for date in df.ob_end_time.dt.date:
#   
#   for hr in :
#       print()
#df['ob_end_time'][0].month
#df.ob_end_time.dt.strptime

