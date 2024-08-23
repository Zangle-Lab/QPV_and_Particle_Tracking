# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 11:00:37 2021

@author: alyss
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import pandas as pd
import math

plt.close()
setTwo = pd.read_csv(r"Data/ADJUSTEDdifferenceMSDsizeSetTwo.csv")
setThree = pd.read_csv(r"Data/ADJUSTEDdifferenceMSDsizeSetThree.csv")
setSeven = pd.read_csv(r"Data/ADJUSTEDdifferenceMSDsizeSetSeven.csv")
setEight = pd.read_csv(r"Data/ADJUSTEDdifferenceMSDsizeSetEight.csv")
setNine = pd.read_csv(r"Data/ADJUSTEDdifferenceMSDsizeSetNine.csv")
setTen = pd.read_csv(r"Data/ADJUSTEDdifferenceMSDsizeSetTen.csv")
setEleven = pd.read_csv(r"Data/ADJUSTEDdifferenceMSDsizeSetEleven.csv")
setRPE = pd.read_csv(r"Data/ADJUSTEDdifferenceMSDsizeRPE.csv") #additional RPE data for revision, untreated


xMin = -1
xMax = 1
yMin = -2
yMax = 4


xAxisx = [xMin, xMax]
xAxisy= [0,0]

yAxisx = [0,0]
yAxisy= [yMin, yMax]

plt.plot(xAxisx, xAxisy, 'k-')
plt.plot(yAxisx, yAxisy, 'k-')
plt.xlim(xMin, xMax)
plt.ylim(yMin, yMax)

#below code normalized by the average the slopes, instead of just the MSD slope: use version for 5a
plt.scatter(setTwo.diffSize, setTwo.diffSlope*2/(setTwo.avgMsdSlopeMT+setTwo.avgMsdSlopePI), label = "DMSO")
plt.scatter(setThree.diffSize, setThree.diffSlope*2/(setThree.avgMsdSlopeMT+setThree.avgMsdSlopePI), label = "Ethanol")
plt.scatter(setTen.diffSize, setTen.diffSlope*2/(setTen.avgMsdSlopeMT+setTen.avgMsdSlopePI), label = "Untreated")
plt.scatter(setSeven.diffSize, setSeven.diffSlope*2/(setSeven.avgMsdSlopeMT+setSeven.avgMsdSlopePI), label = "Doxorubicin")
plt.scatter(setEight.diffSize, setEight.diffSlope*2/(setEight.avgMsdSlopeMT+setEight.avgMsdSlopePI), label = "Cycloheximide")
plt.scatter(setNine.diffSize, setNine.diffSlope*2/(setNine.avgMsdSlopeMT+setNine.avgMsdSlopePI), label = "Remdesivir")
plt.scatter(setEleven.diffSize, setEleven.diffSlope*2/(setEleven.avgMsdSlopeMT+setEleven.avgMsdSlopePI), label = "Homoharringtonine")
plt.scatter(setRPE.diffSize, setRPE.diffSlope*2/(setRPE.avgMsdSlopeMT+setRPE.avgMsdSlopePI), label = "Untreated")

plt.xlabel("PTV Size - PIV Size, um")
plt.ylabel("PTV MSD/time - PIV MSD/time, norm by average")
plt.title("Slope Difference vs Size Difference")
plt.legend()
plt.xlim(-.6,.6)
plt.ylim(-2.1,2.1)
plt.savefig('outputimage.eps', format='eps')
