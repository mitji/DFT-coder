from scipy.fftpack import fft, ifft
import numpy as np
from quantimaxmin import quantimaxmin
from analSynth import dft


def bandQuant(x,winL,nbits,window, overlap): #LI CANVIEM EL NOM A LA FUNCIÓ¿?

    audiodft = dft(x, winL, window, overlap) 
    halfX = np.array([])
    waveOut = np.array([])

    # Define the amplitudes for each band
    A1 = int(np.sqrt(winL))
    A2 = A1/2
    A3 = A1/4
    A4 = A1/8
    A5 = A1/16

    for i in range(0,int(len(x)/winL)):
        newX = np.array([])

        frame = audiodft[i*winL:(i+1)*winL]

        # Separate each frame in frequency bands
        # We are only using half dft. We first divide in freq bands or octaves and then quantize and do the synthesis
        fb1 = frame[0:int(winL/32)]
        fb2 = frame[int(winL/32):int(winL/16)]
        fb3 = frame[int(winL/16):int(winL/8)]
        fb4 = frame[int(winL/8):int(winL/4)]
        fb5 = frame[int(winL/4):int(winL/2)]

        # Quantize real part
        fb1_Q_Re,_ = quantimaxmin(fb1.real,nbits,A1,-A1)
        fb2_Q_Re,_ = quantimaxmin(fb2.real,nbits,A2,-A2)
        fb3_Q_Re,_ = quantimaxmin(fb3.real,nbits,A3,-A3)
        fb4_Q_Re,_ = quantimaxmin(fb4.real,nbits,A4,-A4)
        fb5_Q_Re,_ = quantimaxmin(fb5.real,nbits,A5,-A5)

        # Quantize imaginary part
        fb1_Q_Imag,_ = quantimaxmin(fb1.imag,nbits,A1,-A1)
        fb2_Q_Imag,_ = quantimaxmin(fb2.imag,nbits,A2,-A2)
        fb3_Q_Imag,_ = quantimaxmin(fb3.imag,nbits,A3,-A3)
        fb4_Q_Imag,_ = quantimaxmin(fb4.imag,nbits,A4,-A4)
        fb5_Q_Imag,_ = quantimaxmin(fb5.imag,nbits,A5,-A5)

        # Add Quantized Real and Imaginary parts
        fb1_Q = np.array(fb1_Q_Re) + 1j*np.array(fb1_Q_Imag)
        fb2_Q = np.array(fb2_Q_Re) + 1j*np.array(fb2_Q_Imag)
        fb3_Q = np.array(fb3_Q_Re) + 1j*np.array(fb3_Q_Imag)
        fb4_Q = np.array(fb4_Q_Re) + 1j*np.array(fb4_Q_Imag)
        fb5_Q = np.array(fb5_Q_Re) + 1j*np.array(fb5_Q_Imag)

        # Half spectrum quantized
        halfX = np.concatenate([fb1_Q,fb2_Q,fb3_Q,fb4_Q,fb5_Q])
        # We flip the spectrum and do the conjugate to get te full spectrum
        newX = np.append(halfX, halfX[:0:-1].conj())

        #ifft
        waveOut = np.append(waveOut,ifft(newX).real)

    
    return waveOut