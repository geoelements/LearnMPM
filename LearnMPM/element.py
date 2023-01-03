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
        """Checks if a given material point coordinates is withing the cell

        Args:
            x: coordinate of material point
        
        Returns:
            A boolean to indicate if a coordinate is in the cell or not
        """
        # get the nodal position
        xn0 = self.nodes[0].x
        xn1 = self.nodes[1].x
        if x >= xn0 and x < xn1:
            return True
        else:
            return False

    def compute_xi(self, x):
        """Computes the local xi (natural coordinates) of a given coordinate(x)
        The function transforms the physical coordinate to a natural coordinate.
        We call the `is_point_in_element(x)` function to check if the coordinate
        is in the cell.

        Args:
            x: coordinate of material point
        
        Returns:
            A tuple of a boolean to indicate if a coordinate is in the cell or not
            and the natural coordinate equivalent of the physical coordinate. We 
            return a value of zero for the natural coordinate, if the coordinate is
            not in the cell.
        """
        # get the nodal position
        xn0 = self.nodes[0].x
        xn1 = self.nodes[1].x
        length = abs(xn1 - xn0)
        if (self.is_point_in_element(x)):
            xi = (x - xn0) * 2./length - 1
            return True, xi
        else:
            return False, 0.