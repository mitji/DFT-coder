# DFT-coder
This python project implements a first version/approach of an audio coder based on the DFT. 

It consists in an incremental coder, starting from the very basics of analysis/synthesis of any digital signal processing to an "intelligent" variable bit allocation based on energy detection.

The objective of this project is to implement a `DFT-based audio coder` that can compress the PCM signal by 1) using less than 16-bits to quantize, and 2) by dropping frequency bands with low energy.

It's a university final subject project which consists in migrating to Python and improving a DFT-coder written in Matlab we made during the subject.

## Set Up
### Prerequisits
In order to have no issues with running the code, we recommend having installed python3.

All the different imports needed are called in the functions. It could be necessarily to install some packages if you don't have it. That's an easy job, just by typping in your terminal: 
```
pip install package-name
```

## Code and Project Style
The code is structured in a main.py file where the different parts of the incremental coder are called. There are also several plots already written. However, feel free to add plots of your choice to test the code. All the other files contain the functions needed to implement the different steps of the coder. 

First o fall, in 'WAVS' folder there are 12 audio files for test purposes, which are part of the MPEG dataset commonly used to evaluate new coding algorithms. They contain PCM audio recordings sampled at fs=44100Hz and quantized using 16bits/sample, which makes a data rate of 705,6 Kbits/second. 

In the `main.py` function there are the different steps made to build the coder. Tis main code is divided in three parts.

**First** 

A simple frequency analysis with DFT and IDFT

**Second** 

Divide the frames of the signal in frequency bands and apply a simple quantization

**Third** 

Apply a variable bit allocation that consists in detecting which bands are kept and which are dropped according to their energy.

In `analSynth.py` there are the functions that implement the DFT and IDFT, which will be necessarily in other functions.

In `bandquant.py`, there is the code to quantize each band of the signal frames. In our case the number of bands and their width is fixed. However, in more advanced coders this could be done according to the actual frame content. This function calls the `quantimaxmin` function that quantizes the signal wanted within a required maximum and minimum amplitude. 

In `energyQuantizer` there is the variable bit allocation based on detecting the energy of each band.


### How to use?
To run the project you just have to open your terminal, go to the project directory (DFT-coder), and write the following command:
```
python main.py
```
Once you have run it, you can listen to the generated ".wav" files in the project folder.

If you want to edit it or analyze it deeper, you will only need an editor, for instance PyCharm, useful to debug and run your code (download: https://www.jetbrains.com/pycharm/download/), or otherwise if you use a plain text editor such as Sublime Text you will have to run it in the terminal.

Some parameters you can modify and test with are the analysis window size `N`, the number of bits `nbits` to quantize the signal, the `window type` (rectangular, hanning, blackman...), the `overlapp` factor to the DFT , etc. (Open the code and play a little bit ;)).

## Authors
[David Mitjana](https://github.com/mitji) and [Oriol Nadal](https://github.com/oriolnadal)

Audiovisual Engineering Students at Universitat Pompeu Fabra, Barcelona.




