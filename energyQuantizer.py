import numpy as np
from analSynth import dft
from quantimaxmin import quantimaxmin
from dequanti import dequanti
from scipy.fftpack import ifft


def energyQuantizer(audio,winL,window,overlap):

    windowing = 0
    audiodft = dft(audio,winL,window,windowing)

    # Define the amplitudes for each band
    A1 = int(np.sqrt(winL))
    A2 = A1/2
    A3 = A1/4
    A4 = A1/8
    A5 = A1/16
    ampBand = np.array([A1,A2,A3,A4,A5])

    numFrames = int(len(audiodft)/winL)
    isBandCoded = np.zeros(shape = (numFrames, 5))      # Matrix where we save the bits that inform if a band is coded or not
    quantImag = np.zeros(shape = (numFrames,5))         # Matrix where the imaginary part of each coded band will be saved
    bitstream = 0                                       # Variable with the length of the bitstream coded
    energyThr = 0.08                                    # Value chosen randomly to define the threshold
    #quantReal1 = np.zeros(numFrames,int(winL/32))
    halfX = np.array([])                                # Will allocate the half spectrum after decoder
    waveOut_freqBands = np.array([])                    # Decoded signal

    for i in range(0,numFrames):

        bitstream = bitstream + 1                                                   # We send a bit to indicate weather the frame is sent or not
        
        # --------- CODER ---------
        
        frame = audiodft[i*winL:(i+1)*winL]

        # Separate each frame in frequency bands
        fb1 = frame[0:int(winL/32)]
        fb2 = frame[int(winL/32):int(winL/16)]
        fb3 = frame[int(winL/16):int(winL/8)]
        fb4 = frame[int(winL/8):int(winL/4)]
        fb5 = frame[int(winL/4):int(winL/2)]
        bands = np.array([fb1,fb2,fb3,fb4,fb5])
        nbits = 8                                                                   # In our case we will use the same number of bits for each band
        
        for j in range(0,5):
            freqBand = bands[j]                                                     # We take the frequency band to code
            if max(abs(freqBand))>(ampBand[j]*energyThr):
                isBandCoded[i,j] = 1
                bitstream = bitstream + 1                                           # Add a bit to say that it is coded    
                # code and save real part                                           
                _,Qlevel_Re = quantimaxmin(freqBand.real,nbits,ampBand[j],-ampBand[j])
                bitstream = bitstream + nbits
                # code and save imaginary part
                _,Qlevel_Im = quantimaxmin(freqBand.imag,nbits,ampBand[j],-ampBand[j])
                bitstream = bitstream + nbits

                if j==0:
                    quantReal1 = Qlevel_Re
                    quantImag1 = Qlevel_Im
                if j==1:
                    quantReal2 = Qlevel_Re
                    quantImag2 = Qlevel_Im
                if j==2:
                    quantReal3 = Qlevel_Re
                    quantImag3 = Qlevel_Im
                if j==3:
                    quantReal4 = Qlevel_Re
                    quantImag4 = Qlevel_Im
                if j==4:
                    quantReal5 = Qlevel_Re
                    quantImag5 = Qlevel_Im
            else:
                isBandCoded[i,j] = 0
                bitstream = bitstream + 1                                           # Add a bit to say that it is not coded
        
        # --------- END OF CODER ---------
        #print('Coded with no errors')

        # --------- DECODER ---------

        decAmpBand = np.array([np.zeros(len(fb1)), np.zeros(len(fb2)), np.zeros(len(fb3)),np.zeros(len(fb4)),np.zeros(len(fb5))]) # Dequantized frequency band array where we will store the decoded bands in order to sinthetize it later
        halfX = np.array([])
        newX = np.array([])                                                         # Full spectrum of each frame

        for j in range(0,5):
            if isBandCoded[i,j] == 1:                                                # Check if the band has been coded. If yes, we decode it
                nbits = 8
                if j==0:
                    qAmp_Re1 = dequanti(quantReal1,nbits,ampBand[j],-ampBand[j])     # Decode amplitude real part
                    qAmp_Imag1 = dequanti(quantImag1,nbits,ampBand[j],-ampBand[j])   # Decode ammplitude imaginary part
                    decAmpBand[j] = np.array(qAmp_Re1) + 1j*np.array(qAmp_Imag1)     # Add real and imag parts     
                if j==1:
                    qAmp_Re2 = dequanti(quantReal2,nbits,ampBand[j],-ampBand[j])     
                    qAmp_Imag2 = dequanti(quantImag2,nbits,ampBand[j],-ampBand[j])   
                    decAmpBand[j] = np.array(qAmp_Re2) + 1j*np.array(qAmp_Imag2)
                if j==2:
                    qAmp_Re3 = dequanti(quantReal3,nbits,ampBand[j],-ampBand[j])     
                    qAmp_Imag3 = dequanti(quantImag3,nbits,ampBand[j],-ampBand[j])   
                    decAmpBand[j] = np.array(qAmp_Re3) + 1j*np.array(qAmp_Imag3)  
                if j==3:
                    qAmp_Re4 = dequanti(quantReal4,nbits,ampBand[j],-ampBand[j])     
                    qAmp_Imag4 = dequanti(quantImag4,nbits,ampBand[j],-ampBand[j])   
                    decAmpBand[j] = np.array(qAmp_Re4) + 1j*np.array(qAmp_Imag4)
                if j==4:
                    qAmp_Re5 = dequanti(quantReal5,nbits,ampBand[j],-ampBand[j])     
                    qAmp_Imag5 = dequanti(quantImag5,nbits,ampBand[j],-ampBand[j])   
                    decAmpBand[j] = np.array(qAmp_Re5) + 1j*np.array(qAmp_Imag5)

        # --------- END OF DECODER ---------                
        #print('Decoded with no errors')

        halfX = np.concatenate([decAmpBand[0],decAmpBand[1],decAmpBand[2],decAmpBand[3],decAmpBand[4]])    # Here we have the half dft with all the bands decoded     
        newX = np.append(halfX, halfX[::-1].conj())                                                        # We flip the spectrum and do the conjugate to get te full spectrum        
        waveOut_freqBands = np.append(waveOut_freqBands,(ifft(newX).real)*window)                          # Compute IDFT
        
    
    return bitstream, waveOut_freqBands





