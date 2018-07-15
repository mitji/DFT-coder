from scipy.fftpack import fft, ifft
import numpy as np
import matplotlib.pyplot as plt
import math 

# x = signal to analyze
# winL = window size
# window = window type
# overlap = boolean to apply overlap-add or not. If we decide to apply it, we make a hop size 1/2 of winL (window size)

def dft(x,winL,window,overlap,windowing):
    lenAudio = len(x)
    audiodft = np.array([])

    if overlap == 0:
        H = winL
    else:
        H = int(winL/2)

    # Applying window and computing DFT in each frame
    for i in range(0, int(lenAudio - (lenAudio % winL/2)),H):
        #print(winL)
        if(len(x[i:i+winL])!=1024): break

        if windowing == 1:
            frame = x[i:i+winL] * window
        else:
            frame = x[i:i + winL]

        audiodft = np.append(audiodft, fft(frame))

    return audiodft


def invDFT(lenAudio,dft,winL,window,overlap,windowing):
    waveOut = np.zeros(lenAudio)
    halfWin = int(math.ceil(winL/2))

    if overlap == 0:
        H = winL
    else:
        H = int(winL / 2)

    for i in range(0, int(len(dft)), H):
        halfDFT = dft[i:i+halfWin+1]
        #print('halfDFT shape', halfDFT.shape)

        invHalfDFT = halfDFT[:1:-1]
        #print('invhalfDFT shape', invHalfDFT.shape)
        mirrordft = np.append(halfDFT, invHalfDFT.conj())
        #waveOut = np.append(waveOut, (ifft(mirrordft).real)*window)
        #print(waveOut[i:i+winL])
        waveOut[i:i+winL] = (ifft(mirrordft).real)*window
        if windowing == 1:
            waveOut[i:i + winL] = (ifft(mirrordft).real) * window
        else:
            waveOut[i:i + winL] = (ifft(mirrordft).real)

    return waveOut

