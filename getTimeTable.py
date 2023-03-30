import os

import numpy as np
import pandas as pd




async def getTimetable(isFlatten=True):
    """Function that read Excel file and return matrix
    ...

     Attributes
    ----------
    isFlatten : bool
        if true, return array (matrix in one row)
    """
    path=os.getcwd()
    df = pd.read_excel(path+"/zones.xlsx", sheet_name=1)
    matrix = np.delete(df.to_numpy(), 0, 1)
    if isFlatten:
        matrix = np.ndarray.tolist(matrix.flatten())
    return matrix


async def detectCurrentEventReturnString(zoneNum):

    match zoneNum:
        case 0: zoneNum = "БІЛА ЗОНА"
        case 1: zoneNum = "СІРА ЗОНА"
        case 2: zoneNum = "ЧОРНА ЗОНА"
    return zoneNum

async def getNextEvent(fMatrix,currRowCell,shag):
    matrixLen = len(fMatrix)


    if currRowCell+shag>matrixLen-1:
        return fMatrix[shag-matrixLen+currRowCell]

    return fMatrix[currRowCell+shag]


def getItem(arr,currentPos,shag=0):
    return np.take(arr,indices=currentPos+shag,mode='wrap')

time=['00:00:00', '01:00:00', '02:00:00', '03:00:00', '04:00:00', '05:00:00', '06:00:00', '07:00:00', '08:00:00', '09:00:00', '10:00:00', '11:00:00', '12:00:00', '13:00:00', '14:00:00', '15:00:00', '16:00:00', '17:00:00', '18:00:00', '19:00:00', '20:00:00', '21:00:00', '22:00:00', '23:00:00']
def getTimeByPos(pos):
    return getItem(time,pos%len(time))

def getNextGroupItem(arr,currentPos,shag):
    if getItem(arr,currentPos)==getItem(arr,currentPos+1):
        return getNextGroupItem(arr,currentPos+1,shag)
    return [getItem(arr,currentPos+1),currentPos+1]

async def getNextItem(fMatrix,currRowCell,shag):
    matrixLen = len(fMatrix)
    if currRowCell+shag>matrixLen-1:
        return fMatrix[shag-matrixLen+currRowCell]
    return fMatrix[currRowCell+shag]