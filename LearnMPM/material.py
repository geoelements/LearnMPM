import numpy as np

class LinearElastic1D:
    def  __init__(self, E, density):
        self.E = E
        self.density = density

    def update_stress(self, particle):
        particle.stress+=particle.dstrain*self.E