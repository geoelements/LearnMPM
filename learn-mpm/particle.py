import numpy as np

class Particle1D:
    def __init__(self, mass, x, material):
        self.id = None
        
        self.mass = mass
        self.x  = x 
        self.material = material 
        self.density = material.density 

        self.velocity  = np.array([0])
        self.stress    = np.array([0])  
        self.dstrain   = np.array([0])
        self.momentum  = np.array([0])
