import numpy as np
from analSynth import dft
from quantimaxmin import quantimaxmin
from dequanti import dequanti

def energyQuantizer(audio,winL,window,overlap):

    audiodft = dft(audio,winL,window,overlap)


    # Define the amplitudes for each band
    A1 = int(np.sqrt(winL))
    A2 = A1/2
    A3 = A1/4
    A4 = A1/8
    A5 = A1/16
    ampBand = np.array([A1,A2,A3,A4,A5])

    numFrames = int(len(audiodft)/winL)
    isBandCoded = np.zeros(shape = (numFrames,5))       # (metadata) Binary matrix that will contain the info of whether a band is coded or not (0=no, 1=yes)
    quantReal = np.zeros(shape = (numFrames,5))         # Matrix where the real part of each coded band will be saved
    quantImag = np.zeros(shape = (numFrames,5))         # Matrix where the imaginary part of each coded band will be saved
    bitstream = 0                                       # Variable with the length of the bitstream coded
    energyThr = 100                                      # Value chosen randomly to define the threshold
    #quantReal1 = np.zeros(numFrames,int(winL/32))
    decAmpBand = np.zeros(shape = 5)                  # Dequantized frequency band array where we will store the decoded bands in order to sinthetize it later
   
    for i in range(0,numFrames):

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
            if max(abs(freqBand))>(freqBand[j]/energyThr):
                isBandCoded[i,j] = 1
                bitstream = bitstream + 1                                            # Add a bit to say if it is quantized or not    
                # code and save real part                                           
                _,Qlevel_Re = quantimaxmin(freqBand.real,nbits,ampBand[j],-ampBand[j])
                bitstream = bitstream + nbits
                _,Qlevel_Im = quantimaxmin(freqBand.imag,nbits,ampBand[j],-ampBand[j])
                bitstream = bitstream + nbits
                print('Band ampl', freqBand.shape)                                                  

                if j==0:
                    quantReal1 = Qlevel_Re
                    quantImag1 = Qlevel_Im
                    #print('Qlevel_Real1: ', Qlevel_Re)
                if j==1:
                    quantReal2 = Qlevel_Re
                    quantImag2 = Qlevel_Im
                    #print('Qlevel_Real2: ', Qlevel_Re)
                if j==2:
                    quantReal3 = Qlevel_Re
                    quantImag3 = Qlevel_Im
                if j==3:
                    quantReal4 = Qlevel_Re
                    quantImag4 = Qlevel_Im
                if j==4:
                    quantReal5 = Qlevel_Re
                    quantImag5 = Qlevel_Im
                    #print('hey Im in')
            else:
                isBandCoded[i,j] = 0
                bitstream = bitstream + 1
        # --------- END OF CODER ---------
        print('Coder with no errors')
        print('heeee', isBandCoded.max())

        # --------- DECODER ---------
    
        for j in range(0,5):
            if isBandCoded[i,j] == 1:                                                # Check if the band has been coded. If yes, we decode it
                nbits = 8
                # Decode amplitude real part
                Qlevel = quantReal[i,j]
                qAmp_Re = dequanti(Qlevel,nbits,ampBand[j],-ampBand[j])
                # Decode ammplitude imaginary part
                Qlevel = quantImag[i,j]
                qAmp_Imag = dequanti(Qlevel,nbits,ampBand[j],-ampBand[j])
                # We add Real and Imaginary parts band by band
                decodedAmplitued = np.array(qAmp_Re) + 1j*np.array(qAmp_Imag)        # Decoded Amplitude of the band
                if j==0:
                    decAmpBand[j] = decodedAmplitued
                    print('AMPLITUDE', decodedAmplitued)
                if j==1:
                    decAmpBand[j] = decodedAmplitued
                if j==2:
                    decAmpBand[j] = decodedAmplitued
                if j==3:
                    decAmpBand[j] = decodedAmplitued
                if j==4:
                    decAmpBand[j] = decodedAmplitued
            '''else:
                decAmpBand[j] = np.zeros(shape = bands[j].shape)      '''              #if it is not decoded, we put 0's in all values
        
        print('Decoder with no errors')

        #halfX = np.concatenate([decAmpBand[0],decAmpBand[1],decAmpBand[2],decAmpBand[3],decAmpBand[4]])        # Here we have the half dft with all the bands decoded
        

    return bitstream





