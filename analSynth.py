from scipy.fftpack import fft, ifft
import numpy as np
import matplotlib.pyplot as plt


def dft(x,winL,window):
    lenAudio = len(x)
    audiodft = np.array([])

    # Applying window and computing DFT in each frame
    for i in range(0, (lenAudio - lenAudio % winL), winL):  # lenAudio&winL ro remove from lenAudio the last 283 samples
        frame = x[i:i + winL] * window
        audiodft = np.append(audiodft, fft(frame))

    return audiodft


def invDFT(dft,winL,window):
    waveOut = np.array([])
    halfWin = int(winL/2)
    for i in range(0, (len(dft)), winL):
        halfDFT = dft[i:i + halfWin]
        invHalfDFT = halfDFT[::-1]
        mirrordft = np.append(halfDFT, invHalfDFT.conj())
        np.shape(halfDFT)
        waveOut = np.append(waveOut, (ifft(mirrordft).real)*window)


    return waveOut

