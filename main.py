from scipy.fftpack import fft, ifft
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from bandQuant import bandQuant
from analSynth import dft, invDFT
from energyQuantizer import energyQuantizer
import soundfile as sf


# EX1 - Block Transform ------------------------------------------------------------------------

	# Defining variables
winL= 1024
H = 0.5 									# Hop size --> H=1(NO overlap), H=0.5(50% overlap)
#fsaudio, audio = wavfile.read('es01_m44.wav')
audio, fsaudio = sf.read('WAVS/es01_m44.wav')
#audio = audio/max(audio) #normalize
lenAudio = len(audio)

	# Defining windows
#window = np.hanning(winL)
#window = np.blackman(winL)
window = np.ones((winL),float)   			# Rectangular Window

#plt.plot(window/window)
#plt.show()

	# Declare auxiliar variables
audiodft = np.array([])
frame = np.zeros(winL)
overlap = 0         						# In ex 1 we don't want overlap, so we write 0
windowing = 0                               # Apply windowing = 1

	# 1st step: COMPUTE DFT
audiodft = dft(audio,winL,window,overlap,windowing)

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

waveOut = invDFT(lenAudio,audiodft,winL,window,overlap,windowing)

'''
#Plotting original waveform and synthesized one
fig3, (oX,sX) = plt.subplots(2,1)
oX.plot(audio); oX.set_title('Original')
sX.plot(waveOut); sX.set_title('Synthesized')
#plt.show()
'''

wavfile.write("waveOut.wav",fsaudio, waveOut)


# EX2 - Design of the frequency bands ------------------------------------------------------------------------------
# Defining bands --> inside freq bandQuantizer
# EX3 - Fixed-bit allocation and Quantization ----------------------------------------------------------------------

nbits = 8								

waveOut2 = bandQuant(audio,winL,nbits,window,overlap)
wavfile.write("waveOut2.wav",fsaudio, waveOut2)
# Compute bitrate
nsamples = len(waveOut2)
bitrate = nbits*fsaudio
print('BITRATE exercise 3 --->', bitrate/1000, ' kb/s')


 # EX4 - Overlap-Add ----------------------------------------------------------------------

overlap = 1
windowing = 1
waveOut_OvAdd = bandQuant(audio,winL,nbits,window,overlap)
wavfile.write("waveOut_OvAdd.wav",fsaudio, waveOut_OvAdd)
num_windows = int(lenAudio/(int(winL)/2))							# Number of windows with overlapp-add of factor 2
nbits_total = nbits * winL  * num_windows
bitrate2 = (nbits_total * fsaudio) / lenAudio
print('BITRATE exercise 4 (Overlap-Add) --->', '%.2f' %(bitrate2/1000), 'kb/s')


 # EX5 - Variable Bit Allocation ----------------------------------------------------------------------
overlap = 0
bitstream, waveOut_freqBands = energyQuantizer(audio,winL,window,overlap)

#print('Bitstream (bits): ', bitstream)
wavfile.write("waveOut_freqBands.wav",fsaudio, waveOut_freqBands)					
bitrate3 = (bitstream / lenAudio) * fsaudio
print('BITRATE exercise 5 (Variable Bit Allocation) --->', '%.2f' %(bitrate3/1000), 'kb/s')







