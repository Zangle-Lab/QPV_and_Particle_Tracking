# -*- coding: utf-8 -*-
"""
Created on Sat 3/19/2022

@author: alyss
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import pandas as pd
from sklearn.metrics import r2_score

plt.close()

saveLocation =  r"/Data/"

#get all pathLength comparison
setName = ["SetTwo", "SetThree", "SetTen", "SetSeven", "SetEight", "SetNine", "SetEleven"]
legendLabel = ["DMSO", "Ethanol", "Water", "Doxorubicin", "Cycloheximide", "Remdesivir", "Homoharringtonine"]

allMdisp = []
allPdisp = []

textSize = 17

plt.figure(figsize=(8,5))

for index in range(0, 7):
    MTX = pd.read_csv(saveLocation+"MTX" + setName[index])
    MTY = pd.read_csv(saveLocation+"MTY"+setName[index])
    PIX = pd.read_csv(saveLocation+"PIX"+setName[index])
    PIY = pd.read_csv(saveLocation+"PIY"+setName[index])
    diameter = pd.read_csv(saveLocation+"Diameter"+setName[index])
    dT = pd.read_csv(saveLocation+"dT"+setName[index])
    lenTrack = pd.read_csv(saveLocation+"Length"+setName[index])


    start = 0
    end = len(lenTrack)

    Mtot = []
    Ptot = []

    for i in range(start, end):
        column = str(i)
        lastCol = lenTrack.at[i, 'Length']

        #MT beginning pt to final pt diagonal
        MTXb = MTX.at[0, column]
        MTYb = MTY.at[0, column]
        MTXf = MTX.at[lastCol-1, column]
        MTYf = MTY.at[lastCol-1, column]

        Mdisp = np.sqrt((MTXf-MTXb)**2 + (MTYf-MTYb)**2)

        #PIV beginning pt to final pt diagonal
        PIXb = PIX.at[0, column]
        PIYb = PIY.at[0, column]
        PIXf = PIX.at[lastCol-1, column]
        PIYf = PIY.at[lastCol-1, column]

        Pdisp = np.sqrt((PIXf-PIXb)**2 + (PIYf-PIYb)**2)

        Mtot.append(Mdisp)
        Ptot.append(Pdisp)

        allMdisp.append(Mdisp)
        allPdisp.append(Pdisp)


    plt.scatter(Mtot, Ptot, label = legendLabel[index], s = 40)


coeff = np.polyfit(allMdisp, allPdisp, 1)
xLin = np.linspace(0, max(allMdisp))
yFit = coeff[0]*xLin+coeff[1]
plt.plot(xLin, yFit, 'k--', label = 'Linear Fit')

# need to be in order?
model = []
#get model
for each in allMdisp:
    model.append(coeff[0]*each+coeff[1])

r2 = r2_score(allPdisp, model)

plt.xlim(-1, 21)
plt.ylim(-1, 16)

plt.legend(fontsize = 10, ncol = 4)
plt.ylabel("PIV Displacement ($\mu$m)", fontsize = textSize)
plt.xlabel("PTV Displacement ($\mu$m)", fontsize = textSize)
print("Coefficients: {}".format(coeff))
print("r2: {}".format(r2))
plt.savefig('outputimage.eps', format='eps')
