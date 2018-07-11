# DFT-coder
This python project implements a first version/approach of an audio coder based on the DFT. 

In 'WAVS' folder there are 12 audio files, which are part of the MPEG dataset commonly used to evaluate new coding algorithms. They contain PCM audio recordings sampled at fs=44100Hz and quantized using 16bits/sample, which makes a data rate of 705,6 Kbits/second. 
The objective of this project is to implement a DFT-based audio coder that can compress the PCM signal by 1) using less than 16-bits to quantize, and 2) by dropping frequency bands with low energy.

## Things to bear in mind

In analSynth.py there are the functions that implement the DFT and IDFT, which will be necessarily in other functions.

In bandquant.py, the number of bands and their width is fixed. However, in more advanced coders this could be done according to the actual frame content.



