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

    df = pd.read_excel("zones.xlsx", sheet_name=0)
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


async def getNextItem(fMatrix,currRowCell,shag):
    matrixLen = len(fMatrix)

    if currRowCell+shag>matrixLen-1:
        #print(f"curr In Matrix with shag:{shag}",fMatrix[shag-matrixLen+currRowCell])
        return fMatrix[shag-matrixLen+currRowCell]

    #print(f"curr In Matrix with shag:{shag}", fMatrix[currRowCell+shag])
    return fMatrix[currRowCell+shag]