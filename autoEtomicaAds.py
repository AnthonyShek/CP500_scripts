import os
import pyautogui as pya
import psutil
import time
import pyperclip
import numpy as np
import pylab as plt
import pandas as pd
import openpyxl

def tab(n, delay=0.01):
    pya.press('tab', presses=n, interval=delay)
    return 0

def reset(n):               
    tabs_reset2reset = 12
    tab(tabs_reset2reset-n)

def setT(T):
    tabsfromreset = 1
    tab(tabsfromreset) # temperature input box
    pya.write(str(T)) 
    reset(tabsfromreset)
    
def setP(P, B=False):
    tabsfromreset = 4
    if B == True:
        tab(2)
        pya.press('right')
        tab(1)
        pya.press('enter')
        tab(2) # B pressure input box
    elif B == False:
        tab(tabsfromreset) # pressure input box
    
    with pya.hold('ctrl'):
        pya.press('a')
    pya.write(str(P)) 
    
    if B == True:
        reset(tabsfromreset)
        tab(2)
        pya.press('left')
        tab(2)
        reset(tabsfromreset)
    elif B == False:
        reset(tabsfromreset)

    
def setEps(e, B=False):
    tabsfromreset = 6
    if B == True:
        tab(2)
        pya.press('right')
        tab(5)
    elif B == False:
        tab(tabsfromreset)
    
    defaultEps = 5.0
    pressN = int((e-defaultEps)*10) 
    if pressN >= 0:
        pya.press('right', presses=pressN)
    elif pressN < 0:
        pya.press('left', presses=abs(pressN))
        
    if B == True:
        reset(tabsfromreset)
        tab(2)
        pya.press('left')
        tab(4)
        reset(tabsfromreset)
    elif B == False:
        reset(tabsfromreset)

    
def startsim():
    tab(9) # start button
    pya.press('enter')
    tab(11) # enter info tabs
    pya.press('right', presses=1)

def collectdat(bulk = False, B=False):
    pya.click(button='right')
    pya.press('down', presses=5)
    pya.press('right')
    
    if B==True:
        pya.press('down')
    
    if bulk == True:
        pya.press('down', presses=2)
    
    if B==True and bulk == True:
        pya.press('down')
    
    pya.press('enter')
    with pya.hold('ctrl'):
        pya.press('a')
    with pya.hold('ctrl'):
        pya.press('c')
    with pya.hold('alt'):
        pya.press('f4')
    pastedat = pyperclip.paste()
    with open('tmpdat.txt', 'w') as f:
        f.write(pastedat)
        
    with open('tmpdat.txt') as f:
        lines = f.readlines()
    ydat, xdat = [],[]
    for line in lines:
        if len(line) > 18: #avoid first row
            xdat.append(float(line.split("\t")[0][0 : -1]))
            ydat.append(float(line.split("\t")[1][0 : -1]))
    
    return ydat, xdat

def getmeanAds():
    tab(11)
    pya.press('enter') #pause
    tab(14)
    meanAd = copypaste() 
    tab(8)
    pya.press('enter') #continue
    tab(11)
    return meanAd #excess adsorbed A

    
def collectAdsorption(BPresent=False):
    # graphlocat = pya.center(pya.locateOnScreen('graph2.bmp', confidence=0.8))
    graphlocat = pya.center(pya.locateOnScreen('graphlaptop.bmp', confidence=0.8))
    pya.moveTo(graphlocat.x, graphlocat.y)
    return collectdat(B=BPresent)
    
    
def copypaste():    
    with pya.hold('ctrl'):
        pya.press('a')
    with pya.hold('ctrl'):
        pya.press('c')
    return float(pyperclip.paste())
    
def collectmetrics(BPresent = False):
    metrics = []
    tab(8)
    pya.press('right')
    tab(3)
    metrics.append(copypaste()) #excess adsorbed A
    tab(1)
    metrics.append(copypaste()) # error
    
    if BPresent == False:
        tab(5)
        metrics.append(copypaste()) # potential energy
        tab(1)
        metrics.append(copypaste())
    elif BPresent == True: 
        
        tab(2)
        metrics.append(copypaste()) # excess adsorbed B
        tab(1)
        metrics.append(copypaste())
        
        tab(2)
        metrics.append(copypaste()) # potential energy
        tab(1)
        metrics.append(copypaste())
    
    tab(12)
    pya.press('left')
    tab(1)
    return metrics

        
def waitEquil(B = False):

    notequil = True
    equilToler = 0.01 # maximum deviation per cycle at 1%
    meanAds = [0]
    yprofA, xprofA= [], []
    yprofAB, xprofAB= [], []
    while notequil:
        time.sleep(5.0) # period between data collection

        meanAds.append(getmeanAds())
        if abs(meanAds[-1]-meanAds[-2])/meanAds[-1] < equilToler: 
            notequil = False
        # issue with this is that only the data point immediately prior decided if the system 
        # is in equilibirum. Therefore slow enough positive/negative trends (<1%) will go 
        # unnoticed. Consider introducing a method to assign a new weight to each in meanAds, 
        # the weight of a datapoint will decrease with increasing distance away from current. 
        # i.e. older datapoints have less weight. Determine if equil using weights
    
    pya.press('left')
    tab(1)   
    pya.press('enter') #pause
    
    print('Equil reached')
    del meanAds[0]
    plt.plot(range(len(meanAds)), meanAds)
    
    tab(11)
    pya.press('right', presses=2, interval = 0.05)
    qdat, tdat = collectAdsorption()
    if B == True:
        qdatB, tdatB = collectAdsorption(BPresent=B)
    
    # collect profile dat
    pya.press('right')
    yprofA, xprofA = collectdat()
    yprofAB, xprofAB = collectdat(bulk = True)
    
    if B == True:
        yprofB, xprofB = collectdat(B=B)
        yprofBB, xprofBB = collectdat(bulk = True, B=B)
    
    pya.press('left', presses=3)
    #reset(8)
    tab(4)
    metrics = collectmetrics(BPresent = B)
    tab(2)
    pya.press('enter') #reset avg
    reset(11)
    
    dc = {'q':qdat, 't':tdat, 'meanAds':meanAds, 'yprofA':yprofA, 'xprofA':xprofA, 'yprofAB':yprofAB, 'xprofAB':xprofAB, 'metrics':metrics}
    if B == True:
        dc['qB'] = qdatB
        dc['tB'] = tdatB
        dc['yprofB'] = yprofB
        dc['xprofB'] = xprofB
        dc['yprofBB'] = yprofBB
        dc['xprofBB'] = xprofBB
    return dc

def stopsim():
    tabsfromreset = 9
    tab(tabsfromreset)
    reset(tabsfromreset)
################################################################################
# A definitive and consistent solution to equilibrium determination for the adsorption module of Etomica

#create blank workbook
path = 'T1.0B.xlsx'

# df = pd.DataFrame([])
# with pd.ExcelWriter(path, engine='openpyxl', mode='a') as writer:  
#     df.to_excel(writer, sheet_name='Main')

T, eps = 1.0, 6.0
Pdat = np.arange(-4.5, -1.9, 0.25)
# Pdat = [-2.0]

BPresent= False
if BPresent == True:
    PB, epsB = -2, 6.0

for P in Pdat:          
    # os.popen('C:\\Users\evilp\Desktop\etomica\etomica-modules.exe') # link for desktop
    os.popen('C:\\Users\evilp\OneDrive\Desktop\Etomica\etomica-modules.exe') # link for laptop
    running = False
    while not running:
        running = "etomica-modules.exe" in (i.name() for i in psutil.process_iter())
        
    time.sleep(1)   
    tab(3)
    pya.press('enter')
    time.sleep(1) # adsorption opened, highlighting temperature slider
    
    setT(T)               
    setP(P)
    setEps(eps)
    
    if BPresent == True:
        setP(PB, B=BPresent)
        setEps(epsB, B=BPresent)    
    
    dat = {
            'pre': {},
            'post': {}
            }
           
    startsim()
    dat['pre'] = waitEquil(B = BPresent) 
    startsim()
    dat['post']= waitEquil(B = BPresent)
    stopsim()
                
    
    # spreadsheet export function
    
    index_name, dat_list = [], []
    
    with pd.ExcelWriter(path, engine='openpyxl', mode='a') as writer:
        index_name.append('Pre Equil')
        dat_list.append([])
        for key, datlist in dat['pre'].items():
            index_name.append(key)
            dat_list.append(datlist)
            
        index_name.append('Post Equil')
        dat_list.append([])
        for key, datlist in dat['post'].items():
            index_name.append(key)
            dat_list.append(datlist)
        
        df = pd.DataFrame(dat_list, index=index_name)
        dfT = df.T
        name = 'T' + str(T) + '-P' + str(abs(P)) + '-e' + str(eps)
        dfT.to_excel(writer, index=False, sheet_name=name)
    
    with pya.hold('alt'):
        pya.press('f4')