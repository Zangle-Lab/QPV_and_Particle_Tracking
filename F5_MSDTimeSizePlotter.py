"""
Created on Tue Oct 26 14:27:20 2021

@author: alyss
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import pandas as pd
import math
import seaborn as sns

saveLocation = r"Data/"


plt.close()


#colors
firstColor = sns.color_palette()
secondColor = sns.color_palette("deep")
colors = firstColor + secondColor

Sets = "SetTwo","SetThree","SetTen","SetSeven","SetEight","SetNine","SetEleven"
Labels = "DMSO","Ethanol","Untreated","Dox","Cyclo","Rem","Hom"
numSets = len(Sets)

plt.close("all")


for j in range(0,numSets):
    setName = Sets[j]

    MT = pd.read_csv(saveLocation+"/MSDMT"+setName+"compiled.csv", header = None)
    PIV = pd.read_csv(saveLocation+"/MSDPI"+setName+"compiled.csv", header = None)
    diameter = pd.read_csv(saveLocation+"/Diameter"+setName)
    pivDiameter = pd.read_csv(saveLocation+"/DiameterPIV"+setName+".csv")
    dT = pd.read_csv(saveLocation+"/dT"+setName)
    numOrg = len(dT.dT)

    allSizeM = []
    allSizeP = []
    avgMsdSlopeM = []
    avgMsdSlopeP = []

    for i in range(0,numOrg):
        colMT = MT.iloc[:, i]
        colPIV = PIV.iloc[:,i]

        #create the time step
        tStep = dT.iloc[i,1]

        #temp holder of each msd/time calc for one particle
        msdTimeM = []
        msdTimeP = []


        index = 1;
        for each in colMT[1:]:
            if(math.isnan(each)):
                a = 3
                #don't include NaN in calculations
            else:
                msdTimeM.append(each/(index*tStep))
            index = index + 1

        indexB = 1;
        for eachB in colPIV[1:]:
            if(math.isnan(eachB)):
                a = 3
                #don't include NaN in calculations
            else:
                msdTimeP.append(eachB/(indexB*tStep))
            indexB = indexB + 1

        allSizeM.append(diameter.iloc[i,1])
        allSizeP.append(pivDiameter.iloc[i,1])

        avgMsdSlopeM.append(np.mean(msdTimeM))
        avgMsdSlopeP.append(np.mean(msdTimeP))


    DeffM = np.divide(avgMsdSlopeM,4)
    DeffP = np.divide(avgMsdSlopeP,4)
    Mprod = np.multiply(allSizeM,DeffM)
    Pprod = np.multiply(allSizeP,DeffP)
    plt.scatter(Mprod,Pprod, color = colors[j], marker = 'o',label=Labels[j])


#below section runs the same code to plot additional data for RPE:
saveLocation = r"Data/"
MT = pd.read_csv(saveLocation+"MSDManualTrackingRPEcompiled.csv", header = None)
PIV = pd.read_csv(saveLocation+"MSDPIVTrackingRPEcompiled.csv", header = None)
diameter = pd.read_csv(saveLocation+"DiameterRcsv.csv")
pivDiameter = pd.read_csv(saveLocation+"DiameterPIVR.csv")
dT = pd.read_csv(saveLocation+"dTRcsv.csv")

numOrg = len(dT.dT)

allSizeM = []
allSizeP = []
avgMsdSlopeM = []
avgMsdSlopeP = []

for i in range(24,numOrg): #start at 24, to get additional 12 unique vesicles in the additional dataset
    colMT = MT.iloc[:, i]
    colPIV = PIV.iloc[:,i]

    #create the time step
    tStep = dT.iloc[i,1]

    #temp holder of each msd/time calc for one particle
    msdTimeM = []
    msdTimeP = []


    index = 1;
    for each in colMT[1:]:
        if(math.isnan(each)):
            a = 3
            #don't include NaN in calculations
        else:
            msdTimeM.append(each/(index*tStep))
        index = index + 1

    indexB = 1;
    for eachB in colPIV[1:]:
        if(math.isnan(eachB)):
            a = 3
            #don't include NaN in calculations
        else:
            msdTimeP.append(eachB/(indexB*tStep))
        indexB = indexB + 1

    allSizeM.append(diameter.iloc[i,1])
    allSizeP.append(pivDiameter.iloc[i,1])

    avgMsdSlopeM.append(np.mean(msdTimeM))
    avgMsdSlopeP.append(np.mean(msdTimeP))

DeffM = np.divide(avgMsdSlopeM,4)
DeffP = np.divide(avgMsdSlopeP,4)
Mprod = np.multiply(allSizeM,DeffM)
Pprod = np.multiply(allSizeP,DeffP)
plt.scatter(Mprod,Pprod, color = colors[9], marker = 'o',label="untreated2")


Line = np.arange(0,0.5,0.1)
plt.plot(Line,Line,'k--', label="x=y")

plt.title("MSD/time vs Size")
plt.xlabel("Particle Diameter (um)")
plt.ylabel("Particle Average MSD/time (um^2/min)")
plt.legend(loc = "best")

plt.xlabel("PTV Deff*D (um^3/min)")
plt.ylabel("QPV Deff*D (um^3/min)")
plt.savefig('outputimage.eps', format='eps')
