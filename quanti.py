import scipy
import numpy as np

def quanti(x,b,xsc):

    delta = (2**(1-b))*xsc
    y = ((x!=0)*np.sign(x)*(np.fix(abs(x)/delta)+(0.5)))+((x==0)*(0.5))
    ymax = (2**(b-1))-0.5
    y = ((abs(y)>ymax)*ymax*np.sign(y))+((abs(y)<=ymax)*y)
    
    return y