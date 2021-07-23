
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import os 
import pandas as pd

def sub(FileName,FsHz,x1):
    print(FsHz)
    if FsHz == 2100:
        FsHzNew = FsHz / 80
        x1New = np.array([])
        F1 = 0
        while 1:
            F2 = F1 + 80
            if F2 > len(x1):
                break
            x1New = np.append(x1New, np.mean(x1[F1:F2]))
            F1 = F2
        x1 = x1New
        FsHz = FsHzNew
    frequency(FileName,FsHz,x1)



def frequency(FileName,FsHz,x1):
    TimeArray = np.arange(0.0, np.size(x1)) / FsHz
    FreqIniHz = 30.0
    FreqEndHz = 800.0
    FreqStepHz = 5.0
    FreqTestHz = np.arange(FreqIniHz, FreqEndHz + FreqStepHz, FreqStepHz)

    TFMat = np.zeros([np.size(FreqTestHz), np.size(x1)], dtype=complex)

    NumCycles = 10

    x1fft = np.fft.fft(x1)
    for FreqIter in range(np.size(FreqTestHz)):
        xtest = np.exp(1j * 2.0 * np.pi * FreqTestHz[FreqIter] * TimeArray)
        xtestwinstd = ((1.0 / FreqTestHz[FreqIter]) * NumCycles) / 2.0
        xtestwin = np.exp(-0.5 * (TimeArray / xtestwinstd) ** 2.0)
        xtest = xtest * xtestwin
        fftxtest = np.fft.fft(xtest)
        fftxtest = abs(fftxtest)
        TFMat[FreqIter, :] = np.fft.ifft(x1fft * fftxtest)

        TFMatAbs = np.abs(TFMat)
        TFMatAbsMax = np.zeros([np.size(TFMatAbs, 0), np.size(TFMatAbs, 1)])
    FreqLenHz = 20
    FreqLenPoints = np.int(np.round(FreqLenHz / FreqStepHz))
    TimeLenSec = 0.25
    TimeLenSam = np.int(np.round(TimeLenSec * FsHz))

    for i in range(np.size(TFMatAbsMax, 0)):
        for j in range(np.size(TFMatAbsMax, 1)):
            iF1 = i - FreqLenPoints
            iF2 = i + FreqLenPoints
            jF1 = j - TimeLenSam
            jF2 = j + TimeLenSam
            if iF1 < 0 or iF2 > np.size(TFMatAbsMax, 0) or \
                    jF1 < 0 or jF2 > np.size(TFMatAbsMax, 1):
                continue
            MatAux = TFMatAbs[iF1:iF2, jF1:jF2]
            maxin = np.argmax(MatAux)
            maxin_i = maxin // np.size(MatAux, 1)
            maxin_j = maxin - (maxin_i  * np.size(MatAux, 1))
            TFMatAbsMax[iF1 + maxin_i, jF1 + maxin_j] = \
              TFMatAbs[iF1 + maxin_i, jF1 + maxin_j]


    TFMatAbsMaxBin = np.zeros([np.size(TFMatAbsMax, 0), np.size(TFMatAbsMax, 1)])
    for i in range(np.size(TFMatAbsMax, 0)):
        for j in range(np.size(TFMatAbsMax, 1)):
            if TFMatAbsMax[i,j] == 0:
                continue

            MatValues, MatiValues, MatjValues = \
            GetConnectedPatchMat(TFMatAbsMax, i, j)
            # for c1 in range(np.size(MatiValues)):
            #     TFMatAbsMaxBin[np.int(MatiValues[c1]), np.int(MatjValues[c1])] = 0.5

            maxin = np.argmax(MatValues)
            maxin_i = np.int(MatiValues[maxin])
            maxin_j = np.int(MatjValues[maxin])
            TFMatAbsMaxBin[maxin_i, maxin_j] = 1.0


    HashValues = np.array([])
    TFMatAbsMax = np.zeros([np.size(TFMatAbs, 0), np.size(TFMatAbs, 1)])
    FreqLenHz = 50
    FreqLenPoints = np.int(np.round(FreqLenHz / FreqStepHz))
    TimeLenSec = 1.0
    TimeLenSam = np.int(np.round(TimeLenSec * FsHz))
    TimeForwardSec = 0.25
    TimeForwardSam = np.int(np.round(TimeForwardSec * FsHz))
    for i in range(np.size(TFMatAbsMaxBin, 0)):
        for j in range(np.size(TFMatAbsMaxBin, 1)):
            if TFMatAbsMaxBin[i][j] == 0.0:
                continue
            HashFreqHz = np.int(np.round(FreqTestHz[i]))    
            HashTimeMilliSec = np.int(np.round(TimeArray[j] * 1000))
            iF1 = i - FreqLenPoints
            iF2 = i + FreqLenPoints
            jF1 = j + TimeForwardSam
            jF2 = jF1 + TimeLenSam
            if iF1 < 0:
                iF1 = 0
            if iF2 >= np.size(TFMatAbsMaxBin, 0):
                iF2 = np.size(TFMatAbsMaxBin, 0) - 1
            if jF1 > np.size(TFMatAbsMaxBin, 1):
                continue
            if jF2 >= np.size(TFMatAbsMaxBin, 1):
                jF2 = np.size(TFMatAbsMaxBin, 1) - 1
            for i1 in range(iF1, iF2 + 1):
                for j1 in range(jF1, jF2 + 1):
                    if TFMatAbsMaxBin[i1][j1] == 0.0:
                        continue
                    HashFreqHzAux = np.int(np.round(FreqTestHz[i1]))
                    HashTimeMilliSecAux = np.int(np.round(TimeArray[j1] * 1000))

                    HashTimeDiffMilliSecAux = \
                     np.int(HashTimeMilliSecAux - HashTimeMilliSec)
                    HashLine = np.array([HashTimeMilliSec,HashFreqHz,HashFreqHzAux, HashTimeDiffMilliSecAux])
                    if np.size(HashValues) == 0:
                        HashValues = np.array([HashLine])
                    else:
                        HashValues = np.append(HashValues,[HashLine], 0)
    
    data = {'Hash': HashValues.flatten()}

    df = pd.DataFrame(data, columns = ['Hash'])
    abc = FileName+'.csv'
    df.to_csv(abc, sep=';', index=False)

    print(pd.read_csv(FileName+'.csv', names=['Hash'], sep=";"))


##
# Definimos una función para encontrar el
# máximo dentro de cada parche de puntos conectados
def GetConnectedPatchMat(MatIn, iIn, jIn):
    MatValues = np.array([])
    MatiValues = np.array([])
    MatjValues = np.array([])
    MatijCheck = np.array([[iIn, jIn]])
    while 1:
        if np.size(MatijCheck) == 0:
            break
        iInAux = np.int(1 * MatijCheck[0][0])
        jInAux = np.int(1 * MatijCheck[0][1])
        MatijCheck = np.delete(MatijCheck, 0, 0)
        i1 = iInAux - 1
        if i1 < 0:
            i1 = 0
        i2 = iInAux + 1
        if i2 >= np.size(MatIn, 0):
            i2 = np.size(MatIn, 0) - 1
        j1 = jInAux - 1
        if j1 < 0:
            j1 = 0
        j2 = jInAux + 1
        if j2 >= np.size(MatIn, 1):
            j2 = np.size(MatIn, 1) - 1
        for iCount in range(i1, i2 + 1):
            for jCount in range(j1, j2 + 1):
                if MatIn[iCount, jCount] == 0.0:
                    continue
                ValAux = 1.0 * MatIn[iCount, jCount]
                MatValues = np.append(MatValues, [ValAux])
                MatiValues = np.append(MatiValues, [iCount])
                MatjValues = np.append(MatjValues, [jCount])
                MatIn[iCount, jCount] = 0.0
                if iCount == iIn and jCount == jIn:
                    continue

                MatijCheck = np.append(MatijCheck, [[iCount, jCount]], 0)

    return MatValues, MatiValues, MatjValues



