# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 14:37:54 2022

@author: alyss
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import pandas as pd
import math
import seaborn as sns

saveLocation =  r"Data/"

plt.close()

textSize = 20;
legendSize = 15;
markerSize = 10;
edgeSize = 1.75;
lineWidth = 2;
see = 0.6;

#To Use: Select and uncomment the set that you wish to display below:

#DMSO related
# setName = ["SetTwo", "SetNine", "SetEleven"]
# legendLabel = ["DMSO","Remdesivir", "Homoharringtonine"]

#Ethanol related
# setName = ["SetThree", "SetEight"]
# legendLabel = ["Ethanol", "Cycloheximide"]

#Water related
# setName = ["SetTen", "SetSeven"]
# legendLabel = ["Water", "Doxorubicin"]

#controls
# setName = ["SetTwo", "SetThree", "SetTen"]
# legendLabel = ["DMSO", "Ethanol", "Water"]

#drug-treated
setName = ["SetSeven", "SetEight", "SetNine", "SetEleven"]
legendLabel = ["Doxorubicin", "Cycloheximide", "Remdesivir", "Homoharringtonine"]

colors = ["black","blue", "orange","red","green"]


plt.figure(figsize=(8,6))

plotLines = []
for i in range(0,len(setName)):
    MTraw = pd.read_csv(saveLocation+"avgMsdMT"+setName[i]+".csv", header = None)
    PIVraw = pd.read_csv(saveLocation+"avgMsdPI"+setName[i]+".csv", header = None)

    MT = MTraw.dropna(axis=0, how='any')
    PIV = PIVraw.dropna(axis=0, how='any')

    MTtime = MT.iloc[:,0]
    PIVtime = PIV.iloc[:,0]

    MTmsd = MT.iloc[:,1]
    PIVmsd = PIV.iloc[:,1]

    MTs = MT.iloc[:,2]
    PIVs = PIV.iloc[:,2]

    MTn = MT.iloc[:,3]
    PIVn = PIV.iloc[:,3]


    plt.errorbar(MTtime, MTmsd, yerr = MTs/np.sqrt(MTn), color = colors[i], capsize = 5)
    plt.errorbar(PIVtime, PIVmsd, yerr = PIVs/np.sqrt(PIVn), color = colors[i], capsize = 5)
    MTline = plt.loglog(MTtime, MTmsd, '-', color = colors[i], markersize = markerSize, label = legendLabel[i], linewidth = lineWidth)
    PIVline = plt.loglog(PIVtime, PIVmsd, '-', color = colors[i], fillstyle = 'none', markersize = markerSize, linewidth = lineWidth)
    MTdot, = plt.loglog(MTtime, MTmsd, 'o', color = colors[i], markersize = markerSize)
    PIVdot, = plt.loglog(PIVtime, PIVmsd, 'o', markerfacecolor = 'white', markeredgewidth = edgeSize, markeredgecolor = colors[i], markersize = markerSize-edgeSize)

    plotLines.append([MTdot, PIVdot])

plt.legend()
plt.xlabel("Time Lag (min)", fontsize = textSize)
plt.ylabel("Average MSD ($\mu \mathrm{m}^2$)", fontsize = textSize)

plt.xlim(0,10.5)
plt.ylim(0,12)

#save both uncropped and appropriately cropped and say have errors
legend1 = plt.legend(plotLines[0], ["PTV", "PIV"], loc = "lower right", fontsize = legendSize)
plt.legend(loc = 2, fontsize = legendSize)
plt.gca().add_artist(legend1)
plt.tight_layout()
plt.savefig('outputimage.eps', format='eps')
