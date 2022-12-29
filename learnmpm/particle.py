import numpy as np
from learnmpm import element

class Particle1D:
    def __init__(self, mass, x, xi, material):
        self.id = None
        
        self.mass      = mass
        self.x         = x 
        self.xi        = xi
        self.material  = material 
        self.density   = material.density 
        self.element   = None
        self.shapefn   = np.array([])
        self.gradsf    = np.array([])

        self.velocity  = 0.
        self.stress    = 0.
        self.dstrain   = 0.
        self.strain    = 0.
        self.f_ext     = 0.
        self.volume    = 0.

    def compute_strain(self, dt):
        strain_rate = 0
        for i in range(self.element.nnodes):
            strain_rate += self.gradsf[i] * self.element.nodes[i].velocity

        self.dstrain = strain_rate * dt
        # Update strain
        self.strain += self.dstrain
