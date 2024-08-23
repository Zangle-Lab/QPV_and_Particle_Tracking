# -*- coding: utf-8 -*-
"""
Created on March 22, 2022

@author: alyss
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import pandas as pd
import math
import scipy.stats as ss
import seaborn as sns
from statsmodels.formula.api import ols

saveLocation =  r"Data"


plt.close()

#full list in legend order
setName = ["SetTwo", "SetThree", "SetTen", "SetSeven", "SetEight", "SetNine", "SetEleven"]
legendLabel = ["DMSO", "Ethanol", "Water", "Doxorubicin", "Cycloheximide", "Remdesivir", "Homoharringtonine"]

colors = ["b", "orange"]

avgRatio = 0
textSize = 18;
legendSize = 12;

plottingPD = pd.DataFrame(columns = ["Names", "PTV", "PIV", "errorPTV", "errorPIV", "ratio", "errorRatio"])
plt.figure(figsize=(8,6))

for i in range(0, len(setName)):
    MTraw = pd.read_csv(saveLocation+"/avgMsdMT"+setName[i]+".csv", names = ["Time", "MSD", "s", "n"])
    PIVraw = pd.read_csv(saveLocation +"/avgMsdPI"+setName[i]+".csv", names = ["Time", "MSD", "s", "n"])

    MTraw = MTraw.iloc[0:11, :]
    PIVraw = PIVraw.iloc[0:11, :]

    MT = MTraw.dropna(axis=0, how='any')
    PIV = PIVraw.dropna(axis=0, how='any')

    MT["D"] = MT.MSD/4
    PIV["D"] = PIV.MSD/4

    modelMT = ols('D ~ Time', MT).fit()
    MTslope = modelMT.params[1]
    seMT = np.array(modelMT.bse)[1]
    modelPIV = ols('D ~ Time', PIV).fit()
    PIVslope = modelPIV.params[1]
    sePIV = np.array(modelPIV.bse)[1]

    ratio = MTslope/PIVslope
    avgRatio = ratio + avgRatio
    seRatio = ratio * np.sqrt((seMT/MTslope)**2+(sePIV/PIVslope)**2)

    plottingPD.loc[len(plottingPD.index)] = [legendLabel[i], MTslope, PIVslope, seMT, sePIV, ratio, seRatio]

'''
#uncomment this section and comment next to plot ratio data
#ratio bar plot
plt.bar(plottingPD.Names, plottingPD.ratio)
plt.errorbar(plottingPD.Names, plottingPD.ratio, yerr = plottingPD.errorRatio, fmt = 'none', color = 'k', capsize = 5)
plt.xticks(fontsize = 11.5, rotation=17)
plt.ylabel("PTV/PIV Effective Diffusivity", fontsize = textSize)
plt.ylim(0,4.51)

'''
#uncomment this section and comment previous to plot absolute data
#drug bar plot
X = plottingPD.Names
X_axis = np.arange(len(plottingPD.Names))

plt.bar(X_axis - 0.2, plottingPD.PTV, 0.4, label = 'PTV',  color = colors[0])
plt.bar(X_axis + 0.2, plottingPD.PIV, 0.4, label = 'PIV', color = colors[1])

plt.errorbar(X_axis - 0.2, plottingPD.PTV, yerr = plottingPD.errorPTV, fmt = 'none', color = 'k', capsize = 5)
plt.errorbar(X_axis + 0.2, plottingPD.PIV, yerr = plottingPD.errorPIV, fmt = 'none', color = 'k', capsize = 5)

plt.xticks(X_axis, X)
plt.ylabel("Effective Diffusivity ($\mu m^2$/min)", fontsize = textSize)
plt.ylim(0,0.25)
plt.xticks(fontsize = 11.5, rotation=17)
plt.legend(fontsize = legendSize)


plt.savefig('outputimage.eps', format='eps')
