import numpy as np
from quanti import quanti


def quantimaxmin(A,bits,Amax,Amin):

    # Output:
        # ampQ: Quantized Amplitude
        # level: Quantization level

    # Make the signal vary between values within the range -xsc and xsc
    Amaxmed = Amax*5
    Aminmed = Amin*5
    xsc = (Amaxmed-Aminmed)
    A2 = A - (Amaxmed + Aminmed)

    # Quantize
    ampQ = quanti(A2, bits, xsc)
    level = ampQ + (-.5 + 2**(bits - 1))
    level = np.round(level)

    ampQ = ampQ * xsc * (2 ** (1 - bits))

    ampQ = ampQ + (Amaxmed + Aminmed)

    return ampQ, level