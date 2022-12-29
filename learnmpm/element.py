import numpy as np

class Bar1D:
    """
    1D bar element with 2 nodes.

    Attributes:

    id: int
        Element index.
    
    nodes: list
        List of nodes.

    nnodes: int
        Number of nodes in the element.

    length: float
        Element length.
    
    particles: list
        List of particles in the element.
    """

    def __init__(self):
        self.id = None
        self.nodes = [None, None]
        self.nnodes = 2
        self.size = 0.0
        self.particles = []
        self.shapefn = None