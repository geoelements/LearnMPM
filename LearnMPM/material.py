import numpy as np

class LinearElastic1D:
    """ 
    Linear Elastic material for 1D

    Attributes:

    E: float
    	Young's modulus
    
    density: float
    	Density of material point
    """
    def  __init__(self, E, density):
        """Initialize material properties

        Args:
            E: Young's modulus
        
            density: Density
        """
        self.E = E
        self.density = density

    def update_stress(self, particle):
        """Update particle stress based on particle strain. :math:`d\sigma = E \cdot d\epsilon` and the stress :math:`\sigma = \sigma + d \sigma`.

        Args:
            particle: Particle object
        
        """
        particle.stress+=particle.dstrain*self.E