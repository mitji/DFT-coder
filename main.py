from scipy.fftpack import fft, ifft
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from bandQuant import bandQuant
from analSynth import dft, invDFT
from energyQuantizer import energyQuantizer


# EX1 - Block Transform ------------------------------------------------------------------------

	# Defining variables
winL= 1024
fs = 44100
H = 0.5 									# Hop size --> H=1(NO overlap), H=0.5(50% overlap)
audio, fsaudio = sf.read('es01_m44.wav')
print(min(abs(audio))) #normalize
lenAudio = len(audio)

	# Defining windows
#window = np.hanning(winL)
#window = np.blackman(winL);
window = np.ones((winL),float)   			# Rectangular Window

#plt.plot(window*window)
#plt.show()

	# Declare auxiliar variables
audiodft = np.array([])
frame = np.zeros(winL)
overlap = 0         						# In ex 1 we don't want overlap, so we write 0

	# 1st step: COMPUTE DFT
audiodft = dft(audio,winL,window,overlap)

	# PLOTS
numFrame = 90								# We choose a random frame for ploting purpose
randomFrame = audiodft[winL*numFrame:winL*(numFrame+1)]

'''
	# Ploting magnitude and phase of the chosen frame
fig1, (mX,pX) = plt.subplots(2,1)
mX.plot(np.abs(randomFrame)); mX.set_title('Magnitude')
pX.plot(np.angle(randomFrame)); pX.set_title('Phase')
#plt.show()

	# Ploting real and imaginary part of the chosen frame
fig2, (rX,iX) = plt.subplots(2,1)
rX.plot(randomFrame.real); rX.set_title('Real part')
iX.plot(randomFrame.imag); iX.set_title('Imaginary Part')
#plt.show()
'''


	# 2nd step: COMPUTE the IDFT

	# Declare auxiliary variables
halfWin = int(winL/2)
mirrordft = np.zeros(winL)
halfDFT = np.zeros(halfWin)
waveOut = np.array([])

waveOut = invDFT(audiodft,winL,window,overlap)

'''
#Plotting original waveform and synthesized one
fig3, (oX,sX) = plt.subplots(2,1)
oX.plot(audio); oX.set_title('Original')
sX.plot(waveOut); sX.set_title('Synthesized')
#plt.show()
'''

wavfile.write("waveOut.wav",fs, waveOut)


# EX2 - Design of the frequency bands ------------------------------------------------------------------------------
# Defining bands --> inside freq bandQuantizer
# EX3 - Fixed-bit allocation and Quantization ----------------------------------------------------------------------

nbits = 8

waveOut2 = bandQuant(audio,winL,nbits,window,overlap)
wavfile.write("waveOut2.wav",fs, waveOut2)
# Compute bitrate
nsamples = len(waveOut2)
bitrate = (8*2*5*(len(audiodft)/winL))/fs
print('BITRATE --->', bitrate)


 # EX4 - Overlap-Add ----------------------------------------------------------------------

overlap = 1
waveOut_OvAdd = bandQuant(audio,winL,nbits,window,overlap)
wavfile.write("waveOut_OvAdd.wav",fs, waveOut_OvAdd)



 # EX5 - Variable Bit Allocation ----------------------------------------------------------------------

bitstream = energyQuantizer(audio,winL,window,overlap)

print('Bitstream (bits): ', bitstream)





