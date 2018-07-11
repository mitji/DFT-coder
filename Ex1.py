from scipy.fftpack import fft, ifft
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from bandQuant import bandQuant
from analSynth import dft, invDFT


#EX1 - Block Transform ------------------------------------------------------------------------

# Defining variables
winL= 1024
fs = 44100
audio, fsaudio = sf.read('es01_m44.wav')
print(min(abs(audio))) #normalize
lenAudio = len(audio)

#Defining window
#window = np.hanning(winL)
#window = np.blackman(winL);
window = np.ones((winL),float)

#plt.plot(window*window)
#plt.show()

#Declare auxiliar variables
audiodft = np.array([])
frame = np.zeros(winL)

audiodft = dft(audio,winL,window)

#Choosing a random frame to plot
numFrame = 90
randomFrame = audiodft[winL*numFrame:winL*(numFrame+1)]

'''
#Ploting magnitude and phase of the chosen frame
fig1, (mX,pX) = plt.subplots(2,1)
mX.plot(np.abs(randomFrame)); mX.set_title('Magnitude')
pX.plot(np.angle(randomFrame)); pX.set_title('Phase')
#plt.show()

#Ploting real and imaginary part of the chosen frame
fig2, (rX,iX) = plt.subplots(2,1)
rX.plot(randomFrame.real); rX.set_title('Real part')
iX.plot(randomFrame.imag); iX.set_title('Imaginary Part')
#plt.show()
'''


#IFFT: Computing the IDFT

#Declare auxiliar variables
halfWin = int(winL/2)
mirrordft = np.zeros(winL)
halfDFT = np.zeros(halfWin)
waveOut = np.array([])

waveOut = invDFT(audiodft,winL,window)

'''
#Plotting original waveform and synthesized one
fig3, (oX,sX) = plt.subplots(2,1)
oX.plot(audio); oX.set_title('Original')
sX.plot(waveOut); sX.set_title('Synthesized')
#plt.show()
'''

wavfile.write("waveOut.wav",fs, waveOut)


#EX2 - Design of the frequency bands ------------------------------------------------------------------------------
#Defining bands --> inside freq bandQuantizer
#EX3 - Fixed-bit allocation and Quantization ----------------------------------------------------------------------

nbits = 8

waveOut2 = bandQuant(audiodft,winL,nbits)

wavfile.write("waveOut2.wav",fs, waveOut2)











real_dequant = np.zeros(round(len(audio)/2))
im_dequant = np.zeros(round(len(audio)/2))
finestraBandes = np.zeros(len(audio))


quantized = np.zeros(round(len(audio)/2))

audio_dur = len(audio)/fs
print(audio_dur)
data_rate = 0
data_rate2 = 0











