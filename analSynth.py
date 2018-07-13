from scipy.fftpack import fft, ifft
import numpy as np
import matplotlib.pyplot as plt

# x = signal to analyze
# winL = window size
# window = window type
# overlap = boolean to apply overlap-add or not. If we decide to apply it, we make a hop size 1/2 of winL (window size)

def dft(x,winL,window,overlap):
    lenAudio = len(x)
    audiodft = np.array([])

    # Applying window and computing DFT in each frame
    for i in range(0, int(lenAudio/winL)):  
        if overlap==0:
            frame = x[i*winL:(i+1)*winL] * window
        else:
            frame = x[int(i*0.5*winL):int((i*0.5 + 1) * winL)] * window
        audiodft = np.append(audiodft, fft(frame))

    return audiodft


def invDFT(dft,winL,window,overlap):
    waveOut = np.array([])
    halfWin = int(winL/2)
    for i in range(0, int(len(dft)/winL)):
        if overlap==0:
            halfDFT = dft[i*winL:(i*winL)+halfWin]
        else:
            halfDFT = dft[int(i*0.5*winL):int(i*0.5*winL)+halfWin]
        
        invHalfDFT = halfDFT[::-1]
        mirrordft = np.append(halfDFT, invHalfDFT.conj())
        waveOut = np.append(waveOut, (ifft(mirrordft).real)*window)

    return waveOut

