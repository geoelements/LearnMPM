import numpy as np
from LearnMPM import element

class Particle1D:
    """
    1D material point object

    Attributes:   
        id: int
            particle id
        
        mass: float
            particle mass
        
        x: float
            particle position

        xi: float
            particle position in natural coordinates
        
        material: material type
            material
        
        density: float
            particle density
        
        velocity: float
            particle velocity
        
        stress: float
            particle stress
        
        dstrain: float
            particle strain increment
        
        f_ext: float
            external force in particle

        volume: float
            particle volume
        
        element: element type
            element containing the particle
        
        shapefn: array
            nodal interpolation functions
        
        dn_dx: array
            gradient of interpolation fn in physical coordinates

    """

    def __init__(self, mass, x, xi, material):
        """Initialize particle class

        Arguments:
            mass: float
                Mass of particle

            x: float
                Particle location in physical coordinates

            xi: float
                Particle location in natural coordinates

            material: material type
        """
        self.id = None
        self.mass      = mass
        self.x         = x 
        self.xi        = xi
        self.material  = material 
        self.density   = material.density 
        self.element   = None
        self.shapefn   = np.empty([2])
        self.dn_dx     = np.empty([2])

        self.velocity  = 0.
        self.stress    = 0.
        self.dstrain   = 0.
        self.strain    = 0.
        self.f_ext     = 0.
        self.volume    = 0.

    def compute_strain(self, dt):
        """Compute particle strain by mapping nodal velocity with gradient of interpolation fn.

        Arguments:
            dt: float
                time step of simulation.
        """
        strain_rate = 0
        for i in range(self.element.nnodes):
            strain_rate += self.dn_dx[i] * self.element.nodes[i].velocity

        self.dstrain = strain_rate * dt
        # Update strain
        self.strain += self.dstrain
