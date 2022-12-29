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

    def is_point_in_element(self, x):
        # get the nodal position
        xn0 = self.nodes[0].x
        xn1 = self.nodes[1].x
        if x >= xn0 and x < xn1:
            return True
        else:
            return False

    def compute_xi(self, x):
        # get the nodal position
        xn0 = self.nodes[0].x
        xn1 = self.nodes[1].x
        length = abs(xn1 - xn0)
        if (self.is_point_in_element(x)):
            xi = (x - xn0) * 2./length - 1
            return True, xi
        else:
            return False, 0.