import numpy as np

def dequanti(nivel, bits, Amax, Amin):

    # Make the signal change between -xsc and xsc
    Amaxmed = 5*Amax
    Aminmed = 5*Amin

    # Change from level to quantified value
    Aq = nivel-(-0.5+2**(bits-1))

    xsc =Amaxmed-Aminmed;
    Aq = Aq*xsc*(2**(1-bits))

    # Set signal back to original amplitudes
    Aq = Aq+(Amaxmed)+(Aminmed)


    return Aq