import numpy as np

def dequanti(nivel, bits, Amax, Amin):

    #make the signal change between -xsc and xsc
    Amaxmed = 5*np.array(Amax)
    Aminmed = 5*np.array(Amin)

    #change from level to quantified value
    Aq = nivel-(-0.5+2**(bits-1))

    xsc =Amaxmed-Aminmed;
    Aq = Aq*xsc*(2**(1-bits))

    #Set signal back to original amplitudes
    Aq = Aq+(Amaxmed)+(Aminmed)


    return Aq