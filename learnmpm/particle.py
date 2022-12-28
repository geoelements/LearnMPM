import numpy as np
from learnmpm import element

class Particle1D:
    def __init__(self, mass, x, xi, material):
        self.id = None
        
        self.mass = mass
        self.x  = x 
        self.xi = xi
        self.material = material 
        self.density = material.density 
        self.element = None

        self.velocity  = np.array([0])
        self.stress    = np.array([0])  
        self.dstrain   = np.array([0])
        self.momentum  = np.array([0])
